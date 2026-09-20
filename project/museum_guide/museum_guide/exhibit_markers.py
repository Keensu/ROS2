import time

import rclpy
from rclpy.node import Node
from turtlesim_msgs.srv import Spawn


EXHIBITS = [
    (2.0, 2.0, 'exhibit_1'),
    (9.0, 2.0, 'exhibit_2'),
    (9.0, 9.0, 'exhibit_3'),
    (2.0, 9.0, 'exhibit_4'),
]


class ExhibitMarkers(Node):

    def __init__(self):
        super().__init__('exhibit_markers')
        self.spawn_client = self.create_client(Spawn, '/spawn')

        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /spawn service...')

        for x, y, name in EXHIBITS:
            request = Spawn.Request()
            request.x = x
            request.y = y
            request.theta = 0.0  # for spawn required field
            request.name = name
            future = self.spawn_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            self.get_logger().info(f'Spawned {name} at ({x}, {y})')
            time.sleep(0.3)


def main(args=None):
    rclpy.init(args=args)
    node = ExhibitMarkers()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
