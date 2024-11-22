import pytest
import json
import shutil

from test_resources.testing_harness import *


def test_cmake_exists():
    assert shutil.which("cmake") is not None


def test_pair_0():
    cmake_run = CMakeRun(*get_test_paths("pair_0"))
    assert cmake_run.call_cmake()


def test_pair_0_cmdline_default_override():
    cmake_run = CMakeRun(*get_test_paths("pair_0"), "-DABC_DEFAULT_STRING=XYZ")
    assert cmake_run.call_cmake()


def test_pair_0_cmdline_spec_override():
    cmake_run = CMakeRun(*get_test_paths("pair_0"), "-DABC_SPEC_STRING=XYZ")
    assert cmake_run.call_cmake()
