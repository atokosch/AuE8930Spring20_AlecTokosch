#!/usr/bin/env python

import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt

# Alec Tokosch
# Assignment  - TurleSim
# This file contains the python script for the third task which is make the 
# square_closedloop.py file. 


class turtlebot():

    def __init__(self):
        #Creating our node,publisher and subscriber
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    #Callback function implementing the pose value received
    def callback(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def get_distance(self, goal_x, goal_y):
        distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
        return distance

    def move2goal(self):
        goal_pose = Pose()
        # Set the goal position based on the loop form the main below
        goal_pose.x = newX 
        goal_pose.y = newY 
        distance_tolerance = .1
        vel_msg = Twist()

        # Declare and set the relative angle to 0
        relative_angle = 0

        # Calculate the relative angle by getting the goal position and the current position
        relative_angle = (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x))-self.pose.theta

        # If the relative angle is greater than 0.01, then go into the while loop and continue in the loop
        # until the relative angle is less than 0.01. This ensures that the turtlebot turns and points in
        # the correct direction before moving towards the goal position. 0.01 is the angular tolerance, 
        # a larger angular tolerance the larger distance tolerance is needed. Setting to very small to
        # avoid issues with the turtlebot missing the goal position with tolerance and continuing off into 
        # open space (the edge of the window)
        while abs(relative_angle)>.01:

            #Porportional Controller
            # Ensure that the linear velocities are set to 0
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            #angular velocity in the z-axis:
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 4 * (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x) - self.pose.theta)
            relative_angle = (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x))-self.pose.theta

            #Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()

        # Publish the angular velocity as 0 to ensure that it is not moving
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # Now, lets move towards the goal on the x-axis, using the loop. It will continue to move towards the goal 
        # until it is within the distance tolerance which was set above to be 0.1
        while sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) >= distance_tolerance:

            #Porportional Controller
            #linear velocity in the x-axis:
            vel_msg.linear.x = 1.5 * sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Ensure that the angular velocities are set to 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0

            #Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        #Stopping our robot after the movement is over
        vel_msg.linear.x = 0
        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        #Testing our function

        # X and Y coordinate to go to 
        go_To_X = [5, 8, 8, 5, 5]
        go_To_Y = [5, 5, 8, 8, 5]

        x = turtlebot()

        # For loop to call move to goal and change the different X and Y coordinates in use
        for n in range(len(go_To_X)):
            newX = go_To_X[n]
            newY = go_To_Y[n]
            x.move2goal()

    except rospy.ROSInterruptException: pass
