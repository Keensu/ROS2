import time

from hw4_action_interfaces.action import CheckPowers
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node


class CheckPowersServer(Node):

    def __init__(self):
        super().__init__('check_powers_server')
        self._action_server = ActionServer(
            self,
            CheckPowers,
            'check_powers',
            self.execute_callback)

    def is_power_of_two(self, n):
        return n > 0 and (n & (n - 1)) == 0

    def execute_callback(self, goal_handle):
        numbers = goal_handle.request.numbers
        self.get_logger().info(f'Got goal: check {list(numbers)}')

        feedback_msg = CheckPowers.Feedback()
        flags = []

        for n in numbers:
            is_pow = self.is_power_of_two(n)
            flags.append(is_pow)

            feedback_msg.current_number = n
            feedback_msg.is_power_of_two = is_pow
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f'Feedback: number={n}, is_power_of_two={is_pow}'
            )
            time.sleep(0.5)

        goal_handle.succeed()
        result = CheckPowers.Result()
        result.flags = flags
        self.get_logger().info(f'Goal finished. Flags: {flags}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = CheckPowersServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
