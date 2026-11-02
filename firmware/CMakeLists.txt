cmake_minimum_required(VERSION 3.25)

project(somnasound_firmware LANGUAGES C CXX ASM)

set(CMAKE_C_STANDARD 17)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXECUTABLE_SUFFIX ".elf")

add_executable(somnasound_firmware
  src/main.cpp
)

target_include_directories(somnasound_firmware PRIVATE include)

# Board-specific startup, linker, and peripheral sources belong in boards/<target>/.
# Select a cross-compilation toolchain via CMAKE_TOOLCHAIN_FILE at configure time.
