import pytest
import json
import shutil

from test_resources.testing_harness import *


def test_cmake_exists():
    assert shutil.which("cmake") is not None


def test_pair_0():
    cmake_run = CMakeRun(*get_test_paths("pair_0"))
    cmake_run.verbose = True
    assert cmake_run()
