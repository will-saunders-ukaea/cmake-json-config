cmake_minimum_required(VERSION 3.19)
project(JSONConfig VERSION 0.0.1)

include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake-json-config/JSONConfig.cmake)

cmake_path(SET DEFAULT_JSON "${CMAKE_CURRENT_SOURCE_DIR}/config/default.json")
cmake_path(SET SPEC_JSON "${CMAKE_CURRENT_SOURCE_DIR}/config/spec.json")

# This sets JSON_CONFIG_PREPROCESSOR_NAMES and JSON_CONFIG_PREPROCESSOR_VALUES
json_config_get(${DEFAULT_JSON} ${SPEC_JSON})

# write the JSON_CONFIG to CMakeCache.txt
json_config_write_to_cmake_cache()
