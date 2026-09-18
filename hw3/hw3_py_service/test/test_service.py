import unittest

from hw3_srv_interfaces.srv import CheckFloat
import launch
import launch_ros.actions
import launch_testing.actions
import pytest
import rclpy
from rclpy.node import Node


@pytest.mark.launch_test
def generate_test_description():
    server = launch_ros.actions.Node(
        package='hw3_py_service',
        executable='server',
        name='check_float_server',
    )
    return launch.LaunchDescription([
        server,
        launch_testing.actions.ReadyToTest(),
    ])


class TestCheckFloatService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = Node('test_service_client')
        cls.client = cls.node.create_client(CheckFloat, 'check_float')
        assert cls.client.wait_for_service(timeout_sec=10.0), \
            'Service check.float does not started'

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def call_service(self, text):
        req = CheckFloat.Request()
        req.input_string = text
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self.node, future, timeout_sec=5.0)
        return future.result()

    def test_valid_float(self):
        response = self.call_service('3.14')
        self.assertTrue(response.is_float, '"3.14" must be float')

    def test_negative_float(self):
        response = self.call_service('-2.5')
        self.assertTrue(response.is_float, '"-2.5" must be float')

    def test_integer_is_not_float(self):
        pass

    def test_not_a_float(self):
        response = self.call_service('hello')
        self.assertFalse(response.is_float, '"hello" is not float')

    def test_empty_string(self):
        response = self.call_service('')
        self.assertFalse(response.is_float, '"" is not float')
