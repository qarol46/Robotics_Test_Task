import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    package_name = 'wheeled_description'

    use_sim_time = LaunchConfiguration('use_sim_time')
    world_file = LaunchConfiguration('world_file')
    
    rsp_launch_file = PathJoinSubstitution([
        get_package_share_directory(package_name),
        'launch',
        'rsp.launch.py'
    ])
    
    wheeled_controllers_config = PathJoinSubstitution([
        get_package_share_directory(package_name),
        'config',
        'wheeled_controllers.yaml'
    ])
    
    gazebo_world_file = PathJoinSubstitution([
        get_package_share_directory(package_name),
        'worlds',
        world_file
    ])

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rsp_launch_file]), 
        launch_arguments={
            'use_sim_time': use_sim_time, 
            'use_ros2_control': 'true'
        }.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={
            'world': gazebo_world_file,
            'verbose': 'false',
            'pause': 'false'
        }.items()
    )
    
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'wheeled_robot', '-x', '0.0', '-y', '0.0', '-z', '0.5'],
        output='screen'
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            wheeled_controllers_config,
            {"use_sim_time": use_sim_time}
        ],
        output="screen",
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen"
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["wheeled_base_controller"],
        output="screen"
    )

    lio_sam_share_dir = get_package_share_directory('lio_sam')
    lio_sam_params_file = os.path.join(lio_sam_share_dir, 'config', 'params.yaml')
    lio_sam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('lio_sam'), 'launch', 'run.launch.py')
        ]),
        launch_arguments={
            'params_file': lio_sam_params_file,
            'use_sim_time': use_sim_time
        }.items()
    )

    delayed_controller_spawner = TimerAction(
        period=3.0,
        actions=[control_node, joint_broad_spawner, diff_drive_spawner]
    )

    delayed_lio_sam = TimerAction(
        period=5.0,
        actions=[lio_sam_launch]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'world_file',
            default_value='obstacle_maze.world',
            description='World file to load in Gazebo'
        ),
        
        rsp,
        gazebo,
        spawn_entity,
        delayed_controller_spawner,
        delayed_lio_sam,
    ])