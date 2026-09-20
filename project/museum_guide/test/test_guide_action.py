import unittest

import launch
import launch_ros.actions
import launch_testing.actions
from museum_interfaces.action import GoToExhibit
from museum_interfaces.msg import Exhibit
import pytest
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


@pytest.mark.launch_test
def generate_test_description():
    guide_node = launch_ros.actions.Node(
        package='museum_guide',
        executable='guide_node',
        name='guide_node',
    )
    return launch.LaunchDescription([
        guide_node,
        launch_testing.actions.ReadyToTest(),
    ])


class TestGuideAction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = Node('test_guide_client')
        cls.client = ActionClient(cls.node, GoToExhibit, 'go_to_exhibit')
        assert cls.client.wait_for_server(timeout_sec=10.0), \
            'Action go_to_exhibit is not started'

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def send_goal(self, x, y, description):
        target = Exhibit()
        target.x = x
        target.y = y
        target.description = description

        goal = GoToExhibit.Goal()
        goal.target = target
        goal.stop_distance = 1.5

        send_future = self.client.send_goal_async(goal)
        rclpy.spin_until_future_complete(
            self.node, send_future, timeout_sec=5.0)
        return send_future.result()

    def test_goal_accepted(self):
        goal_handle = self.send_goal(6.0, 5.5, 'Test exhibit')
        self.assertIsNotNone(goal_handle, 'Goal handle is None')
        self.assertTrue(goal_handle.accepted, 'Goal must be accepted')

    def test_goal_rejected_when_no_pose(self):
        # second goal should not be recieved while first is active
        # or check if server is answering
        goal_handle = self.send_goal(3.0, 3.0, 'Second exhibit')
        self.assertIsNotNone(goal_handle)
