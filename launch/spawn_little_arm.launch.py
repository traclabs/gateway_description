from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch_ros.actions import Node, SetParameter
from launch.event_handlers import OnProcessExit

from ament_index_python.packages import get_package_share_directory

import os
import xacro


def generate_launch_description():

  # URDF
  little_arm_urdf = os.path.join(get_package_share_directory("gateway_description"), "robots", "little_arm.urdf.xacro")
  little_arm_doc = xacro.process_file(little_arm_urdf, mappings={"parent_link" : "world"})
  little_arm_urdf_content = little_arm_doc.toxml()

  # Robot state publisher
  little_arm_robot_state_publisher = Node(
    package="robot_state_publisher",
    executable="robot_state_publisher",
    name="robot_state_publisher",
    output="screen",
    parameters=[
      {"robot_description": little_arm_urdf_content},
      {"use_sim_time": True},
    ],
    namespace="little_arm",
  )

  # Spawn in Gazebo
  little_arm_spawn = Node(
    package="ros_gz_sim",
    executable="create",
    name="spawn",
    output="screen",
    arguments=[
      "-string",
      little_arm_urdf_content,
      "-name", "little_arm",
      "-allow_renaming", "true",
    ],
    namespace="little_arm"
  )

  # Test motion with services
  little_arm_move = Node(
    package="gateway_description",
    executable="move_little_arm",
    namespace="little_arm",
    output="screen"
  )

  # Control
  little_arm_joint_state_broadcaster_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=["joint_state_broadcaster", "--controller-manager", "/little_arm/controller_manager"],
    name="start_joint_state_broadcaster",
    namespace="little_arm",
    output="screen",
  )

  little_arm_joint_controller_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=["joint_trajectory_controller", "-c", "/little_arm/controller_manager"],
    name="start_joint_trajectory_controller",
    namespace="little_arm",
    output="screen",
  )

  return LaunchDescription([
    SetParameter(name="use_sim_time", value=True),
    little_arm_robot_state_publisher,
    little_arm_spawn,
    little_arm_move,
    # FIXME sometimes the arm fails to spawn and things have to be restarted
    # @sethgee tried using a couple of different events but no others behaved like OnProcessExit
    RegisterEventHandler(
      OnProcessExit(
        target_action=little_arm_spawn,
        on_exit=[little_arm_joint_state_broadcaster_spawner],
      )
    ),
    RegisterEventHandler(
      OnProcessExit(
        target_action=little_arm_joint_state_broadcaster_spawner,
        on_exit=[little_arm_joint_controller_spawner],
      )
    )
  ])
