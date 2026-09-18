from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hw2_py_pubsub',
            executable='random_publisher',
            name='random_publisher',
            output='screen',
        ),
        Node(
            package='hw2_py_pubsub',
            executable='mode_subscriber',
            name='mode_subscriber',
            output='screen',
        ),
    ])
