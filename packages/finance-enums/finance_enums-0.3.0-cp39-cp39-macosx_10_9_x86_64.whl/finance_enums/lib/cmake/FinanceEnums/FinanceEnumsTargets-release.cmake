#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "FinanceEnums::finance-enums" for configuration "Release"
set_property(TARGET FinanceEnums::finance-enums APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(FinanceEnums::finance-enums PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libfinance-enums.so"
  IMPORTED_SONAME_RELEASE "@rpath/libfinance-enums.so"
  )

list(APPEND _cmake_import_check_targets FinanceEnums::finance-enums )
list(APPEND _cmake_import_check_files_for_FinanceEnums::finance-enums "${_IMPORT_PREFIX}/lib/libfinance-enums.so" )

# Import target "FinanceEnums::finance-enums-static" for configuration "Release"
set_property(TARGET FinanceEnums::finance-enums-static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(FinanceEnums::finance-enums-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libfinance-enums-static.a"
  )

list(APPEND _cmake_import_check_targets FinanceEnums::finance-enums-static )
list(APPEND _cmake_import_check_files_for_FinanceEnums::finance-enums-static "${_IMPORT_PREFIX}/lib/libfinance-enums-static.a" )

# Import target "FinanceEnums::extension" for configuration "Release"
set_property(TARGET FinanceEnums::extension APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(FinanceEnums::extension PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELEASE ""
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./extension.cpython-39-darwin.so"
  IMPORTED_NO_SONAME_RELEASE "TRUE"
  )

list(APPEND _cmake_import_check_targets FinanceEnums::extension )
list(APPEND _cmake_import_check_files_for_FinanceEnums::extension "${_IMPORT_PREFIX}/./extension.cpython-39-darwin.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
