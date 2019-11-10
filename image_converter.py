#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import cv2

import cv_bridge
import sensor_msgs.msg

import argparse
import numpy as np

class image_converter:
    def __init__(self, input_topic, output_topic):
        self.image_pub = rospy.Publisher(
            output_topic, sensor_msgs.msg.Image, queue_size=10)
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber(
            input_topic, sensor_msgs.msg.Image,
            self.callback)

    def callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        #
        # DO SOMETHING
        #
        try:
            ros_img = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
        except cv_bridge.CvBridgeError as e:
            print(e)

        self.image_pub.publish(ros_img)

# Usage:
# rosrun PACKAGE image_converter.py input:=/camera/image_raw_throttle output:=/test
#
def main(args):
    rospy.init_node('image_converter', anonymous=True)
    input_topic = rospy.resolve_name("input")
    output_topic = rospy.resolve_name("output")
    print("input_topic: %s" % (input_topic,))
    print("output_topic: %s" % (output_topic,))
    sys.stdout.flush()
    ic = image_converter(input_topic, output_topic)
    try:
        print("Invoke rospy.spin().")
        sys.stdout.flush()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)