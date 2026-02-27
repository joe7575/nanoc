cmake_minimum_required(VERSION 3.10)
project(nanoc VERSION 2.3.3 LANGUAGES C)

include_directories(./src)
add_compile_options(-Wall)

add_executable(nanoc
    ./src/nc_scanner.c
    ./src/nc_compiler.c
    ./src/nc_runtime.c
    ./src/nc_memory.c
    ./src/nc_kvstore.c
    ./test/main.c
    ./src/nc.h
    ./src/nc_int.h
    ./src/nc_kvstore.h
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
