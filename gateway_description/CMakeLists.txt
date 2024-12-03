cmake_minimum_required(VERSION 3.5)
project(gateway_description)


find_package(
  catkin REQUIRED COMPONENTS
  joint_state_publisher
  )

catkin_package(
  #INCLUDE_DIRS include
  #LIBRARIES yumi_executors
  CATKIN_DEPENDS
  #joint_state_publisher
)


install(DIRECTORY
    launch
    meshes
    rviz
    urdf
    DESTINATION  ${CATKIN_PACKAGE_SHARE_DESTINATION})


