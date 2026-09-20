import math
import time

from geometry_msgs.msg import Twist
from museum_interfaces.action import GoToExhibit
import rclpy
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import Float32
from turtlesim_msgs.msg import Pose


LINEAR_SPEED = 1.5
ANGULAR_SPEED = 4.0
TOLERANCE = 0.15
MIN_VISITOR_DISTANCE = 1.5
STOP_TIME = 3.0


class GuideNode(Node):

    def __init__(self):
        super().__init__('guide_node')

        self.guide_pose = None
        self.visitor_distance = None

        self.create_subscription(Pose, '/turtle1/pose', self.pose_cb, 10)
        self.create_subscription(Float32, '/distance', self.distance_cb, 10)

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self._action_server = ActionServer(
            self, GoToExhibit, 'go_to_exhibit', self.execute_cb)

        self.get_logger().info('Guide node started')

    def pose_cb(self, msg):
        self.guide_pose = msg

    def distance_cb(self, msg):
        self.visitor_distance = msg.data

    def stop(self):
        self.cmd_pub.publish(Twist())

    def move_to(self, target_x, target_y):
        if self.guide_pose is None:
            return None

        dx = target_x - self.guide_pose.x
        dy = target_y - self.guide_pose.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < TOLERANCE:
            self.stop()
            return distance

        angle_to_target = math.atan2(dy, dx)
        angle_diff = angle_to_target - self.guide_pose.theta

        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        elif angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        twist = Twist()

        if abs(angle_diff) > 0.1:
            twist.angular.z = ANGULAR_SPEED if angle_diff > 0 else -ANGULAR_SPEED
        else:
            twist.linear.x = LINEAR_SPEED

        if (self.visitor_distance is not None
                and self.visitor_distance < MIN_VISITOR_DISTANCE):
            twist.linear.x = 0.0

        self.cmd_pub.publish(twist)
        return distance

    def execute_cb(self, goal_handle):
        exhibit = goal_handle.request.target
        self.get_logger().info(
            f'Going to: {exhibit.description} '
            f'({exhibit.x:.2f}, {exhibit.y:.2f})')

        feedback = GoToExhibit.Feedback()

        while rclpy.ok():
            distance = self.move_to(exhibit.x, exhibit.y)
            if distance is None:
                time.sleep(0.1)
                continue

            feedback.distance_left = float(distance)
            goal_handle.publish_feedback(feedback)

            if distance < TOLERANCE:
                break

            time.sleep(0.05)

        self.stop()
        self.get_logger().info(f'=== {exhibit.description} ===')
        time.sleep(STOP_TIME)

        goal_handle.succeed()
        result = GoToExhibit.Result()
        result.success = True
        return result


def main(args=None):
    rclpy.init(args=args)
    node = GuideNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
