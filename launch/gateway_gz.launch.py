from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node, SetParameter
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit

from ament_index_python.packages import get_package_share_directory

import os
import xacro


def generate_launch_description():

  # Gazebo setup
  sim_resource_path = os.pathsep.join([
    os.environ.get("GZ_SIM_RESOURCE_PATH", default=""),
    os.path.join(get_package_share_directory("gateway_description"), "models" )
  ])
  env_gz_sim = SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", sim_resource_path)

  # World
  cislunar_sdf = PathJoinSubstitution([
    FindPackageShare("gateway_description"), "worlds", "cislunar.sdf"
  ])

  # Launch gazebo world
  gz_launch = IncludeLaunchDescription(
    PathJoinSubstitution([FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]),
    launch_arguments=[
      ("gz_args", [
          cislunar_sdf,
          " -r",
          " -v 4"
      ])
    ]
  )

  # Spawn Gateway
  gateway = IncludeLaunchDescription(
    PathJoinSubstitution([
      FindPackageShare("gateway_description"), "launch", "spawn_gateway.launch.py"
    ])
  )

  # Spawn big arm and its controllers
  big_arm = IncludeLaunchDescription(
    PathJoinSubstitution([
      FindPackageShare("gateway_description"), "launch", "spawn_big_arm.launch.py"
    ])
  )

  # Spawn little arm and its controllers
  little_arm = IncludeLaunchDescription(
    PathJoinSubstitution([
      FindPackageShare("gateway_description"), "launch", "spawn_little_arm.launch.py"
    ])
  )

  # Make the /clock topic available in ROS
  gz_sim_bridge = Node(
    package="ros_gz_bridge",
    executable="parameter_bridge",
    arguments=[
      "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
    ],
    output="screen",
  )

  return LaunchDescription([
    SetParameter(name="use_sim_time", value=True),
    env_gz_sim,
    gz_launch,
    gateway,
    big_arm,
    little_arm,
    gz_sim_bridge
  ])
