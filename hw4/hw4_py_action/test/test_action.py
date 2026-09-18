import unittest

from hw4_action_interfaces.action import CheckPowers
import launch
import launch_ros.actions
import launch_testing.actions
import pytest
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


@pytest.mark.launch_test
def generate_test_description():
    server = launch_ros.actions.Node(
        package='hw4_py_action',
        executable='server',
        name='check_powers_server',
    )
    return launch.LaunchDescription([
        server,
        launch_testing.actions.ReadyToTest(),
    ])


class TestCheckPowersAction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = Node('test_action_client')
        cls.client = ActionClient(cls.node, CheckPowers, 'check_powers')
        assert cls.client.wait_for_server(timeout_sec=10.0), \
            'Action server check_powers is not started'
        cls.feedback_received = []

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.feedback_received.append(feedback_msg.feedback.current_number)

    def send_goal_and_wait(self, numbers, timeout_sec=15.0):
        goal = CheckPowers.Goal()
        goal.numbers = numbers
        send_future = self.client.send_goal_async(
            goal, feedback_callback=self.feedback_callback)
        rclpy.spin_until_future_complete(
            self.node, send_future, timeout_sec=5.0)
        goal_handle = send_future.result()
        self.assertIsNotNone(goal_handle, 'Goal is not accepted')
        self.assertTrue(goal_handle.accepted, 'Goal rejected')

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(
            self.node, result_future, timeout_sec=timeout_sec)
        return result_future.result().result

    def test_all_powers_of_two(self):
        result = self.send_goal_and_wait([1, 2, 4, 8, 16])
        self.assertEqual(
            list(result.flags), [True, True, True, True, True])

    def test_none_are_powers_of_two(self):
        result = self.send_goal_and_wait([3, 5, 6, 7, 9])
        self.assertEqual(
            list(result.flags), [False, False, False, False, False])

    def test_mixed_order(self):
        numbers = [1, 3, 4, 7, 8, 16, 20, 32]
        expected = [True, False, True, False, True, True, False, True]
        result = self.send_goal_and_wait(numbers)
        self.assertEqual(list(result.flags), expected)

    def test_feedback_count(self):
        self.feedback_received.clear()
        numbers = [1, 2, 3, 4, 5]
        self.send_goal_and_wait(numbers)
        self.assertEqual(
            len(self.feedback_received), len(numbers),
            'Feedback received for %d of %d numbers' % (
                len(self.feedback_received), len(numbers)))
