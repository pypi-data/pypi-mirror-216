#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fortran_stdlib::fortran_stdlib" for configuration "Release"
set_property(TARGET fortran_stdlib::fortran_stdlib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fortran_stdlib::fortran_stdlib PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "Fortran"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libfortran_stdlib.a"
  )

list(APPEND _cmake_import_check_targets fortran_stdlib::fortran_stdlib )
list(APPEND _cmake_import_check_files_for_fortran_stdlib::fortran_stdlib "${_IMPORT_PREFIX}/lib64/libfortran_stdlib.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
