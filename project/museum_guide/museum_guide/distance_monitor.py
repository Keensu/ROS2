import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from turtlesim_msgs.msg import Pose


def calculate_distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx * dx + dy * dy)


class DistanceMonitor(Node):

    def __init__(self):
        super().__init__('distance_monitor')
        self.guide_pose = None
        self.visitor_pose = None

        self.create_subscription(Pose, '/turtle1/pose', self.guide_cb, 10)
        self.create_subscription(Pose, '/visitor/pose', self.visitor_cb, 10)

        self.pub = self.create_publisher(Float32, '/distance', 10)
        self.create_timer(0.1, self.publish)

    def guide_cb(self, msg):
        self.guide_pose = msg

    def visitor_cb(self, msg):
        self.visitor_pose = msg

    def publish(self):
        if self.guide_pose is None or self.visitor_pose is None:
            return
        distance = calculate_distance(
            self.guide_pose.x, self.guide_pose.y,
            self.visitor_pose.x, self.visitor_pose.y)

        msg = Float32()
        msg.data = distance
        self.pub.publish(msg)

        self.get_logger().info(f'Distance: {distance:.2f}', throttle_duration_sec=3.0)


def main(args=None):
    rclpy.init(args=args)
    node = DistanceMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
