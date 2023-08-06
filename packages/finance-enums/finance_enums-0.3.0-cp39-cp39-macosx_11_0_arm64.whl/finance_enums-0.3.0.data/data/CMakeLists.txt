###############################################################################################################
# Project Configuration #
#########################
cmake_minimum_required(VERSION 3.20.0)
project(finance-enums)
set(CMAKE_CXX_STANDARD 20)
set(PROJECT_VERSION "0.3.0")

###############################################################################################################
# CMake Dependencies #
######################
include(CheckCCompilerFlag)

###############################################################################################################
# CMake Policies #
##################
# option() should use new make behavior wrt variable clobbering
cmake_policy (SET CMP0077 NEW)

# Allow dep roots from env vars
cmake_policy (SET CMP0074 NEW)

# Set CMP0094 to NEW - find the first version that matches constraints,
# instead of the latest version installed
cmake_policy(SET CMP0094 NEW)

###############################################################################################################
# Environemtn #
###############
if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(WIN32 ON)
    set(MACOS OFF)
    set(LINUX OFF)
elseif(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set(WIN32 OFF)
    set(MACOS ON)
    set(LINUX OFF)
else()
    set(WIN32 OFF)
    set(MACOS OFF)
    set(LINUX ON)
endif()


###############################################################################################################
# Paths #
#########
# Custom CMake modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_SOURCE_DIR}/cpp/cmake/modules")

# Base includes
include_directories ("${CMAKE_SOURCE_DIR}/cpp/include")

###############################################################################################################
# Build Configuration #
#######################
find_package (Color)

if (NOT DEFINED CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "3.9" CACHE STRING "Release/Debug build")
endif()
if (NOT DEFINED PYTHON_VERSION)
  set(PYTHON_VERSION "3.9" CACHE STRING "Python version to build against")
endif()
option(BUILD_PYTHON "Build Python bindings" ON)
option(USE_CCACHE "Use CCache for build" OFF)
option(STATIC_PYTHON "Build against static python (no libraries)" OFF)
option(PYODIDE "Build against pyodide" OFF)

# CCache setup
if(USE_CCACHE)
    set(CMAKE_C_COMPILE_LAUNCHER ccache)
    set(CMAKE_CXX_COMPILER_LAUNCHER ccache)
endif()

if(MACOS)
    # fix for threads on osx
    # assume built-in pthreads on MacOS
    set(CMAKE_THREAD_LIBS_INIT "-lpthread")
    set(CMAKE_HAVE_THREADS_LIBRARY 1)
    set(CMAKE_USE_WIN32_THREADS_INIT 0)
    set(CMAKE_USE_PTHREADS_INIT 1)
    set(THREADS_PREFER_PTHREAD_FLAG ON)

    # don't link against build python
    # https://blog.tim-smith.us/2015/09/python-extension-modules-os-x/
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -undefined dynamic_lookup")

    # Support cross build
    check_c_compiler_flag("-arch x86_64" x86_64Supported)
    check_c_compiler_flag("-arch arm64" arm64Supported)

    if(x86_64Supported AND arm64Supported)
        set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64" CACHE STRING "Build universal architecture for OSX" FORCE)
    elseif(x86_64Supported)
        set(CMAKE_REQUIRED_LINK_OPTIONS "-arch;x86_64")
        set(CMAKE_OSX_ARCHITECTURES "x86_64" CACHE STRING "Build universal architecture for OSX" FORCE)
    elseif(arm64Supported)
        set(CMAKE_REQUIRED_LINK_OPTIONS "-arch;arm64")
        set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Build universal architecture for OSX" FORCE)
    endif()
endif()

if(WIN32)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

###############################################################################################################
# RPath #
#########
if(NOT WIN32)
    set(CMAKE_SHARED_LIBRARY_SUFFIX .so)

    # Look for the binary using @loader_path (relative to binary location)
    set(CMAKE_MACOSX_RPATH TRUE)
    set(CMAKE_SKIP_BUILD_RPATH FALSE)
    set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

    # module_origin_path is the location of the binary
    if(MACOS)
        set(module_origin_path "@loader_path")
    else()
        set(module_origin_path "\$ORIGIN")
    endif()
else()
    set(CMAKE_SHARED_LIBRARY_PREFIX "lib")
    set(CMAKE_STATIC_LIBRARY_PREFIX "lib")
endif()

###############################################################################################################
# Flags #
#########
# Compiler version flags
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++2a")
endif()

# Optimization Flags
if(WIN32)
    if(CMAKE_BUILD_TYPE_LOWER STREQUAL debug)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /DEBUG /Z7 /Zi /Zc:preprocessor")
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /O2 /Zc:preprocessor ")
    endif()
else()
    if(CMAKE_BUILD_TYPE_LOWER STREQUAL debug)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g3")
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -g0")
    endif()
endif()

# Other Flags
if(WIN32)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc /MP /bigobj")
    foreach(warning 4244 4251 4267 4275 4290 4786 4305 4996)
        SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd${warning}")
    endforeach(warning)
    add_compile_definitions(WIN32 _WIN32)
	  if (MSVC_VERSION GREATER_EQUAL 1920)
		    add_compile_options(/d2FH4-) # Because we don't want to link against VCRUNTIME140_1.dll (see https://cibuildwheel.readthedocs.io/en/stable/faq/#importerror-dll-load-failed-the-specific-module-could-not-be-found-error-on-windows)
	  endif()
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-macro-redefined")
endif()

###############################################################################################################
# Python #
##########
if(BUILD_PYTHON AND STATIC_PYTHON AND LINUX)
    message("${Red}Manylinux build has no python shared libraries${ColorReset}")
    find_package(Python ${PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter OPTIONAL_COMPONENTS Development.Module)
elseif(BUILD_PYTHON)
    message("${Cyan}Use python shared libraries${ColorReset}")
    if(PYODIDE)
        find_package(Python ${PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter OPTIONAL_COMPONENTS Development.Module)
    else()
        find_package(Python ${PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter Development.Module)
    endif()
    link_directories(${Python_LIBRARY_DIRS})
endif()

if(BUILD_PYTHON)
  message("${Cyan}Using Python ${Python_VERSION}, \nPython_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}, \nPython_LIBRARIES: ${Python_LIBRARIES}, \nPython_EXECUTABLE: ${Python_EXECUTABLE} ${ColorReset}")
  include_directories(${Python_INCLUDE_DIRS})
  add_definitions(-DBUILD_PYTHON)
endif()

###############################################################################################################
# Messages #
############
string(TOLOWER "${CMAKE_BUILD_TYPE}" CMAKE_BUILD_TYPE_LOWER)

if(CMAKE_BUILD_TYPE_LOWER STREQUAL debug)
    message("${Red}Building DEBUG${ColorReset}")
else()
    message("${Cyan}Building RELEASE${ColorReset}")
endif()

###############################################################################################################
# Configure asset output directories #
######################################
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

###############################################################################################################
# Standalone C++ Binary #
#########################
set(
    PROJECT_SRCS
    "${PROJECT_SOURCE_DIR}/cpp/src/finance-enums.cpp"
)

add_library(finance-enums SHARED ${PROJECT_SRCS})
add_library(finance-enums-static STATIC ${PROJECT_SRCS})

# export symbols
if(WIN32)
    target_compile_definitions(finance-enums PRIVATE LIB_EXPORTS)
    target_compile_definitions(finance-enums-static PRIVATE LIB_EXPORTS)
endif()

# install standalone library inside package
install(TARGETS finance-enums EXPORT FinanceEnums LIBRARY DESTINATION lib)
install(TARGETS finance-enums-static EXPORT FinanceEnums LIBRARY DESTINATION lib)

# Install headers inside package
install(DIRECTORY "${PROJECT_SOURCE_DIR}/cpp/include/" DESTINATION include)

###############################################################################################################
# Pybind Extension #
####################
if(BUILD_PYTHON)
  # Find Numpy
  find_package(NumPy REQUIRED)

  # Find PyBind11
  find_package(pybind11 REQUIRED)
  include_directories(${pybind11_INCLUDE_DIR})

  # Extension
  pybind11_add_module(extension MODULE "${PROJECT_SOURCE_DIR}/cpp/src/python/extension.cpp")

  # Link to standalone library
  target_link_libraries(extension PUBLIC finance-enums)
  set_property(TARGET extension PROPERTY INSTALL_RPATH "${module_origin_path}/lib")

  # install in python module
  install(TARGETS extension EXPORT FinanceEnums LIBRARY DESTINATION .)
endif()

###############################################################################################################
# C++ Discoverability #
#######################

# Generate cmake config files for reuse by downstream packages
include(CMakePackageConfigHelpers)

# generate the config file that is includes the exports
configure_package_config_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cpp/cmake/config/FinanceEnumsConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/FinanceEnumsConfig.cmake
  INSTALL_DESTINATION cmake
)
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/FinanceEnumsConfigVersion.cmake
  VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}"
  COMPATIBILITY SameMajorVersion
)

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cpp/cmake/config/FinanceEnums.pc.in
  "${CMAKE_CURRENT_BINARY_DIR}/FinanceEnums.pc"
  @ONLY)

# install the configuration file
install(EXPORT FinanceEnums
    FILE FinanceEnumsTargets.cmake
    NAMESPACE FinanceEnums::
    DESTINATION lib/cmake/FinanceEnums
)
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/FinanceEnumsConfig.cmake ${CMAKE_CURRENT_BINARY_DIR}/FinanceEnumsConfigVersion.cmake
  DESTINATION lib/cmake/FinanceEnums
)

# install the configuration file
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/FinanceEnums.pc
  DESTINATION lib/pkgconfig)

