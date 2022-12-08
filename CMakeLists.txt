cmake_minimum_required(VERSION 3.17)
project(lmptools)

file(READ "VERSION" LMPTOOLS_VERSION)
string(STRIP "${LMPTOOLS_VERSION}" LMPTOOLS_VERSION)
message("Version will be ${LMPTOOLS_VERSION}")

set(CMAKE_CXX_COMPILER g++)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "-Werror -pedantic -Wall")

include_directories(cpp/include)
file(GLOB SRCS cpp/src/*.cpp)


#set(CMAKE_CXX_CLANG_TIDY clang-tidy; -header-filter=.;
#	-checks=*,-llvmlibc-restrict-system-libc-headers,-fuchsia-overloaded-operator;
#	--warnings-as-errors=*;)

add_library(lmptools SHARED  ${SRCS})
set_target_properties(lmptools PROPERTIES VERSION ${LMPTOOLS_VERSION})
set_target_properties(lmptools PROPERTIES SOVERSION 1)


# Enable testing
enable_testing()

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# Glob all tests
file(GLOB ALLTESTS tests/cpp/*.cpp)

add_executable(lmptoolstests ${ALLTESTS})
target_link_libraries(lmptoolstests GTest::gtest GTest::gtest_main)
add_test(LMPTOOLSTestSuite lmptoolstests)

