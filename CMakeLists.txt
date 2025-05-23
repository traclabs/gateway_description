cmake_minimum_required(VERSION 3.6)
project(gateway_description)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
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
    xacro
    robots
    worlds
    models
    config
    DESTINATION share/${PROJECT_NAME})

install(PROGRAMS
  scripts/move_big_arm
  scripts/move_little_arm
  DESTINATION lib/${PROJECT_NAME}
)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")

ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})

ament_package()

