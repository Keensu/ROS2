import time

from museum_interfaces.action import GoToExhibit
from museum_interfaces.srv import GetExhibits
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


class RouteClient(Node):

    def __init__(self):
        super().__init__('route_client')
        self.exhibits_client = self.create_client(GetExhibits, 'get_exhibits')
        self.action_client = ActionClient(self, GoToExhibit, 'go_to_exhibit')

    def get_exhibits(self):
        while not self.exhibits_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        future = self.exhibits_client.call_async(GetExhibits.Request())
        rclpy.spin_until_future_complete(self, future)
        return future.result().exhibits

    def send_goal(self, exhibit):
        self.get_logger().info(f'Goal: {exhibit.description}')
        goal = GoToExhibit.Goal()
        goal.target = exhibit
        goal.stop_distance = 1.5

        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        self.get_logger().info(
            f'Done: success={result_future.result().result.success}')

    def run(self):
        exhibits = self.get_exhibits()
        self.get_logger().info(f'Exhibits: {len(exhibits)}')
        for exhibit in exhibits:
            self.send_goal(exhibit)
            time.sleep(1.0)
        self.get_logger().info('Route finished')


def main(args=None):
    rclpy.init(args=args)
    node = RouteClient()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
