#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int16, Int8, String, Float32, UInt16

x = None
y = None
tx = None
ty = None
RPM = None


def callback(data):
    global x, y, tx, ty
    if x == None and y == None:
        x = data.data
        tx = rospy.Time.to_sec(rospy.Time.now())
        rospy.loginfo(f"{x}:{tx}")
    elif y == None:
        y = x
        ty = tx
        x = data.data
        tx = rospy.Time.to_sec(rospy.Time.now())
        rospy.loginfo(f"{x}:{tx}, {y}:{ty}")
    else:
        y = x
        ty = tx
        x = data.data
        tx = rospy.Time.to_sec(rospy.Time.now())
        calc()


def calc():
    global x, tx, y, ty, RPM
    states = 4096
    limit = 2000
    dl = x - y
    dt = tx - ty

    if dl > limit:
        dl = states - dl
    elif dl < -limit:
        dl = states + dl
        dl = -dl

    RPM = ((dl / 4096) / dt) * 60
    # rospy.loginfo(f'RPM:{RPM}, dt:{dt}), dl:{dl}, x:{x}), tx:{tx}, y:{y}), ty:{ty}, ')

    pub.publish(RPM)
    rospy.loginfo(f"sent {RPM}")


rospy.init_node("position_to_RPM_node")
pub = rospy.Publisher("/virtual_dc_motor_driver/get_velocity", Float32, queue_size=100)
sub = rospy.Subscriber("/virtual_dc_motor/get_position", UInt16, callback)
rospy.loginfo("Node started")


rospy.spin()
