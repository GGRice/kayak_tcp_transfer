#!/usr/bin/env python

import argparse
import socket
import rospy
import time
import yaml
from TCP import *
from std_msgs.msg import String
from glider_kayak_sim.msg import STU, UnderwaterGeoPose, UnderwaterGeoPoint


class KayakReader(object):
	def __init__(self, n):
		#subscribes to kayak_n sensor and position
		stu_sub = rospy.Subscriber("kayak_%d/stu_sensor"%n, STU, self.stuCallback)
		pose_sub = rospy.Subscriber("kayak_%d/pose"%n, UnderwaterGeoPose, self.poseCallback)
		
		#creates variable to hold kayak_n values
		self.temperature = None
		self.salinity = None
		self.longitude = None
		self.latitude = None
		self.depth = None
		self.x = None
		self.y = None
		self.z = None
		self.w = None

	#sets the sensor variables equal to subscribes values
	def stuCallback(self, data):
		self.temperature = data.temperature
		self.salinity = data.salinity

	#sets position variables equal to subscribed values
	def poseCallback(self, data):
		self.longitude = data.position.longitude
		self.latitude = data.position.latitude
		self.depth = data.position.depth
		self.x = data.orientation.x
		self.y = data.orientation.y
		self.z = data.orientation.z
		self.w = data.orientation.w

def main():
	rospy.init_node("kayak_tcp")
	rate = rospy.Rate(.1)

	t=time.time()

	#initializes TCP server
	tcp = TCP(mode='server')

	#create kayak subscribers
	#to subscribe to new kayaks: reader# = KayakReader(#)
	reader0 = KayakReader(0)
	reader1 = KayakReader(1)


	#while ros is running, constantly update the database
	#when client corresponds with this server, use these databases
	#When subscribing to new kayaks add
	#			k# = dict(Temperature = reader#.temperature, Salinity = reader#.salinity, Latitude = reader#.latitude, Longitude = reader#.longitude, Depth = reader#.depth, x = reader#.x, y = reader#.y, z = reader#.z, w = reader#.w)
	while not rospy.is_shutdown():
		if reader0.temperature is not None and reader0.longitude is not None:
			k0 = dict(Time = t, Temperature = reader0.temperature, Salinity = reader1.salinity, Latitude = reader0.latitude, Longitude = reader0.longitude, Depth = reader0.depth, x = reader0.x, y = reader0.y, z = reader0.z, w = reader0.w)
			k1 = dict(Time = t, Temperature = reader1.temperature, Salinity = reader1.salinity, Latitude = reader1.latitude, Longitude = reader1.longitude, Depth = reader1.depth, x = reader1.x, y = reader1.y, z = reader1.z, w = reader1.w)
			
			with open('data.yml', 'w') as outfile:
				yaml.dump(k0, outfile, default_flow_style=False)

			tcp.database['kayak_0']= yaml.dump(k0)
			tcp.database['kayak_1']= yaml.dump(k1)
	rate.sleep()




if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    pass
