import time
import serial

con = serial.Serial('/dev/ttyUSB0',9600)

data = con.read(325)
for line in data.split('\n') :
	if line.startswith( '$GPRMC') :
		print(line)
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
		print(count)	
		print(lon)
		print(lat)
		print(time2)
		# calculating actual latitude from lat
		lat2 =int( int(lat) / 100)
		lat3 = lat - lat2*100
		latitude = lat2 +  lat3/60  
		print "latitude : " ,latitude
		#calculating actual longitude from lon
		if count==4 :
			factor = 100
		else:
			factor = 1000
		lon2 = int( int(lon)/factor)
		lon3 = lon - lon2*factor
		longitude = lon2 + lon3/60
		print "longitude : " ,longitude
		#converting time to hhmmss and integers
		hour =(int( time2/10000))  
		minute = int((time2 -( hour*10000))/100) 
		second = int( time2 - (hour*10000) - (minute*100))
		hour = hour + 5
		minute = minute + 30
		if minute > 59:
			minute = minute-60
		print "time:", hour, ":", minute, ":", second
		#calculating speed
		speed = speed*1.852
		print "speed : ", speed, "kmph"
		 
print(data)
print("\n\n")

