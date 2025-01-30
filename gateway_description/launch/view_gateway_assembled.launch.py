from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition

def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz",
            default_value='true',
            description="launch rviz",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "gui",
            default_value='true',
            description="launch joint control guis",
        )
    )

    rviz = LaunchConfiguration("rviz")
    gui = LaunchConfiguration("gui")

    # *****************************
    # Gateway body (static)
    # *****************************
    gateway_body_xacro = Command([
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("gateway_description"), "robots", "gateway_body.urdf.xacro"]),
        ])
    gateway_robot_description = {"robot_description": gateway_body_xacro}

    gateway_rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[
            gateway_robot_description,
            {'frame_prefix': 'gateway_body/'}],
        namespace="gateway_body"
    )

    # ***********************
    #  Big Arm
    # ***********************
    big_arm_xacro = Command([
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("gateway_description"), "robots", "big_arm.urdf.xacro"]),
        ])
    big_arm_robot_description = {"robot_description": big_arm_xacro}

    big_arm_rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[
            big_arm_robot_description,
            {'frame_prefix': 'big_arm/'}],
        namespace="big_arm"
    )

    big_arm_jsp = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace="big_arm",
        condition=IfCondition(gui)
    )

    big_arm_static_pub = Node(
        name="big_arm_static_publisher",
        package="tf2_ros",
        executable="static_transform_publisher",
        output="screen",
        # found this transform from the "older" model of a uni-body gateway model
        arguments=["1.0213", "-3.9783", "-0.1377", # XYZ
                   "0.12043", "-0.20551", "0.96527", "-0.10728", # XYZW
                   "gateway_body/root",
                   "big_arm/big_arm_link_0"]
    )

    # *************************
    #  Little Arm
    # **************************
    little_arm_xacro = Command([
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("gateway_description"), "robots", "little_arm.urdf.xacro"]),
        ])
    little_arm_robot_description = {"robot_description": little_arm_xacro}

    little_arm_rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[
            little_arm_robot_description,
            {'frame_prefix': 'little_arm/'}],
        namespace="little_arm"
    )
    little_arm_jsp = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace="little_arm",
        condition=IfCondition(gui)
    )

    little_arm_static_pub = Node(
        name="little_arm_static_publisher",
        package="tf2_ros",
        executable="static_transform_publisher",
        output="screen",
        # found this transform from the "older" model of a uni-body gateway model
        arguments=["0.79101", "-12.157", "-7.121", # XYZ
                   "0.74426", "-0.51624", "0.96527", "-0.10728", # XYZW
                   "gateway_body/root",
                   "little_arm/little_arm_link_0"]
    )

    # **************************************
    # RVIZ
    # **************************************
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("gateway_description"), "rviz", "view_gateway_assembled.rviz"]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        condition=IfCondition(rviz)
    )

    nodes_to_start = [
        gateway_rsp,
        big_arm_rsp,
        big_arm_jsp,
        big_arm_static_pub,
        little_arm_rsp,
        little_arm_jsp,
        little_arm_static_pub,
        rviz_node,
    ]

    return LaunchDescription(declared_arguments + nodes_to_start)


