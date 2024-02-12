#!/bin/bash

#export WEBOTS_HOME=$HOME/webots_R2023a
export WEBOTS_HOME=$HOME/webots-R2022b
source /opt/ros/foxy/setup.bash

#ros2 launch webots_ros2_turtlebot robot_launch.py \
#  world:=turtlebot3_burger_pedestrian_simple.wbt

#ros2 launch webots_ros2_turtlebot robot_launch.py \
#  world:=turtlebot3_burger_pedestrian_no_walls.wbt

ros2 launch webots_ros2_turtlebot robot_launch.py \
  world:=turtlebot3_burger_pedestrian_simple_002.wbt

