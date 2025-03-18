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

    # Gazebo setup
    gateway_path = get_package_share_directory('gateway_description')
    
    sim_resource_path = os.pathsep.join(
            [
                environ.get("GZ_SIM_RESOURCE_PATH", default=""),
                os.path.join( gateway_path, 'models' )
            ]
    )
    env_gz_sim = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', sim_resource_path)

    # World
    cislunar_sdf = os.path.join(gateway_path, 'worlds', 'cislunar.sdf')

    # Launch gazebo world
    gz_launch = IncludeLaunchDescription(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py']),
            launch_arguments = [
               ('gz_args', [
                   cislunar_sdf,
                   ' -r',
                   ' -v 4' 
               ])
            ]   
    )

    # Gateway body
    gateway_urdf = os.path.join(gateway_path, 'robots', 'gateway_body.urdf.xacro')
    gateway_doc = xacro.process_file(gateway_urdf)
    gateway_urdf_content = gateway_doc.toxml()

    gateway_spawn = Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_gateway',
            output='screen',
            arguments=[
              "-string", 
              gateway_urdf_content, 
              "-name", 'gateway', 
              "-allow_renaming", "true",
          ] 
        ) 

    # Big arm
    big_arm_urdf = os.path.join(gateway_path, 'robots', 'big_arm.urdf.xacro')
    big_arm_doc = xacro.process_file(big_arm_urdf, mappings={'parent_link' : 'world'}) #, 'rpy': '3.1416 0.0 0.0'})
    big_arm_urdf_content = big_arm_doc.toxml()


    #run_move_arm = Node(
    #    package="canadarm",
    #    executable="move_arm",
    #    output='screen'
    #)


    big_arm_robot_state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': big_arm_urdf_content},
            {"use_sim_time": True}])
    
    big_arm_spawn = Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_big_arm',
            output='screen',
            arguments=[
              "-string", 
              big_arm_urdf_content, 
              "-name", 'big_arm', 
              "-allow_renaming", "true",
          ] 
        )      


    # Control
    big_arm_joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output='screen'
    )
        
    big_arm_joint_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["big_arm_joint_trajectory_controller", "-c", "/controller_manager"],
        output='screen',
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
        SetParameter(name='use_sim_time', value=True),    
        env_gz_sim,
        gz_launch,
        gateway_spawn,
        big_arm_robot_state_publisher,
        big_arm_spawn,
        ##run_node,
#        run_move_arm,

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
        ),
        gz_sim_bridge
    ])
