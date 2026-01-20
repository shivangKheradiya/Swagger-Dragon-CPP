
cmake_minimum_required(VERSION 3.20)
project(Drogon LANGUAGES CXX)

find_package(Drogon CONFIG REQUIRED)

add_library(Drogon_lib SHARED
  src/TestCtrl.cc
  src/JsonCtrl.cc
  src/User.cc
)

# Public headers
target_include_directories(Drogon_lib
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(Drogon_lib PRIVATE Drogon::Drogon)

add_executable(Drogon_Demo src/main.cpp )
target_link_libraries(Drogon_Demo PRIVATE 
    Drogon::Drogon
    Drogon_lib )