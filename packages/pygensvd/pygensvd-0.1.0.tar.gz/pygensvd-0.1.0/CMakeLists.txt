# Set minimum cmake version
cmake_minimum_required(VERSION 3.26)

# set c standard to c17
set(CMAKE_C_STANDARD 17)

# set project name and languages
project(omni LANGUAGES C)

# find python 3.10 > 3.7
exec_program(${PYTHON_EXECUTABLE} ARGS "-c \"import sys; print('.'.join(map(str, sys.version_info[:2])))\"" OUTPUT_VARIABLE PYTHON_VERSION)
find_package(Python ${PYTHON_VERSION} EXACT REQUIRED OPTIONAL_COMPONENTS NumPy)

# if we couldn't find numpy with FindPython then try using the numpy module instead
if(NOT Python_NumPy_FOUND)
    message(STATUS "Could not find NumPy with FindPython, trying to find it with the numpy module instead.")
    exec_program(${PYTHON_EXECUTABLE} ARGS "-c \"import numpy; print(numpy.get_include())\"" OUTPUT_VARIABLE Python_NumPy_INCLUDE_DIRS)
    message(STATUS "Found NumPy include directory: ${Python_NumPy_INCLUDE_DIRS}")
endif()

# find LAPACK and BLAS (Use static linkage)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR})

# search for openblas first
set(BLA_VENDOR OpenBLAS)
find_package(BLAS)

if(BLAS_FOUND)
    find_package(LAPACK REQUIRED)
    find_package(LAPACKE REQUIRED)
endif()

# then search for everything else
# NO GUARANTEE THAT THIS WILL WORK!
if(NOT BLAS_FOUND)
    find_package(BLAS REQUIRED)
    find_package(LAPACK REQUIRED)
    find_package(LAPACKE REQUIRED)
endif()

# add pygensvd library
Python_add_library(
    _gsvd
    MODULE
    WITH_SOABI
    src/_gsvd.c
)
target_include_directories(
    _gsvd
    PRIVATE
    ${LAPACKE_INCLUDE_DIRS}
    ${Python_NumPy_INCLUDE_DIRS}
)
target_link_libraries(
    _gsvd
    PRIVATE
    ${LAPACKE_LIBRARIES}
)
target_compile_definitions(
    _gsvd
    PRIVATE
    USE_LAPACK
)

# install library
install(
    TARGETS _gsvd
    LIBRARY DESTINATION lib
)
