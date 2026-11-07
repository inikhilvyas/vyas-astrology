cmake_minimum_required(VERSION 3.16)
project(VYASQt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 COMPONENTS Core Quick REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

add_executable(${PROJECT_NAME}
    src/main.cpp
    src/qml/main.qml
)

target_link_libraries(${PROJECT_NAME} PRIVATE Qt6::Core Qt6::Quick pybind11::module)

# Placeholder for bindings (built into the app)
add_library(vyas_bindings SHARED src/bindings/vyas_bindings.cpp)
target_include_directories(vyas_bindings PRIVATE ${Python3_INCLUDE_DIRS})
target_link_libraries(vyas_bindings PRIVATE ${Python3_LIBRARIES})

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)
