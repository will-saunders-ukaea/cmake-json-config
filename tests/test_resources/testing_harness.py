import tempfile
import os
import subprocess
import shutil
import shlex
import json

VERBOSE = False
JSONCONFIG = "JSONConfig.cmake"
TEST_RESOURCES_PATH = os.path.expanduser(os.path.dirname(os.path.abspath(__file__)))
INTERFACE_FILE = os.path.join(TEST_RESOURCES_PATH, "..", "..", JSONCONFIG)
EXAMPLE_FILE = os.path.join(
    TEST_RESOURCES_PATH, "..", "..", "examples", "CMakeLists.txt"
)


def get_test_paths(path: str) -> tuple[str, str]:
    """
    :param str arg: Root directory containing files "default.json" and "spec.json".
    :returns: Pair of paths to default.json and spec.json.
    """

    paths = (
        os.path.join(TEST_RESOURCES_PATH, path, "default.json"),
        os.path.join(TEST_RESOURCES_PATH, path, "spec.json"),
    )
    assert os.path.exists(paths[0])
    assert os.path.exists(paths[1])
    return paths


def setup_test_directory(path: str, json_default: str, json_spec: str) -> None:
    """
    Setup a directory to run the test with the structure:

    ├── build
    ├── cmake
    │   └── cmake-json-config
    │       └── JSONConfig.cmake
    ├── CMakeLists.txt
    └── config
        ├── default.json
        └── spec.json

    :param str path: Directory to setup test in.
    :param str json_default: JSON file for default config.
    :param str json_spec: JSON file for specialisation config.
    """
    assert os.path.exists(INTERFACE_FILE)
    assert os.path.exists(path)
    os.mkdir(os.path.join(path, "cmake"))
    os.mkdir(os.path.join(path, "cmake", "cmake-json-config"))
    dst_path = os.path.join(path, "cmake", "cmake-json-config", JSONCONFIG)
    shutil.copyfile(INTERFACE_FILE, dst_path)
    assert os.path.exists(dst_path)
    config_path = os.path.join(path, "config")
    os.mkdir(config_path)
    assert os.path.exists(config_path)

    dst_path = os.path.join(path, "config", "default.json")
    shutil.copyfile(json_default, dst_path)
    assert os.path.exists(dst_path)

    dst_path = os.path.join(path, "config", "spec.json")
    shutil.copyfile(json_spec, dst_path)
    assert os.path.exists(dst_path)

    dst_path = os.path.join(path, "CMakeLists.txt")
    shutil.copyfile(EXAMPLE_FILE, dst_path)
    assert os.path.exists(dst_path)

    build_path = os.path.join(path, "build")
    os.mkdir(build_path)
    assert os.path.exists(build_path)


def get_cmake_cache(path: str) -> dict:
    """
    Get the CMakeCache.txt from path/build as a dict.

    :param str path: Root of testing directory.
    :returns: Dict containing values in CMake cache.
    """
    cmakecachetxt = os.path.join(path, "build", "CMakeCache.txt")
    assert os.path.exists(cmakecachetxt)

    cmake_cache = {}
    with open(cmakecachetxt) as fh:
        for line in fh:
            line = line.strip()
            if line.count("=") == 1:
                key, value = line.split("=")
                key = key.split(":")[0]
                cmake_cache[key] = value
    return cmake_cache


class CMakeRun:
    """
    Class to setup, run and test the cmake functionality.
    """

    def __init__(self, json_default: str, json_spec: str, cmake_args: str = ""):
        """
        Create tester.

        :param str json_default: Path to JSON file containing default
        preprocessor definitions.
        :param str json_spec: Path to JSON file containing specialisation
        preprocessor definitions.
        :param str cmake_args: Override a definition using the command line.
        """
        self.json_default = json_default
        self.json_spec = json_spec
        self.verbose = VERBOSE
        self.tree_exists = shutil.which("tree") is not None
        self.cmd = ["cmake"] + shlex.split(cmake_args) + [".."]

    def _call_tree(self, tmp_dir):
        if self.tree_exists:
            subprocess.check_call(["tree"], cwd=tmp_dir)

    def call_cmake(self) -> bool:
        """
        Run cmake and test that the values in the cache match the expected
        values from the JSON files.

        :returns: True if self testing passes.
        """

        tmp_dir_handle = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_handle.name
        setup_test_directory(tmp_dir, self.json_default, self.json_spec)

        if self.verbose:
            self._call_tree(tmp_dir)

        stdout_filename = os.path.join(tmp_dir, "cmake.stdout")
        stderr_filename = os.path.join(tmp_dir, "cmake.stderr")
        error_code = True
        with open(stdout_filename, "w") as stdout_fh:
            with open(stderr_filename, "w") as stderr_fh:
                try:
                    subprocess.check_call(
                        self.cmd,
                        cwd=os.path.join(tmp_dir, "build"),
                        stdout=stdout_fh,
                        stderr=stderr_fh,
                    )
                except subprocess.CalledProcessError as e:
                    print(e)
                    error_code = False

        if self.verbose:
            print("")
            print("-" * 80)
            with open(stdout_filename) as fh:
                print(fh.read())
            print("." * 80)
            with open(stderr_filename) as fh:
                print(fh.read())
            print("-" * 80)
            self._call_tree(tmp_dir)

        return error_code and self.test_cmake_cache(tmp_dir)

    def test_cmake_cache(self, tmp_dir: str) -> bool:
        cmake_cache = get_cmake_cache(tmp_dir)
        default_config = json.loads(open(self.json_default).read())
        spec_config = json.loads(open(self.json_spec).read())

        default_cpp = default_config["preprocessor_defines"]
        spec_cpp = spec_config["preprocessor_defines"]

        # create the correct config as a python dict
        config = {}
        for key, value in default_cpp.items():
            config[key] = value
        for key, value in spec_cpp.items():
            config[key] = value
        for cx in self.cmd:
            if cx.startswith("-DJSON_CONFIG_CPP_"):
                cx = cx[18:]
                key, value = cx.split("=")
                config[key] = value

        print("-----------------------")
        for key, value in config.items():
            print(key, value)
        print("-----------------------")
        for key, value in cmake_cache.items():
            print(key, value)

        # compare each item with the cache version
        for key, value in config.items():
            if not key in cmake_cache.keys():
                return False
            to_test = cmake_cache[key]
            if str(value) != str(to_test):
                return False

        return True
