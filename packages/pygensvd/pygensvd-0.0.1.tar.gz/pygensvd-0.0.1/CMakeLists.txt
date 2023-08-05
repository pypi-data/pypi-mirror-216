# Set minimum cmake version
cmake_minimum_required(VERSION 3.26)

# set c standard to c17
set(CMAKE_C_STANDARD 17)

# set project name and languages
project(omni LANGUAGES C)

# find python 3.10 > 3.7
exec_program(${PYTHON_EXECUTABLE} ARGS "-c \"import sys; print('.'.join(map(str, sys.version_info[:2])))\"" OUTPUT_VARIABLE PYTHON_VERSION)
find_package(Python ${PYTHON_VERSION} EXACT REQUIRED NumPy)

# find LAPACK and BLAS (Use static linkage)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR})

# if we didn't find MKL
# then search for OpenBLAS
set(BLA_VENDOR OpenBLAS)
find_package(BLAS)

if(BLAS_FOUND)
    find_package(LAPACK REQUIRED)
    find_package(LAPACKE REQUIRED)
endif()

# then search for everything else
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
target_link_libraries(
    _gsvd
    PRIVATE
    Python::NumPy
)

# check if this is an mkl library
# THIS IS CURRENTLY NOT WORKING
if(BLAS_LIBRARIES MATCHES "(mkl)")
    if(NOT DEFINED ENV{MKLROOT})
        message(
            FATAL_ERROR
            "CMake detected MKL for a BLAS/LAPACK backend, but MKLROOT is undefined! \
            Check that your MKL environment is setup correctly."
        )
    endif()

    set(MKLROOT $ENV{MKLROOT})
    set(MKL_INCLUDE_DIRECTORY ${MKLROOT}/include)
    target_compile_definitions(
        _gsvd
        PRIVATE
        USE_MKL
    )
    target_include_directories(
        _gsvd
        PRIVATE
        ${MKL_INCLUDE_DIRECTORY}
    )
else()
    target_compile_definitions(
        _gsvd
        PRIVATE
        USE_LAPACK
    )
endif()

target_include_directories(
    _gsvd
    PRIVATE
    ${LAPACKE_INCLUDE_DIRS}
)
target_link_libraries(
    _gsvd
    PRIVATE
    ${LAPACKE_LIBRARIES}
)

# install library
install(
    TARGETS _gsvd
    LIBRARY DESTINATION lib
)
