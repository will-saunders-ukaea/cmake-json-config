# Helper macro for internal use. This macro pushes key value pairs onto the
# output lists if there is not an overriding value set on the command line.
macro(JSON_CONFIG_PUSH_JSON_PREPROCESSOR TMP_KEY TMP_VALUE)
  # Allow command line overrides
  if(DEFINED JSON_CONFIG_CPP_${TMP_KEY})
    message(STATUS "Command line preprocessor definition: " ${TMP_KEY} " = "
                   ${JSON_CONFIG_CPP_${TMP_KEY}})
    list(APPEND JSON_CONFIG_PREPROCESSOR_NAMES ${TMP_KEY})
    list(APPEND JSON_CONFIG_PREPROCESSOR_VALUES ${JSON_CONFIG_CPP_${TMP_KEY}})
  else()
    list(APPEND JSON_CONFIG_PREPROCESSOR_NAMES ${TMP_KEY})
    list(APPEND JSON_CONFIG_PREPROCESSOR_VALUES ${TMP_VALUE})
  endif()
endmacro()

# This function takes two file names as arguments. The first argument is the
# JSON file containing the default preprocessor defines. The second file
# contains the specialisation preprocessor defines. On return the variables
# JSON_CONFIG_PREPROCESSOR_NAMES and JSON_CONFIG_PREPROCESSOR_VALUES are set.
function(JSON_CONFIG_GET DEFAULT_JSON SPEC_JSON)
  message(STATUS "-- JSON CONFIG START --")
  message(STATUS "DEFAULT_JSON: " ${DEFAULT_JSON})
  message(STATUS "SPEC_JSON: " ${SPEC_JSON})

  file(READ ${DEFAULT_JSON} DEFAULT_JSON_STRING)
  file(READ ${SPEC_JSON} SPEC_JSON_STRING)

  set(JSON_CONFIG_PREPROCESSOR_NAMES
      ""
      PARENT_SCOPE)
  set(JSON_CONFIG_PREPROCESSOR_VALUES
      ""
      PARENT_SCOPE)

  # read the specialised key-value pairs
  string(JSON NUM_SPEC_PREPROCESSOR_DEFINES LENGTH ${SPEC_JSON_STRING}
                                                   "preprocessor_defines")
  string(JSON SPEC_PREPROCESSOR_DEFINES GET ${SPEC_JSON_STRING}
         "preprocessor_defines")
  # turn the number of entries into a loop bound
  math(EXPR NUM_SPEC_PREPROCESSOR_DEFINES "${NUM_SPEC_PREPROCESSOR_DEFINES}-1")
  foreach(INDEX RANGE 0 ${NUM_SPEC_PREPROCESSOR_DEFINES})
    # turn the index into a key for the dictonary
    string(JSON TMP_KEY MEMBER ${SPEC_PREPROCESSOR_DEFINES} ${INDEX})
    string(JSON TMP_VALUE GET ${SPEC_PREPROCESSOR_DEFINES} ${TMP_KEY})
    message(STATUS "Parsed specialised preprocessor definition: " ${TMP_KEY}
                   " = " ${TMP_VALUE})
    json_config_push_json_preprocessor(${TMP_KEY} ${TMP_VALUE})
  endforeach()

  # Read the default key, value pairs
  string(JSON NUM_DEFAULT_PREPROCESSOR_DEFINES LENGTH ${DEFAULT_JSON_STRING}
                                                      "preprocessor_defines")
  string(JSON DEFAULT_PREPROCESSOR_DEFINES GET ${DEFAULT_JSON_STRING}
         "preprocessor_defines")
  # turn the number of entries into a loop bound
  math(EXPR NUM_DEFAULT_PREPROCESSOR_DEFINES
       "${NUM_DEFAULT_PREPROCESSOR_DEFINES}-1")
  foreach(INDEX RANGE 0 ${NUM_DEFAULT_PREPROCESSOR_DEFINES})
    # turn the index into a key for the dictonary
    string(JSON TMP_KEY MEMBER ${DEFAULT_PREPROCESSOR_DEFINES} ${INDEX})
    string(JSON TMP_VALUE GET ${DEFAULT_PREPROCESSOR_DEFINES} ${TMP_KEY})
    message(STATUS "Parsed default preprocessor definition: " ${TMP_KEY} " = "
                   ${TMP_VALUE})

    if(NOT ${TMP_KEY} IN_LIST JSON_CONFIG_PREPROCESSOR_NAMES)
      json_config_push_json_preprocessor(${TMP_KEY} ${TMP_VALUE})
    endif()
  endforeach()

  list(LENGTH JSON_CONFIG_PREPROCESSOR_VALUES NUM_JSON_PREPROCESSOR_DEFINES)
  math(EXPR NUM_JSON_PREPROCESSOR_DEFINES "${NUM_JSON_PREPROCESSOR_DEFINES}-1")
  foreach(INDEX RANGE 0 ${NUM_JSON_PREPROCESSOR_DEFINES})
    list(GET JSON_CONFIG_PREPROCESSOR_NAMES ${INDEX} TMP_KEY)
    list(GET JSON_CONFIG_PREPROCESSOR_VALUES ${INDEX} TMP_VALUE)
    message(STATUS "Using preprocessor definition: " ${TMP_KEY} " = "
                   ${TMP_VALUE})
  endforeach()

  # "return" the values
  set(JSON_CONFIG_PREPROCESSOR_NAMES
      ${JSON_CONFIG_PREPROCESSOR_NAMES}
      PARENT_SCOPE)
  set(JSON_CONFIG_PREPROCESSOR_VALUES
      ${JSON_CONFIG_PREPROCESSOR_VALUES}
      PARENT_SCOPE)
  message(STATUS "--  JSON CONFIG END  --")
endfunction()

# This function writes the variables in the two lists to the cmake cache for
# testing purposes.
function(JSON_CONFIG_WRITE_TO_CMAKE_CACHE)
  list(LENGTH JSON_CONFIG_PREPROCESSOR_NAMES NUM_NAMES)
  math(EXPR RANGE_NAMES "${NUM_NAMES}-1")
  foreach(INDEX RANGE 0 ${RANGE_NAMES})
    list(GET JSON_CONFIG_PREPROCESSOR_NAMES ${INDEX} TMP_KEY)
    list(GET JSON_CONFIG_PREPROCESSOR_VALUES ${INDEX} TMP_VALUE)
    set(${TMP_KEY}
        ${TMP_VALUE}
        CACHE STRING "Value from JSON config.")
  endforeach()
endfunction()
