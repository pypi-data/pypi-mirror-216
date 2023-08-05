# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build

# Include any dependencies generated for this target.
include CMakeFiles/amcl_bls_BLS381.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/amcl_bls_BLS381.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/amcl_bls_BLS381.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/amcl_bls_BLS381.dir/flags.make

CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o: CMakeFiles/amcl_bls_BLS381.dir/flags.make
CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o: src/bls_BLS381.c
CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o: CMakeFiles/amcl_bls_BLS381.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o"
	/usr/bin/gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o -MF CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o.d -o CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o -c /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/src/bls_BLS381.c

CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.i"
	/usr/bin/gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/src/bls_BLS381.c > CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.i

CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.s"
	/usr/bin/gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/src/bls_BLS381.c -o CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.s

# Object files for target amcl_bls_BLS381
amcl_bls_BLS381_OBJECTS = \
"CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o"

# External object files for target amcl_bls_BLS381
amcl_bls_BLS381_EXTERNAL_OBJECTS =

lib/libamcl_bls_BLS381.a: CMakeFiles/amcl_bls_BLS381.dir/src/bls_BLS381.c.o
lib/libamcl_bls_BLS381.a: CMakeFiles/amcl_bls_BLS381.dir/build.make
lib/libamcl_bls_BLS381.a: CMakeFiles/amcl_bls_BLS381.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C static library lib/libamcl_bls_BLS381.a"
	$(CMAKE_COMMAND) -P CMakeFiles/amcl_bls_BLS381.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/amcl_bls_BLS381.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/amcl_bls_BLS381.dir/build: lib/libamcl_bls_BLS381.a
.PHONY : CMakeFiles/amcl_bls_BLS381.dir/build

CMakeFiles/amcl_bls_BLS381.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/amcl_bls_BLS381.dir/cmake_clean.cmake
.PHONY : CMakeFiles/amcl_bls_BLS381.dir/clean

CMakeFiles/amcl_bls_BLS381.dir/depend:
	cd /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/CMakeFiles/amcl_bls_BLS381.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/amcl_bls_BLS381.dir/depend

