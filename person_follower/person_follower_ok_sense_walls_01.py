# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class PersonFollower(Node):

    def __init__(self):
        super().__init__('person_follower')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, input_msg):
        angle_min = input_msg.angle_min
        angle_max = input_msg.angle_max
        angle_increment = input_msg.angle_increment
        ranges = input_msg.ranges

        a_min = 0
        a_max = 360
        i_min = 170
        i_max = 210
        r_min = 0.5
        r_max = 3.0
        #k_ang_speed = 0.1
        k_ang_speed = 0.2
        #lin_speed = 0.15
        lin_speed = 0.22


        vx = 0.
        wz = 0.

        for i in range(i_min, i_max, 1):
            if r_min < ranges[i] < r_max:                
                vx = lin_speed
                wz = (180 - i) * k_ang_speed
                print ("Detected!  i=" + str(i) + "  Range: " + str(ranges[i]) + "  Linear: " + str(vx) + "   Angular= " + str(wz))
                break
            else:
                vx = 0.
                wz = 0.

        # i=0
        # for r in ranges:
        #     print ("i= " + str(i) + "   r=" + str(r))
        #     i = i+1

        #
        # your code for computing vx, wz
        #
        #vx = 0.
        #wz = 0.
        #
        output_msg = Twist()
        output_msg.linear.x = vx
        output_msg.angular.z = wz
        self.publisher_.publish(output_msg)

def main(args=None):
    rclpy.init(args=args)
    person_follower = PersonFollower()
    rclpy.spin(person_follower)
    person_follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
