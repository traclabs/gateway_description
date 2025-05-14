import os

from ament_index_python.packages import get_package_share_directory
from craftsman_utils.launch.actions import ScopedIncludeLaunchDescription
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import SetEnvironmentVariable
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():

    # Gazebo setup
    sim_resource_path = os.pathsep.join(
        [
            os.environ.get("GZ_SIM_RESOURCE_PATH", default=""),
            os.path.join(get_package_share_directory("gateway_description"), "models"),
        ]
    )
    env_gz_sim = SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", sim_resource_path)

    # World
    cislunar_sdf = PathJoinSubstitution(
        [FindPackageShare("gateway_description"), "worlds", "cislunar.sdf"]
    )

    # Launch gazebo world
    gz_launch = ScopedIncludeLaunchDescription(
        package="ros_gz_sim",
        launch_file="launch/gz_sim.launch.py",
        launch_arguments={"gz_args": [cislunar_sdf, " -r", " -v 4"]},
        global_params={"use_sim_time": "True"},
    )

    # Spawn Gateway
    gateway = ScopedIncludeLaunchDescription(
        package="gateway_description",
        launch_file="launch/spawn_gateway.launch.py",
        launch_arguments={"use_sim_time": True},
    )

    # Spawn big arm and its controllers
    big_arm = ScopedIncludeLaunchDescription(
        package="gateway_description",
        launch_file="launch/spawn_big_arm.launch.py",
        launch_arguments={"use_sim_time": True},
    )

    # Spawn little arm and its controllers
    little_arm = ScopedIncludeLaunchDescription(
        package="gateway_description",
        launch_file="launch/spawn_little_arm.launch.py",
        launch_arguments={"use_sim_time": True},
    )

    # Make the /clock topic available in ROS
    gz_sim_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        ],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    return LaunchDescription(
        [
            env_gz_sim,
            gz_launch,
            gateway,
            big_arm,
            little_arm,
            gz_sim_bridge,
        ]
    )
