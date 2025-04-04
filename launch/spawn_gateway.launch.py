from http.server import executable
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.substitutions import TextSubstitution, PathJoinSubstitution, LaunchConfiguration, Command
from launch_ros.actions import Node, SetParameter
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit, OnExecutionComplete
import os
from os import environ

from ament_index_python.packages import get_package_share_directory

import xacro


def generate_launch_description():

    # URDF
    gateway_path = get_package_share_directory('gateway_description')
    gateway_urdf = os.path.join(gateway_path, 'robots', 'gateway_body.urdf.xacro')
    gateway_doc = xacro.process_file(gateway_urdf)
    gateway_urdf_content = gateway_doc.toxml()

    # Robot state publisher
    gateway_robot_state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': gateway_urdf_content},
            {"use_sim_time": True},
            # {'frame_prefix': 'gateway/'},
            ],
            namespace="gateway",
    )

    # gateway_static_pub = Node(
    #     name="gateway_static_publisher",
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     output="screen",
    #     arguments=["0", "0", "0", # XYZ
    #                "0", "0", "0", "1", # XYZW
    #                "world",
    #                "gateway/world"]
    # )

    # Spawn in Gazebo
    gateway_spawn = Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn',
            output='screen',
            arguments=[
              "-string", 
              gateway_urdf_content,
              "-name", 'gateway',
              "-allow_renaming", "true",
            ],
            namespace="gateway"
        )


    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),
        gateway_robot_state_publisher,
        gateway_spawn,
        # gateway_static_pub
    ])
