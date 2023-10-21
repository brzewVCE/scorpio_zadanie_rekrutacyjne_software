#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, Int8

vel = None
goal = None
motor_command = 0
log = []
limit = 100

change = 1  # In int


def set_velocity_goal_callback(data):
    global goal
    goal = data.data
    convert_velocity_to_motor_command()


def get_velocity_callback(data):
    global vel
    vel = data.data
    rospy.loginfo(f"Received get_velocity: {vel}")

    convert_velocity_to_motor_command()


def convert_velocity_to_motor_command():
    global vel, goal, motor_command, change, signal, log, limit
    if vel is not None and goal is not None:
        if round(vel) > goal:
            motor_command = motor_command - change
        elif round(vel) < goal:
            motor_command = motor_command + change

        time = rospy.Time.to_sec(rospy.Time.now())

        pub.publish(motor_command)
        log.append(
            {"goal": goal, "velocity": vel, "signal": motor_command, "time": time}
        )

        total_vel = sum(entry["velocity"] for entry in log)
        num_entries = len(log)

        avg_vel = total_vel / num_entries
        rospy.loginfo(
            f'goal: {goal}, velocity:{vel}, signal"{motor_command}, avg_velocity: {avg_vel}, time: {time}'
        )


rospy.init_node("motor_speed_controller_node")
pub = rospy.Publisher("/virtual_dc_motor/set_cs", Int8, queue_size=100)
sub = rospy.Subscriber(
    "/virtual_dc_motor_controller/set_velocity_goal",
    Float32,
    callback=set_velocity_goal_callback,
)
sub = rospy.Subscriber(
    "/virtual_dc_motor_driver/get_velocity", Float32, callback=get_velocity_callback
)
rospy.loginfo("Node started")

rospy.spin()
