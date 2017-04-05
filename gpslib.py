'''
status codes:
1: transmitting correctly
2: Returned no data
3: GPRMC string not returned
4: GPRMC string corrupt
0: No Lock
'''

import serial

class gps:
	def __init__(self,path,led_pin,gpio,baud=9600):
		self.gpio = gpio
		self.gpio.setwarnings(False)
		self.gpio.setmode(self.gpio.BCM)
		self.gpio.setup(led_pin,self.gpio.OUT)
		self.gpio.output(led_pin,self.gpio.LOW)
		self.con=serial.Serial(path,baud)
		self.led_pin=led_pin
		self.signal = 0

	def decode(self):
		dict = None
		data = ""
		line = ""
		for i in range(8):
			data = data + self.con.readline()
		if(not data):
			dict = {"status":2}
			return dict

		for temp in data.strip().split("\n"):
			if(temp.startswith('$GPRMC')):
				line = temp
		if(not line):
			dict = {"status":3}
			return dict

		if(line.find('V',0,len(line)/2) != -1):
			dict = {"status":0}
			return dict
		elif(len(line.strip().split(',')) == 8):
			dict = {"status":4}
			return dict
		else:
	        	lat1, _,lon1  = line.strip().split(',')[3:6]
			time1, _,random1 = line.strip().split(',')[1:4]
			random2, _,speed1 = line.strip().split(',')[5:8]
			speed=float(speed1)
			time2= float(time1)
			lat= float(lat1)
			lon= float(lon1)
			#calculating no. of digits before decimal in lon
			x= lon
			count = 0
			while x>1 :
				x= x/10
				count = count + 1
			# calculating actual latitude from lat
			lat2 =int( int(lat) / 100)
			lat3 = lat - lat2*100
			latitude = lat2 +  lat3/60  
			#calculating actual longitude from lon
			if count==4 :
				factor = 100
			else:
				factor = 1000
			lon2 = int( int(lon)/factor)
			lon3 = lon - lon2*factor
			longitude = lon2 + lon3/60
			#converting time to hhmmss and integers
			hour =(int( time2/10000))  
			minute = int((time2 -( hour*10000))/100) 
			second = int( time2 - (hour*10000) - (minute*100))
			hour = hour + 5
			minute = minute + 30
			if minute > 59:
				minute = minute-60
				hour = hour + 1
			
			if(hour == 24):
				hour = 00			
			dict={
				"status":1,
				"nmea":line,
				"time":str(hour)+":"+str(minute)+":"+str(second),
				"latitude":latitude,
				"longitude":longitude,
				"speed":speed*1.852
			}
			return dict
	
	def set_signal(self,state):
		if(state==0):
			state_string = self.gpio.LOW
		else:
			state_string = self.gpio.HIGH
		self.gpio.output(self.led_pin,state_string)	
