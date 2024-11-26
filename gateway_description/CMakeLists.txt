cmake_minimum_required(VERSION 3.5)
project(gateway_description)

find_package(ament_cmake REQUIRED)
find_package(rviz_rendering REQUIRED)

# Adds shallow folders containing ogre_media such as meshes and scripts to Rviz
# so that they can be found at runtime. Requires rviz_rendering.
register_rviz_ogre_media_exports(
    DIRECTORIES
    "meshes"
#    "meshes/ng_halo"
  )

install(DIRECTORY
    launch
    meshes
    rviz
    urdf
    DESTINATION share/${PROJECT_NAME})

ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})

ament_package()
