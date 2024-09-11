import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.substitutions import FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    package_name = 'bot_description'
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    world_file = PathJoinSubstitution(
        [
            FindPackageShare(package_name),
            "world",
            "example.world"
        ]
    )
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare(package_name),
            "config",
            "controller_manager.yaml",
        ]
    )
    
    # Get URDF via xacro
    robot_description_content = Command(
        [
            FindExecutable(name="xacro"), " ",
            PathJoinSubstitution([FindPackageShare(package_name), "urdf", "robot_urdf.xacro"]),
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    # Robot State Publisher
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp_launch.py'
        )]), launch_arguments={'use_sim_time': use_sim_time, 'use_ros2_control': 'true'}.items()
    )
   
    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={
            'verbose': 'true',
            'world_name': world_file,
            'use_sim_time': use_sim_time,
        }.items()
    )
    
    # Controller Manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, robot_controllers, {'use_sim_time': use_sim_time}],
        output='both',
    )

    # Spawn Entity
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'OGMEN',
                   '-x', '0',
                   '-y', '0',
                   '-z', '0.01'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    # Diff Drive Spawner
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
        parameters=[{'use_sim_time': use_sim_time}],
        output="screen"
    )

    # Joint Broad Spawner
    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        parameters=[{'use_sim_time': use_sim_time}],
        output="screen"
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation (Gazebo) clock if true'),
        rsp,
        gazebo,
        controller_manager,
        joint_broad_spawner,
        diff_drive_spawner,
        spawn_entity
    ])