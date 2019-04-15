#!/usr/bin/env python

import rospy
import bluetooth

class BlueSender():
	"""docstring for BlueSender"""
	def __init__(self):
		rospy.init_node('bt_sender')
		self.faddr = "24:4C:E3:63:1B:CA"
		self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
		rate = 1/3.0
		self.Rate = rospy.Rate(rate)
		
		self.motion_queue = [6,13]
		self.video_queue = ["11001001","11001002","11001003"]
		self.trans_video = ["11001000"] #video for transition 
		self.midx = 0
		self.vidx = 0
		self.track_ani = 0
		self.in_ani = 0
		self.ani_finished = 0
		self.prev_ani_finished = 0
		self.prev_video_id = self.trans_video
		self.trans_time = 3
		self.t_trans_offset = 0
		self.trans_begun = 0

		self.init_sock()
		while not rospy.is_shutdown():
			self.sender_loop()
			rospy.sleep(1/1000.0)

	def init_sock():
		self.find_device()
		rospy.sleep(5)
		self.sock = self.call_service()
		rospy.loginfo("begin to handshake")
		rospy.sleep(3)
		while not rospy.is_shutdown():
			self.sock.send(str(0))
			rospy.loginfo("msg sent: {}".format(i))
			data = sock.recv(1024)
			rospy.loginfo("data recv: {}".format(data))
			if data == '0':
				rospy.loginfo("ready")
				break		
			self.Rate.sleep()


	def find_device(self):
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

			    if self.faddr == addr:
			    	rospy.loginfo("{} found".format(self.faddr))
			    	found = 1

			if not found:
				rospy.loginfo("{} not found".format(self.faddr))
			else:
				break

			self.Rate.sleep()


	def call_service(self):
		r = rospy.Rate(1/3.0)
		rospy.loginfo("connecting to service {}...".format(self.uuid))
		while not rospy.is_shutdown():
			service_matches = bluetooth.find_service(uuid = self.uuid,address = self.addr)
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

	def udp_reader(self):
		self.track_ani = input1
		self.in_ani = input2
		self.ani_finished = input3

	def sender_test(self):
		for msg in self.video_queue:
			self.sock.send(msg)
			rospy.loginfo("msg sent: {}".format(msg))
			while not rospy.is_shutdown():
				data = self.sock.recv(1024)
				rospy.loginfo("data recv: {}".format(data))
				if data == '0':
					rospy.loginfo("received feedback, allow to send the next code")
					break
				rospy.sleep(1)

			self.Rate.sleep()	

	def send_motion_msg(self, motion_id):
		# send motion id via udp

	def send_video_msg(self, video_id):
		self.sock.send(video_id)
		# change to another node

	def make_decision(self):
		if self.track_ani is 0:
			self.midx = 0
			self.vidx = 0

		if self.track_ani is 1:
			if self.ani_finished is 1 and self.prev_ani_finished is not 1 and self.trans_begun is 0:
				self.trans_begun = 1
				self.t_trans_offset = rospy.get_time()

			now = rospy.get_time()
			if self.trans_begun is 1 and now > (self.t_trans_offset + self.trans_time):
				self.midx = min(self.midx+1, len(self.motion_queue))
				self.vidx = min(self.vidx+1, len(self.video_queue))
				self.trans_begun = 0

			motion_id = self.motion_queue(self.midx)
			if self.in_ani:
				video_id = self.video_queue(self.vidx)
			else:
				video_id self.trans_video
		else:
			motion_id = self.motion_queue(0)
			video_id = self.trans_video

		self.send_motion_msg(motion_id)
		if video_id is not self.prev_video_id:
			self.send_video_msg(video_id)

		self.prev_ani_finished = self.ani_finished
		self.prev_video_id = video_id

				
if __name__ == '__main__':
	bs = BlueSender()
	rospy.spin()
