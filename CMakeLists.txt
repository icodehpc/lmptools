cmake_minimum_required(VERSION 3.17)
project(lmptools)

set(CMAKE_CXX_STANDARD 20)

find_package(Python COMPONENTS Development Interpreter)


include_directories(lmptools/_lib/include)
include_directories(${Python_INCLUDE_DIRS})

FILE(GLOB SRCS lmptools/_lib/src/*.cpp)

add_library(lmptools SHARED  ${SRCS})

set_target_properties(
	lmptools
	PROPERTIES
	PREFIX ""
	OUTPUT_NAME "lmptools"
	LINKER_LANGUAGE CXX)

