from museum_interfaces.msg import Exhibit
from museum_interfaces.srv import GetExhibits
import rclpy
from rclpy.node import Node


EXHIBITS = [
    (2.0, 2.0, '"Mona Lisa" by Leonadro Da Vinci'),
    (9.0, 2.0, '"The Kiss" by Gustav Klimt'),
    (9.0, 9.0, '"Le Penseur" by Ogust Roden'),
    (2.0, 9.0, '"David" by Michelangelo'),
]


class ExhibitServer(Node):

    def __init__(self):
        super().__init__('exhibit_server')
        self.srv = self.create_service(
            GetExhibits,
            'get_exhibits',
            self.handle_request)

    def handle_request(self, request, response):
        response.exhibits = []
        for x, y, description in EXHIBITS:
            exhibit = Exhibit()
            exhibit.x = x
            exhibit.y = y
            exhibit.description = description
            response.exhibits.append(exhibit)
        self.get_logger().info(
            f'Sent {len(response.exhibits)} exhibits'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ExhibitServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
# cd ~/ros2_hw_ws && source install/setup.bash && ros2 launch museum_guide museum_launch.py
# cd ~/ros2_hw_ws && source install/setup.bash && ros2 run museum_guide route_client
# ros2 run turtlesim turtle_teleop_key --ros-args -r /turtle1/cmd_vel:=/visitor/cmd_vel
# cd ~/ros2_hw_ws && source install/setup.bash && colcon test --packages-select museum_guide
# && colcon test-result --verbose
