import tempfile
import os

TEST_RESOURCES_PATH = os.path.expanduser(os.path.dirname(os.path.abspath(__file__)))


def get_test_paths(path):
    return (
        os.path.join(TEST_RESOURCES_PATH, path, "default.json"),
        os.path.join(TEST_RESOURCES_PATH, path, "spec.json"),
    )


class CMakeRun:
    def __init__(self, json_default, json_spec):
        self.json_default = json_default
        self.json_spec = json_spec
