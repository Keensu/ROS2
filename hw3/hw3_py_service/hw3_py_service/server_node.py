from hw3_srv_interfaces.srv import CheckFloat
import rclpy
from rclpy.node import Node


class CheckFloatServer(Node):

    def __init__(self):
        super().__init__('check_float_server')
        self.srv = self.create_service(
            CheckFloat,
            'check_float',
            self.handle_request)

    def handle_request(self, request, response):
        text = request.input_string
        try:
            float(text)
            response.is_float = True
        except ValueError:
            response.is_float = False

        self.get_logger().info(
            f'Request: "{text}" -> is_float: {response.is_float}'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = CheckFloatServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
