cmake_minimum_required(VERSION 3.16)
project(fast_succinct_trie_build VERSION 0.1.0 LANGUAGES CXX)

if (NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
  # set(CMAKE_BUILD_TYPE Debug)
endif ()

set(GCC_WARNINGS "-Wall")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -pedantic -std=c++20")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG -march=native -DNDEBUG -O2 -g")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fsanitize=address -fno-omit-frame-pointer -O0 -g -DDEBUG -march=native")

find_package(Boost REQUIRED)

message(STATUS "BUILD_TYPE is ${CMAKE_BUILD_TYPE}")
message(STATUS "CXX_FLAGS are ${CMAKE_CXX_FLAGS}")
message(STATUS "CXX_FLAGS_DEBUG are ${CMAKE_CXX_FLAGS_DEBUG}")
message(STATUS "CXX_FLAGS_RELEASE are ${CMAKE_CXX_FLAGS_RELEASE}")

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../include)

set(COCO_TRIE_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../CoCo-trie)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-function -mpopcnt -msse4 -mbmi2")
set(SCRIPT_PATH "${COCO_TRIE_SOURCE_DIR}/lib/adapted_code/move.sh")
set(WORKING_DIR "${COCO_TRIE_SOURCE_DIR}")
set(SUCCINCT_SOURCE_DIR ${COCO_TRIE_SOURCE_DIR}/lib/ds2i/succinct)
configure_file(
  ${SUCCINCT_SOURCE_DIR}/succinct_config.hpp.in
  ${SUCCINCT_SOURCE_DIR}/succinct_config.hpp)
configure_file(
        ${COCO_TRIE_SOURCE_DIR}/lib/ds2i/ds2i_config.hpp.in
        ${COCO_TRIE_SOURCE_DIR}/lib/ds2i/ds2i_config.hpp
        ESCAPE_QUOTES)
add_custom_target(MoveConfig ALL DEPENDS ${SUCCINCT_SOURCE_DIR}/intrinsics.hpp)
add_custom_command(
    TARGET MoveConfig
    WORKING_DIRECTORY ${WORKING_DIR}
    COMMAND ${CMAKE_COMMAND} -E echo "Running the shell script..."
    COMMAND pwd
    COMMAND sh ${SCRIPT_PATH}
    COMMENT "Running shell script before building bench_coco"
)
add_subdirectory(${COCO_TRIE_SOURCE_DIR}/lib/ds2i/succinct ./succinct)
add_subdirectory(${COCO_TRIE_SOURCE_DIR}/lib/sdsl-lite ./sdsl-lite)
add_executable(bench_coco ../bench.cpp ${COCO_TRIE_SOURCES})
target_link_libraries(bench_coco sdsl succinct ${Boost_LIBRARIES})
target_include_directories(bench_coco PUBLIC ${COCO_TRIE_SOURCE_DIR}/include
    ${COCO_TRIE_SOURCE_DIR}/lib/sdsl-lite/include
    ${COCO_TRIE_SOURCE_DIR}/lib/sux
    ${COCO_TRIE_SOURCE_DIR}/lib/ds2i)
add_dependencies(bench_coco MoveConfig)
set_target_properties(bench_coco PROPERTIES COMPILE_DEFINITIONS "USE_COCO_TRIE")
#target_compile_definitions(bench_coco PRIVATE BIG_ALPHABET)
