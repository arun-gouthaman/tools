cmake_minimum_required(VERSION 3.2 FATAL_ERROR)
include(CMakePrintHelpers)
project( USD_Ref )

set(PYTHON_DIR "C:/Users/Arun/AppData/Local/ov/pkg/usdview-0.22.8/python37/")
set(USD_DIR "C:/my_files/USD/Build/")

set( LIBRARY_NAME USD_Ref )

set(INCLUDE_DIR ${PYTHON_DIR}include ${USD_DIR}include)

# cmake_print_variables(INCLUDE_DIR)


file(GLOB SRC_FILES
    "${CMAKE_CURRENT_LIST_DIR}/src/*"
)

cmake_print_variables(SRC_FILES)

add_executable(
    ${LIBRARY_NAME}
    ${SRC_FILES}
)

include_directories(
    ${INCLUDE_DIR}
)

target_link_libraries( 
    ${LIBRARY_NAME}
    ${PYTHON_DIR}libs/python37.lib
    ${USD_DIR}lib/*.lib
)

set_target_properties(
    ${LIBRARY_NAME}
    PROPERTIES
    CXX_STANDARD 17
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    VS_CONFIGURATION_TYPE "Application"
    CMAKE_CONFIGURATION_TYPES "RelWithDebInfo"
    )

add_compile_definitions(NOMINMAX)