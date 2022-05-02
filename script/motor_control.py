#!/usr/bin/python3

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import numpy as np
import math as m
import rospy
from geometry_msgs.msg import Twist

WHEEL_BASE = 0.28
MAX_Linear  = 1
MAX_Angular = 1
Wheel_prem = (np.pi * 0.0254 * 6.5) #pi inch_to_meter  diameter


class Mover():
	def __init__(self,port, baud, ID):
		self.client = ModbusClient(method = 'rtu', port = port, baudrate = baud)
		self.ID = ID
		self.client.connect()
		
		print("Motors control node start")
		print(">>>...................<<<")
		print(">>>...................<<<")
		print(">>>...................<<<")
		print(">>>...................<<<")
		print(">>>...................<<<")
		
		self.write_reg_with_check(0x200D, 0x0003)
		print(">>>1<<<")
		self.write_regs_with_check(0x2080,[0x01F4, 0x01F4, 0x01F4, 0x01F4])
		print(">>>2<<<")
		self.write_reg_with_check(0x200E, 0x0008)
		print(">>>3<<<")
		self.write_regs_with_check(0x2088, [0, 0])
		
		self.L_rpm = 0
		self.R_rpm = 0

		print("Motor config done!!!")
		print(">>>...................<<<")
		print(">>>...................<<<")
		print(">>>...................<<<")
		print(">>>...................<<<")
		print(">>>...................<<<")
		
		rospy.init_node("twist_to_motors")
		rospy.Subscriber("/cmd_vel", Twist, self.get_target_vel)
		rospy.loginfo("motor control node start")

	def write_regs_with_check(self, regs, vals):	
		while(self.client.write_registers(regs, vals, unit=self.ID).isError()):	
			rospy.sleep(0.005)	

	def write_reg_with_check(self, reg, val):	
		while(self.client.write_register(reg, val, unit=self.ID).isError()):	
			rospy.sleep(0.005)	

	def Set_RPM(self):    
		self.client.write_registers(0x2088, [np.uint16(self.L_rpm), np.uint16(-self.R_rpm)], unit=self.ID)
		rospy.sleep(0.001)

		
	def get_target_vel(self,vel):
		linear_velocity = vel.linear.x
		angular_rate = vel.angular.z
	  	
		if (linear_velocity>MAX_Linear):
			linear_velocity = MAX_Linear
		elif (linear_velocity <-MAX_Linear):
			linear_velocity = -MAX_Linear
			
		if (angular_rate>MAX_Angular):   
			angular_rate = MAX_Angular		
		elif (angular_rate  <-MAX_Angular):
			angular_rate = -MAX_Angular

		velSum0 =  linear_velocity - angular_rate*WHEEL_BASE/2
		velSum1 =  linear_velocity + angular_rate*WHEEL_BASE/2
		self.L_rpm = int(60 * velSum0/Wheel_prem)
		self.R_rpm = int(60 * velSum1/Wheel_prem)
		rospy.loginfo(".")


	def spin(self):
		while not rospy.is_shutdown():			
			self.Set_RPM()  			
			#rospy.loginfo("data %d, %d",self.R_rpm, self.L_rpm)
			rospy.sleep(0.03) 
			
if(__name__ == "__main__"):
	controller = Mover("/dev/RS485", 115200, 0x01)
	controller.spin()
	
	
	
	
    
	
