from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, IfElseSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

  ##########################################
  # Gateway body
  ##########################################
  gateway_urdf_file = PathJoinSubstitution([
    FindPackageShare("gateway_description"), "robots", "gateway_body.urdf.xacro"
  ])

  gateway_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
      PathJoinSubstitution([
        FindPackageShare("craftsman_robots"), "launch", "craftsman_robot_config.launch.py"
      ])
    ]),
    launch_arguments={
      "robot_name": "gateway",
      "urdf_file": gateway_urdf_file, 
      "urdf_mapping": "{'parent_link': 'world'}",
      "launch_robot_state_publisher": "True",
      "launch_joint_state_publisher": IfElseSubstitution(LaunchConfiguration("gz_sim"), 
                                        if_value="False",
                                        else_value="True"
                                      ),
      "launch_srdf_publisher": "False",
      "launch_tf_static": "True",
      "tf_parent_frame": "gateway/world",
      "tf_child_frame": "gateway/root"
    }.items()
  )

  ##########################################
  # big arm
  ##########################################
  big_arm_urdf_file = PathJoinSubstitution([
    FindPackageShare("gateway_description"), "robots", "big_arm.urdf.xacro"
  ])

  big_arm_srdf_file = PathJoinSubstitution([
    FindPackageShare("gateway_application_tools"), "config", "big_arm.srdf.xacro"
  ])

  big_arm_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
      PathJoinSubstitution([
        FindPackageShare("craftsman_robots"), "launch", "craftsman_robot_config.launch.py"
      ])
    ]),
    launch_arguments={
      "robot_name": "big_arm",
      "urdf_file": big_arm_urdf_file, 
      "srdf_file": big_arm_srdf_file,
      "urdf_mapping": "{'parent_link': 'world'}",
      "launch_robot_state_publisher": "True",
      "launch_joint_state_publisher": IfElseSubstitution(LaunchConfiguration("gz_sim"), 
                                        if_value="False",
                                        else_value="True"
                                      ),
      "launch_srdf_publisher": "True",
      "launch_tf_static": "True",
      "tf_parent_frame": "gateway/root",
      "tf_child_frame": "big_arm/world"
    }.items()
  )

  #############################################
  # little arm
  #############################################
  little_arm_urdf_file = PathJoinSubstitution([
    FindPackageShare("gateway_description"), "robots", "little_arm.urdf.xacro"
  ])

  little_arm_srdf_file = PathJoinSubstitution([
    FindPackageShare("gateway_application_tools"), "config", "little_arm.srdf.xacro"
  ])

  little_arm_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
      PathJoinSubstitution([
        FindPackageShare("craftsman_robots"), "launch", "craftsman_robot_config.launch.py"
      ])
    ]),
    launch_arguments={
      "robot_name": "little_arm",
      "urdf_file": little_arm_urdf_file, 
      "srdf_file": little_arm_srdf_file,
      "urdf_mapping": "{'parent_link': 'world'}",
      "launch_robot_state_publisher": "True",
      "launch_joint_state_publisher": IfElseSubstitution(LaunchConfiguration("gz_sim"), 
                                        if_value="False",
                                        else_value="True"
                                      ),
      "launch_srdf_publisher": "True",
      "launch_tf_static": "True",
      "tf_parent_frame": "gateway/root",
      "tf_child_frame": "little_arm/world"
    }.items()
  )

  return LaunchDescription([
    gateway_launch,
    big_arm_launch,
    little_arm_launch,
  ])


