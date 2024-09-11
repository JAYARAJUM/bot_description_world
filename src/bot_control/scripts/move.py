import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
import math

class RobotNavigator(Node):
    def __init__(self):
        super().__init__('robot_navigator')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)
        self.timer = self.create_timer(0.1, self.navigate)
        
        self.waypoints = [
            [0, 0, 0],
            [5, 0, 45],
            [5, 5, 90],
            [0, 5, 0],
            [0, 0, 135]
        ]
        self.current_waypoint = 0
        self.position = Point()
        self.yaw = 0.0
        self.state = 'move'
        
        # Parameters for smooth motion
        self.linear_speed = 0.5
        self.angular_speed = 0.5
        self.distance_threshold = 0.1
        self.angle_threshold = 0.05
        self.rotation_threshold = 0.1

        self.get_logger().info(f"Starting navigation. First waypoint: {self.waypoints[self.current_waypoint]}")

    def odom_callback(self, msg):
        self.position = msg.pose.pose.position
        orientation_q = msg.pose.pose.orientation
        _, _, self.yaw = euler_from_quaternion([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])

    def navigate(self):
        if self.current_waypoint >= len(self.waypoints):
            self.get_logger().info("All waypoints reached. Navigation completed.")
            return

        target = self.waypoints[self.current_waypoint]
        distance = math.sqrt((target[0] - self.position.x)**2 + (target[1] - self.position.y)**2)
        angle_to_target = math.atan2(target[1] - self.position.y, target[0] - self.position.x)
        angle_diff = self.normalize_angle(angle_to_target - self.yaw)

        cmd_vel = Twist()

        if self.state == 'move':
            if distance > self.distance_threshold:
                cmd_vel.linear.x = min(self.linear_speed, distance)
                cmd_vel.angular.z = self.angular_speed * angle_diff
            else:
                self.state = 'rotate'
                self.get_logger().info(f"Reached position of waypoint {self.current_waypoint}. Rotating to target orientation.")
        elif self.state == 'rotate':
            target_yaw = math.radians(target[2])
            rotation_diff = self.normalize_angle(target_yaw - self.yaw)
            
            if abs(rotation_diff) > self.rotation_threshold:
                cmd_vel.angular.z = self.angular_speed * rotation_diff
            else:
                self.current_waypoint += 1
                self.state = 'move'
                if self.current_waypoint < len(self.waypoints):
                    self.get_logger().info(f"Moving to next waypoint: {self.waypoints[self.current_waypoint]}")
                else:
                    self.get_logger().info("All waypoints completed.")

        self.publisher.publish(cmd_vel)

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

def main(args=None):
    rclpy.init(args=args)
    navigator = RobotNavigator()
    rclpy.spin(navigator)
    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()