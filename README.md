# JSONConfig ![Tests](https://github.com/will-saunders-ukaea/cmake-json-config/actions/workflows/run_tests.yaml/badge.svg?branch=main)

Library to create and configure CMake variables from a JSON file. Only requires Python for testing purposes.


## Usage

```
# Include the JSONConfig.cmake from the root of this project. e.g. by checking
# out this repository as a submodule in the project cmake directory.
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake-json-config/JSONConfig.cmake)

# Get paths to a JSON file of default values and specialisations for this
# build.
cmake_path(SET DEFAULT_JSON "${CMAKE_CURRENT_SOURCE_DIR}/config/default.json")
cmake_path(SET SPEC_JSON "${CMAKE_CURRENT_SOURCE_DIR}/config/spec.json")

# This sets JSON_CONFIG_PREPROCESSOR_NAMES and JSON_CONFIG_PREPROCESSOR_VALUES
json_config_get(${DEFAULT_JSON} ${SPEC_JSON})
```

# JSON files
Both default and specialisation values are set from the JSON files as follows:

```
{
    "preprocessor_defines" : {
        "ABC_INT" : 32,
        "ABC_STRING": "FOO",
        "ABC_DEFAULT_INT" : 64,
        "ABC_DEFAULT_STRING" : "BAR"
    }
}

```

Values can also be overridden on the cmake command line by adding the prefix `JSON_CONFIG_CPP_` to a definition. Note that `JSON_CONFIG_` specifies a variable in this utility and `CPP_` denotes a C preprocessor definition.

For example
```
cmake -DJSON_CONFIG_CPP_ABC_DEFAULT_STRING=456 ...
```
overrides the `ABC_DEFAULT_STRING` to `456`.




