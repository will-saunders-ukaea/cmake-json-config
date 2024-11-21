# TODO
function(JSON_CONFIG_GET DEFAULT_JSON SPEC_JSON)
  message(STATUS "-- JSON CONFIG START --")
  message(STATUS "DEFAULT_JSON: " ${DEFAULT_JSON})
  message(STATUS "SPEC_JSON: " ${SPEC_JSON})

  file(READ ${DEFAULT_JSON} DEFAULT_JSON_STRING)
  file(READ ${SPEC_JSON} SPEC_JSON_STRING)

  set(JSON_PREPROCESSOR_NAMES "")
  set(JSON_PREPROCESSOR_VALUES "")

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
    list(APPEND JSON_PREPROCESSOR_NAMES ${TMP_KEY})
    list(APPEND JSON_PREPROCESSOR_VALUES ${TMP_VALUE})
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

    if(NOT ${TMP_KEY} IN_LIST JSON_PREPROCESSOR_NAMES)
      list(APPEND JSON_PREPROCESSOR_NAMES ${TMP_KEY})
      list(APPEND JSON_PREPROCESSOR_VALUES ${TMP_VALUE})
    endif()
  endforeach()

  list(LENGTH JSON_PREPROCESSOR_VALUES NUM_JSON_PREPROCESSOR_DEFINES)
  math(EXPR NUM_JSON_PREPROCESSOR_DEFINES "${NUM_JSON_PREPROCESSOR_DEFINES}-1")
  foreach(INDEX RANGE 0 ${NUM_JSON_PREPROCESSOR_DEFINES})
    list(GET JSON_PREPROCESSOR_NAMES ${INDEX} TMP_KEY)
    list(GET JSON_PREPROCESSOR_VALUES ${INDEX} TMP_VALUE)
    message(STATUS "Using preprocessor definition: " ${TMP_KEY} " = "
                   ${TMP_VALUE})
  endforeach()

  message(STATUS "--  JSON CONFIG END  --")
endfunction()
