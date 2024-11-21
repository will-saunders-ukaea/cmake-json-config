import tempfile
import os
import subprocess
import shutil

JSONCONFIG = "JSONConfig.cmake"
TEST_RESOURCES_PATH = os.path.expanduser(
    os.path.dirname(os.path.abspath(__file__))
)
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
    Setup a directory to run the test in.

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


class CMakeRun:
    def __init__(self, json_default: str, json_spec: str):
        self.json_default = json_default
        self.json_spec = json_spec

    def __call__(self) -> bool:
        tmp_dir_handle = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_handle.name
        setup_test_directory(tmp_dir, self.json_default, self.json_spec)
        subprocess.check_call(["tree"], cwd=tmp_dir)

        cmd = ["cmake", ".."]

        stdout_filename = os.path.join(tmp_dir, "cmake.stdout")
        stderr_filename = os.path.join(tmp_dir, "cmake.stderr")
        with open(stdout_filename, "w") as stdout_fh:
            with open(stderr_filename, "w") as stderr_fh:
                try:
                    subprocess.check_call(
                        cmd,
                        cwd=os.path.join(tmp_dir, "build"),
                        stdout=stdout_fh,
                        stderr=stderr_fh,
                    )
                except subprocess.CalledProcessError as e:
                    print(e)
                    return False

        print("")
        print("-" * 80)
        with open(stdout_filename) as fh:
            print(fh.read())

        print("." * 80)
        with open(stderr_filename) as fh:
            print(fh.read())

        print("-" * 80)

        subprocess.check_call(["tree"], cwd=tmp_dir)

        return True
