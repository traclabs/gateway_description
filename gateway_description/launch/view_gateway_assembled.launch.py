from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "example_arg",
            default_value='false',
            description="example arg to show how to do this",
        )
    )
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

    example_arg = LaunchConfiguration("example_arg")
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
            {'frame_prefix': ''}],
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
            {'frame_prefix': ''}],
        namespace="big_arm"
    )
    big_arm_jsp = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace="big_arm",
        condition=IfCondition(gui)
    )

    # **************************
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
            {'frame_prefix': ''}],
        namespace="little_arm"
    )
    little_arm_jsp = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace="little_arm",
        condition=IfCondition(gui)
    )

    # **************************************
    # RVIZ
    #***************************************
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
        little_arm_rsp,
        little_arm_jsp,
        rviz_node,
    ]

    return LaunchDescription(declared_arguments + nodes_to_start)


