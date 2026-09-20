import time

import rclpy
from rclpy.node import Node
from turtlesim_msgs.srv import SetPen, Spawn


VISITOR_NAME = 'visitor'
VISITOR_X = 10.0
VISITOR_Y = 10.0
VISITOR_THETA = 0.0


class VisitorSpawner(Node):

    def __init__(self):
        super().__init__('visitor_spawner')
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.pen_client = self.create_client(
            SetPen, f'/{VISITOR_NAME}/set_pen')

        self.spawn_visitor()

    def spawn_visitor(self):
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /spawn service...')

        request = Spawn.Request()
        request.x = VISITOR_X
        request.y = VISITOR_Y
        request.theta = VISITOR_THETA
        request.name = VISITOR_NAME

        future = self.spawn_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        self.get_logger().info(f'Spawned visitor: {future.result().name}')

        time.sleep(1.0)

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for set_pen service...')

        pen_request = SetPen.Request()
        pen_request.off = 1
        pen_future = self.pen_client.call_async(pen_request)
        rclpy.spin_until_future_complete(self, pen_future)
        self.get_logger().info('Visitor pen is OFF')


def main(args=None):
    rclpy.init(args=args)
    node = VisitorSpawner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
