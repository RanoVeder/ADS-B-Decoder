
import math


def NLC(lat):
	# return int( pi*2* ( acos(1 - (1-cos((pi)/(2*60)))/(cos((pi*2*lat)/(180))**2)  )**-1 )    )
	
	nz = 60
	a = 1 - math.cos(math.pi * 2 / nz)
	b = math.cos(math.pi / 180.0 * abs(lat)) ** 2
	nl = 2 * math.pi / (math.acos(1 - a/b))
	return int(nl)





class Aircraft:
	Lat = 0
	Lon = 0
	Lat_Even = 0
	Lat_Odd = 0
	Lon_Even = 0
	Lon_Odd = 0
	Speed = 0
	Heading = 0
	ICAO = 'N/A'
	ICAO24 = ''
	ALT = 0
	Counter = 0
	Last_Pos = ''   #"ODD" or "EVEN"
	Passed = False
	Last_Time = 0



	def __init__(self, tuple,time):
		 
		#index1 , 1:ICAO, 2:latlon, 3:Speed,Heading
		if(tuple[1] == 'ICAO'):
			self.ICAO = tuple[2]
		elif(tuple[1] == "Height"):
			self.ALT = tuple[2]
		elif(tuple[1] == "EVEN"):
			self.Lat_Even = tuple[2]
			self.Lon_Even = tuple[3]
			self.ALT = tuple[4]
			self.Last_Pos = "EVEN"
			self.Passed = True
		elif(tuple[1] == "ODD"):
			self.Lat_Odd = tuple[2]
			self.Lon_Odd = tuple[3]
			self.ALT = tuple[4]
			self.Last_Pos = "ODD"
			self.Passed = True
		elif(tuple[1] == "Speed/Heading"):
			self.Speed = tuple[2]
			self.Heading = tuple[3]


		self.ICAO24 = tuple[0]
		self.Counter += 1
		self.Last_Time = time

	def Update(self,tuple,time):
		#index1 , 1:ICAO, 2:latlon, 3:Speed,Heading
		if(tuple[1] == 'ICAO'):
			self.ICAO = tuple[2]
		elif(tuple[1] == "Height"):
			self.ALT = tuple[2]
		elif(tuple[1] == "EVEN"):
			self.Lat_Even = tuple[2]
			self.Lon_Even = tuple[3]
			self.ALT = tuple[4]
			self.Last_Pos = "EVEN"
			self.Passed = True
		elif(tuple[1] == "ODD"):
			self.Lat_Odd = tuple[2]
			self.Lon_Odd = tuple[3]
			self.ALT = tuple[4]
			self.Last_Pos = "ODD"
			self.Passed = True
		elif(tuple[1] == "Speed/Heading"):
			self.Speed = tuple[2]
			self.Heading = tuple[3]


		self.Last_Time = time


	def UpdateCounter(self):
		self.Counter += 1

	def UpdatePosition(self):

		if(self.Passed == False):
			return

		const = 131072.
		if(self.Lat_Even == 0 or self.Lat_Odd == 0 or self.Lon_Even == 0 or self.Lat_Odd == 0):

			return
		Lat_Even_Dec = self.Lat_Even/const
		Lat_Odd_Dec = self.Lat_Odd/const
		Lon_Even_Dec = self.Lon_Even/const
		Lon_Odd_Dec = self.Lon_Odd/const

		Lat_Index = math.floor(59* Lat_Even_Dec - 60 * Lat_Odd_Dec + 0.5)
		Lat_Even_Rel = 360/60.
		Lat_Odd_Rel = 360/59.

		Lat_Even_F = Lat_Even_Rel * (((Lat_Index%60)) + Lat_Even_Dec)
		Lat_Odd_F = Lat_Odd_Rel * (((Lat_Index%59)) + Lat_Odd_Dec)
		if(Lat_Even_F >= 270):
			Lat_Even_F -= 360
		if(Lat_Odd_F >= 270):
			Lat_Odd_F -= 360

		if(NLC(Lat_Even_F) != NLC(Lat_Odd_F)):
			return

		if(self.Last_Pos == "EVEN"):
			NL = NLC(Lat_Even_F)
			ni = NL-0
			if(ni<1):
				ni = 1
			Lon_Index = math.floor(Lon_Even_Dec*(NL-1)-Lon_Odd_Dec*NL + 0.5)
			Lon_F = (360./ni)*((Lon_Index%ni)+Lon_Even_Dec)

			if(Lon_F >= 180):
				Lon_F -= 360

			self.Lat = Lat_Even_F
			self.Lon = Lon_F
			self.Passed = False

		elif(self.Last_Pos == "ODD"):
			NL = NLC(Lat_Odd_F)
			ni = NL-1
			if(ni<1):
				ni = 1
			Lon_Index = math.floor(Lon_Even_Dec*(NL-1)-Lon_Odd_Dec*NL + 0.5)
			Lon_F = (360/ni)*((Lon_Index%ni)+Lon_Odd_Dec)
			
			if(Lon_F > 180):
				Lon_F -= 360

			self.Lat = Lat_Odd_F
			self.Lon = Lon_F
			self.Passed = False





