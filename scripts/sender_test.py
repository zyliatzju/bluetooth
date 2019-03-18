#!/usr/bin/env python

import rospy
import bluetooth
from std_msgs.msg import Int32

def find_device(faddr):
	found = 0;

	rospy.loginfo("performing inquiry...")

	while not rospy.is_shutdown():

		nearby_devices = bluetooth.discover_devices(
		        duration=5, lookup_names=True, flush_cache=True, lookup_class=False)

		rospy.loginfo("found %d devices" % len(nearby_devices))

		for addr, name in nearby_devices:
		    try:
		        rospy.loginfo("  %s - %s" % (addr, name))
		    except UnicodeEncodeError:
		        rospy.loginfo("  %s - %s" % (addr, name.encode('utf-8', 'replace')))

		    if faddr == addr:
		    	rospy.loginfo("{} found".format(faddr))
		    	found = 1

		if not found:
			rospy.loginfo("{} not found".format(faddr))
		else:
			break



def call_service(uuid, addr):
	r = rospy.Rate(1/3.0)
	rospy.loginfo("connecting to service {}...".format(uuid))
	while not rospy.is_shutdown():
		service_matches = bluetooth.find_service( uuid = uuid, address = addr )
		if len(service_matches) == 0:
			rospy.loginfo("couldn't find the service = {}, try again".format(uuid))
		else:
			rospy.loginfo("service found")
			break

		r.sleep()

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	rospy.loginfo("connecting to {} on {} on port {}".format(name,host, port))
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((host,port))

	return sock 

def sender_cmd_cb(data):
	cmd = data.data

if __name__ == '__main__':
	global cmd
	cmd = 0
	rospy.init_node('bt_sender')
	rospy.Subscriber("sender_cmd", Int32, sender_cmd_cb)
	faddr = "24:4C:E3:63:1B:CA"
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	rate = 1/4.0
	Rate = rospy.Rate(rate)
	
	msg_array = ["11001003"]
	#msg_array = ["0","1","2"]
	find_device(faddr)
	rospy.sleep(5)
	sock = call_service(uuid, faddr)
	rospy.loginfo("begin to handshake")
	rospy.sleep(3)
	i  = 0
	while not rospy.is_shutdown():
		sock.send(str(i))
		rospy.loginfo("msg sent: {}".format(i))
		data = sock.recv(1024)
		rospy.loginfo("data recv: {}".format(data))
		if data == '0':
			rospy.loginfo("begin to wait for cmd")
			break		
		Rate.sleep()
	
	while not rospy.is_shutdown():
		rospy.loginfo("cmd received is {}".format(cmd))
		if cmd is 1:
			break
		rospy.sleep(1)
		
	rospy.loginfo("begin to send msg")
	for msg in msg_array:
		sock.send(msg)
		rospy.loginfo("msg sent: {}".format(msg))
		while not rospy.is_shutdown():
			data = sock.recv(1024)
			rospy.loginfo("data recv: {}".format(data))
			if data == '0':
				rospy.loginfo("received feedback, allow to send the next code")
				break
			rospy.sleep(1)

		Rate.sleep()
