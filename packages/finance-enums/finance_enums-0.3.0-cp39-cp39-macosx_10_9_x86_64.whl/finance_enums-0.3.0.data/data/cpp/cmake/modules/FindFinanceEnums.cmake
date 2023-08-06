# Find the Finance-Enums package
# FINANCE_ENUMS_INCLUDE_DIR
# FINANCE_ENUMS_FOUND
# will be set by this script

cmake_minimum_required(VERSION 3.7.2)

find_package( PythonInterp ${PYTHON_VERSION} EXACT REQUIRED )

# Find out the include path
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import finance_enums;print(finance_enums.include_path(), end='')"
          OUTPUT_VARIABLE __fe_path)
# And the version
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import finance_enums;print(finance_enums.__version__, end='')"
  OUTPUT_VARIABLE __fe_version)

find_path(FINANCE_ENUMS_INCLUDE_DIR finance-enums/finance-enums.hpp
  HINTS "${__fe_path}" "${PYTHON_INCLUDE_PATH}" NO_DEFAULT_PATH)

if(FINANCE_ENUMS_INCLUDE_DIR)
  set(FINANCE_ENUMS_FOUND 1 CACHE INTERNAL "Python finance_enums found")
endif(FINANCE_ENUMS_INCLUDE_DIR)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(FinanceEnums REQUIRED_VARS FINANCE_ENUMS_INCLUDE_DIR
                                        VERSION_VAR __fe_version)
