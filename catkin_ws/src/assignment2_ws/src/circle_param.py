#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

# Alec Tokosch
# Assignment  - TurleSim
# This file contains the python script for the first task which is make the 
# circle.py file. 

def circle():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    
    # Let the user know what is going to happen
    print("Let's move your robot in a circle")

    # Set the linear speed as 1
    speed = rospy.get_param('~speed')
    # Set the angular speed as 1
    angle = rospy.get_param('~angle')
    # Set the disance to travel as 6.5 which is a little more
    # than the circumference, but using PI doesn't let the circle
    # get 100% completed
    distance = rospy.get_param('~distance')

    # Set the linear velocities
    vel_msg.linear.x = abs(speed)
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0

    # Set the angular velocities
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = abs(angle)
    
    while not rospy.is_shutdown():

        #Setting the current time for distance calculus
        t0 = float(rospy.Time.now().to_sec())
        current_distance = 0

        #Loop to move the turtle in an specified distance
        while(current_distance < distance):
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=float(rospy.Time.now().to_sec())
            #Calculates distancePoseStamped
            current_distance= speed*(t1-t0)
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)

        # Let the user know that the robot is done moving
        print("The robot is done moving")

        # Break to open the terminal window back up
        break

if __name__ == '__main__':
    try:
        #Testing our function
        circle()
    except rospy.ROSInterruptException: pass