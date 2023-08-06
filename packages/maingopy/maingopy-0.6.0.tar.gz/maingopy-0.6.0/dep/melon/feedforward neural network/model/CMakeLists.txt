cmake_minimum_required(VERSION 3.8 FATAL_ERROR)

message("Checking files for ffNet.")
project(ffNet CXX)

add_library(ffnet STATIC 
    ${PROJECT_SOURCE_DIR}/src/AnnParser.cpp
    ${PROJECT_SOURCE_DIR}/src/AnnParserCSV.cpp
    ${PROJECT_SOURCE_DIR}/src/AnnParserXML.cpp
)
target_include_directories(ffnet PUBLIC ${PROJECT_SOURCE_DIR}/inc)
set_target_properties(ffnet PROPERTIES CXX_STANDARD 17)

add_library(tinyxml2 STATIC
    ${PROJECT_SOURCE_DIR}/dep/tinyxml2/src/tinyxml2.cpp
)
target_include_directories(tinyxml2 PUBLIC ${PROJECT_SOURCE_DIR}/dep/tinyxml2/inc)
set_target_properties(tinyxml2 PROPERTIES CXX_STANDARD 14)

target_link_libraries(ffnet mcpp tinyxml2 meloncommon)

