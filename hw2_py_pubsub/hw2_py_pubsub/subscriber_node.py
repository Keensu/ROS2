from collections import Counter

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class ModeSubscriber(Node):

    def __init__(self):
        super().__init__('mode_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            'random_number',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Int32, 'mode', 10)
        self.numbers = []
        self.subscription

    def listener_callback(self, msg):
        number = msg.data
        self.numbers.append(number)
        self.get_logger().info(f'Received: {number}, array: {self.numbers}')

        counter = Counter(self.numbers)
        mode_value, mode_count = counter.most_common(1)[0]

        mode_msg = Int32()
        mode_msg.data = mode_value
        self.publisher_.publish(mode_msg)
        self.get_logger().info(
            f'Mode: {mode_value} (has been seen for {mode_count} times), published to /mode')


def main(args=None):
    rclpy.init(args=args)
    node = ModeSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
