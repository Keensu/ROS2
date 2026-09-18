import sys

from hw3_srv_interfaces.srv import CheckFloat
import rclpy
from rclpy.node import Node


class CheckFloatClient(Node):

    def __init__(self):
        super().__init__('check_float_client')
        self.client = self.create_client(CheckFloat, 'check_float')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for server...')
        self.request = CheckFloat.Request()

    def send_request(self, text):
        self.request.input_string = text
        self.future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)
    node = CheckFloatClient()

    text = sys.argv[1] if len(sys.argv) > 1 else '2.93'
    response = node.send_request(text)
    node.get_logger().info(
        f'Sent: "{text}" -> is_float: {response.is_float}'
    )

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
