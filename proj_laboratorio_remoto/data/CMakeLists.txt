cmake_minimum_required(VERSION 3.0)
project(vri-slam-lama)

add_executable(data src/main.c)
target_link_libraries(data ufr)