import time
import unittest

import launch
import launch_ros.actions
import launch_testing.actions
import pytest
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


@pytest.mark.launch_test
def generate_test_description():
    random_publisher = launch_ros.actions.Node(
        package='hw2_py_pubsub',
        executable='random_publisher',
        name='random_publisher',
    )
    mode_subscriber = launch_ros.actions.Node(
        package='hw2_py_pubsub',
        executable='mode_subscriber',
        name='mode_subscriber',
    )
    return launch.LaunchDescription([
        random_publisher,
        mode_subscriber,
        launch_testing.actions.ReadyToTest(),
    ])


class TestPubSub(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = Node('test_node')
        cls.received = []
        cls.sub = cls.node.create_subscription(
            Int32, 'random_number', cls.callback, 10)
        cls.mode_received = []
        cls.mode_sub = cls.node.create_subscription(
            Int32, 'mode', cls.mode_callback, 10)

    @classmethod
    def callback(cls, msg):
        cls.received.append(msg.data)

    @classmethod
    def mode_callback(cls, msg):
        cls.mode_received.append(msg.data)

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_random_number_published(self):
        end_time = time.time() + 10
        while time.time() < end_time and len(self.received) < 5:
            rclpy.spin_once(self.node, timeout_sec=0.5)
        self.assertGreaterEqual(
            len(self.received), 5,
            f'Got {len(self.received)} messages from /random_number'
        )

    def test_mode_published(self):
        end_time = time.time() + 10
        while time.time() < end_time and len(self.mode_received) < 3:
            rclpy.spin_once(self.node, timeout_sec=0.5)
        self.assertGreaterEqual(
            len(self.mode_received), 3,
            f'Got {len(self.mode_received)} messages from /mode'
        )
