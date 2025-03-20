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
    big_arm_urdf = os.path.join(gateway_path, 'robots', 'big_arm.urdf.xacro')
    big_arm_doc = xacro.process_file(big_arm_urdf, mappings={'parent_link' : 'world'})
    big_arm_urdf_content = big_arm_doc.toxml()

    # Robot state publisher
    big_arm_robot_state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': big_arm_urdf_content},
            {"use_sim_time": True},
#            {'frame_prefix': 'big_arm/'},
            ],
            namespace="big_arm",
    )
    
    # Spawn in Gazebo
    big_arm_spawn = Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn',
            output='screen',
            arguments=[
              "-string", 
              big_arm_urdf_content, 
              "-name", 'big_arm', 
              "-allow_renaming", "true",
            ],
            namespace="big_arm" 
        )      

    # Test motion with services
    big_arm_move = Node(
        package="gateway_description",
        executable="move_big_arm",
        namespace="big_arm",
        output='screen'
    )


    # Control
    big_arm_joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/big_arm/controller_manager"],
        name="start_joint_state_broadcaster",
        namespace="big_arm",
        output='screen'
    )
        
    big_arm_joint_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "-c", "/big_arm/controller_manager"],
        name="start_joint_trajectory_controller",
        namespace="big_arm",
        output='screen',
    )
    
    image_bridge = Node(
            package='ros_gz_image',
            executable='image_bridge',
            arguments=['/image_raw', '/image_raw'],
            output='screen')
    
    
    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),    
        big_arm_robot_state_publisher,
        big_arm_spawn,
        big_arm_move,
        image_bridge,
        RegisterEventHandler(
            OnProcessExit(
                target_action=big_arm_spawn,
                on_exit=[big_arm_joint_state_broadcaster_spawner],
            )
        ),
        RegisterEventHandler(
            OnProcessExit(
                target_action=big_arm_joint_state_broadcaster_spawner,
                on_exit=[big_arm_joint_controller_spawner],
            )
        )
    ])    
    
