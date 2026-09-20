from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen',
        ),
        Node(
            package='museum_guide',
            executable='exhibit_markers',
            name='exhibit_markers',
            output='screen',
        ),
        Node(
            package='museum_guide',
            executable='visitor_spawner',
            name='visitor_spawner',
            output='screen',
        ),
        Node(
            package='museum_guide',
            executable='distance_monitor',
            name='distance_monitor',
            output='screen',
        ),
        Node(
            package='museum_guide',
            executable='exhibit_server',
            name='exhibit_server',
            output='screen',
        ),
        Node(
            package='museum_guide',
            executable='guide_node',
            name='guide_node',
            output='screen',
        ),
    ])
