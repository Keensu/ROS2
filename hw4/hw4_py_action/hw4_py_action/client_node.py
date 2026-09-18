import sys

from hw4_action_interfaces.action import CheckPowers
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


class CheckPowersClient(Node):

    def __init__(self):
        super().__init__('check_powers_client')
        self._action_client = ActionClient(self, CheckPowers, 'check_powers')

    def send_goal(self, numbers):
        self.get_logger().info('Waiting for server...')
        self._action_client.wait_for_server()

        goal_msg = CheckPowers.Goal()
        goal_msg.numbers = numbers

        self.get_logger().info(f'Sending goal: numbers={numbers}')
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: number={fb.current_number}, '
            f'is_power_of_two={fb.is_power_of_two}'
        )

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: flags={list(result.flags)}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = CheckPowersClient()

    if len(sys.argv) > 1:
        numbers = [int(x) for x in sys.argv[1:]]
    else:
        numbers = [1, 3, 4, 7, 8, 16, 20, 32]

    node.send_goal(numbers)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
