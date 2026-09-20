import unittest

import launch
import launch_ros.actions
import launch_testing.actions
from museum_interfaces.srv import GetExhibits
import pytest
import rclpy
from rclpy.node import Node


@pytest.mark.launch_test
def generate_test_description():
    exhibit_server = launch_ros.actions.Node(
        package='museum_guide',
        executable='exhibit_server',
        name='exhibit_server',
    )
    return launch.LaunchDescription([
        exhibit_server,
        launch_testing.actions.ReadyToTest(),
    ])


class TestExhibitService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = Node('test_exhibit_client')
        cls.client = cls.node.create_client(GetExhibits, 'get_exhibits')
        assert cls.client.wait_for_service(timeout_sec=10.0), \
            'Service get_exhibits is not started'

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def call_service(self):
        future = self.client.call_async(GetExhibits.Request())
        rclpy.spin_until_future_complete(
            self.node, future, timeout_sec=5.0)
        return future.result()

    def test_exhibits_count(self):
        response = self.call_service()
        self.assertEqual(
            len(response.exhibits), 4,
            'Must return exactly 4 exhibits')

    def test_descriptions_not_empty(self):
        response = self.call_service()
        for exhibit in response.exhibits:
            self.assertTrue(
                len(exhibit.description) > 0,
                'Exhibit description must not be empty')

    def test_coordinates_in_range(self):
        response = self.call_service()
        for exhibit in response.exhibits:
            self.assertGreaterEqual(exhibit.x, 0.0)
            self.assertLessEqual(exhibit.x, 11.0)
            self.assertGreaterEqual(exhibit.y, 0.0)
            self.assertLessEqual(exhibit.y, 11.0)
