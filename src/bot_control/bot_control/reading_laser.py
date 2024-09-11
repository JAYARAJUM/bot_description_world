#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import math

class LaserScanFilter(Node):

    def __init__(self):
        super().__init__('laser_scan_filter')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10)
        self.publisher = self.create_publisher(LaserScan, '/filtered_scan', 10)

    def laser_callback(self, msg):
        filtered_scan = LaserScan()
        filtered_scan.header = msg.header
        filtered_scan.angle_min = 0.0
        filtered_scan.angle_max = math.radians(120)
        filtered_scan.angle_increment = msg.angle_increment
        filtered_scan.time_increment = msg.time_increment
        filtered_scan.scan_time = msg.scan_time
        filtered_scan.range_min = msg.range_min
        filtered_scan.range_max = msg.range_max

        start_index = 0
        end_index = int(120 / math.degrees(msg.angle_increment))

        filtered_scan.ranges = msg.ranges[start_index:end_index]
        filtered_scan.intensities = msg.intensities[start_index:end_index] if msg.intensities else []

        self.publisher.publish(filtered_scan)

def main(args=None):
    rclpy.init(args=args)
    laser_scan_filter = LaserScanFilter()
    rclpy.spin(laser_scan_filter)
    laser_scan_filter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()