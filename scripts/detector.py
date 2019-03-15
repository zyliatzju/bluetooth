#!/usr/bin/env python

import rospy
import bluetooth


def find_device():
	found = 0;

	rospy.loginfo("performing inquiry...")

	nearby_devices = bluetooth.discover_devices(
	        duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

	rospy.loginfo("found %d devices" % len(nearby_devices))

	for addr, name in nearby_devices:
	    try:
	        rospy.loginfo("  %s - %s" % (addr, name))
	    except UnicodeEncodeError:
	        rospy.loginfo("  %s - %s" % (addr, name.encode('utf-8', 'replace')))



if __name__ == '__main__':
	rospy.init_node('bt_detector')
	find_device()
