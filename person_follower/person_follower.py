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

import statistics 

last_indexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
first_init = True


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

        a_min = 0    # LaserScan min angle
        a_max = 360  # LaserScan max angle
        i_min = 170  # LaserScan min index
        i_max = 210  # LaserScan max index
        r_min = 0.1  # range min (following)
        r_max = 2.5  # range max (following)
        # k_ang_speed = 0.1
        # constant factor for angular speed  (Turtlebot max rot: 2.84 rad/s)
        k_ang_speed = 0.2


        lin_speed = 0.15
        # lin_speed = 0.22     #max lin speed for Turtlebot3 (m/s)
        # lin_speed = 0.10     #max lin speed for Turtlebot3 (m/s)

        vx = 0.
        wz = 0.

        i_min_detected = get_mean_i_detected(ranges)
        #i_min = i_min_detected - 20
        #i_max = i_min_detected + 20

        if r_min < ranges[i_min_detected] < r_max:
            vx = lin_speed
            wz = (180 - i_min_detected) * k_ang_speed
            wz = angular_limited(wz)
            print("Detected!  i=" + str(i_min_detected) + "  Range: " +
                str(ranges[i_min_detected]) + "  linear.x: " + str(vx) + "   angular.z= " + str(wz))
        else:
            vx = 0.
            wz = 0.



        # for i in range(i_min, i_max, 1):
        #     if r_min < ranges[i] < r_max:
        #         vx = lin_speed
        #         wz = (180 - i) * k_ang_speed
        #         wz = angular_limited(wz)
        #         print("Detected!  i=" + str(i) + "  Range: " +
        #               str(ranges[i]) + "  linear.x: " + str(vx) + "   angular.z= " + str(wz))
        #         break
        #     else:
        #         vx = 0.
        #         wz = 0.

        # i=0
        # for r in ranges:
        #     print ("i= " + str(i) + "   r=" + str(r))
        #     i = i+1

        #
        # your code for computing vx, wz
        #
        # vx = 0.
        # wz = 0.
        #
        output_msg = Twist()
        output_msg.linear.x = vx
        output_msg.angular.z = wz
        self.publisher_.publish(output_msg)


def angular_limited(wz):
    wz_max = 0.5

    if (wz > wz_max):
        print(">> limiting wz= " + str(wz) + "  to wz_max= " + str(wz_max))
        wz = wz_max
    if (wz < -wz_max):
        print(">> limiting wz= " + str(wz) + "  to wz_max= " + str(-wz_max))
        wz = -wz_max
    
    return wz


def get_mean_i_detected(ranges):
    v_min = min(ranges)
    i_min = ranges.index(v_min)
    
    print("v_min= " + str(v_min) + "   i_min=" +  str(i_min) + "   last_indexes= " + str(last_indexes))

    global first_init

    if first_init:
        for i in range(len(last_indexes)):
            last_indexes[i] = i_min
        first_init = False
    else:
        mean_i = round(statistics.mean(last_indexes))
        #if (abs(mean_i - i_min)<10):
        if (True):
            for i in range(len(last_indexes)-1, 0, -1):                
                last_indexes[i] = last_indexes[i-1]
            last_indexes[0] = i_min

    print("v_min= " + str(v_min) + "   i_min=" +  str(i_min) + "   last_indexes= " + str(last_indexes) + " << despues")

    mean_i = round(statistics.mean(last_indexes))

    print("mean_i= " + str(mean_i))

    return mean_i

    # for i, v in enumerate(ranges):
    #     print("i= " +  str(i) + "   v= " + str(v))



def main(args=None):
    rclpy.init(args=args)
    person_follower = PersonFollower()
    rclpy.spin(person_follower)
    person_follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
