from Recieve import *
from Decode import *
from Aircraft_Class import Aircraft
import GUI
import threading
from time import clock



total = 0
total17 = 0
fixed1 = 0
fixed2 = 0
Aircraft_List = {}
Json_To_Send = []

def Process_Sample(samples, rtlsdr_obj):

	# samples = Shift_Samples(samples)						#Shift the samples back to original 1090Mhz
	samples = np.sqrt(np.real(samples)**2 + np.imag(samples)**2)		#Convert from Complex Data to Mag^2
	# Plot_Samples(samples.tolist())
	packets = Extract_ModeS_Packets(samples)				#Get all the Mode-S Packets from the Sample

	global total,total17,Json_To_Send, Aircraft_List,fixed1,fixed2

	curtime = clock()
	for packet in packets:

		Binary_String = Sample_To_Binary(packet)

		Error_Tuple = Brute_Force_Errors(Binary_String)
		if(Error_Tuple == False):
			continue
		Binary_String = Error_Tuple[0]
		fixed1+=Error_Tuple[1]
		fixed2+=Error_Tuple[2]

		if(Binary_String == False):
			continue

		if (Check_DF(Binary_String) == 17):

			total17+=1

			if(not paritycheck(Binary_String)):
				continue

			Decoded_Packet = Decode_DF17(Binary_String)

			if(Decoded_Packet[1] == -2):
				continue

			if Aircraft_List.has_key(Decoded_Packet[0]):

				instance = Aircraft_List[Decoded_Packet[0]] #Get the 'Aircraft_Class' object
				instance.Update(Decoded_Packet,curtime)				#Update the object with new values
				instance.UpdateCounter()					#Update the counter of the object
				instance.UpdatePosition()					#Update the position of the object
				Aircraft_List.update({Decoded_Packet[0]: instance}) #Overwrite previous 'Aircraft_Class' object
			else:
				New_Aircraft = Aircraft(Decoded_Packet,curtime)					#create new 'Aircraft_Class' object
				Aircraft_List.update({Decoded_Packet[0]: New_Aircraft})	#update Aircraft_List with new plane
			

		total+=1

	Json_To_Send = []

	for i in Aircraft_List:
		if(Aircraft_List[i].Counter >= 1):

			Json_To_Send.append({"ICAO24":Aircraft_List[i].ICAO24,"ICAO":Aircraft_List[i].ICAO,"ALT":Aircraft_List[i].ALT,"Speed":Aircraft_List[i].Speed,"Heading":Aircraft_List[i].Heading,"Lat":Aircraft_List[i].Lat,"Lon":Aircraft_List[i].Lon})


	#######################################For GUI####
	Json_To_Send = json.dumps(Json_To_Send)
	f = open("GUI/data/planes.json", 'w')
	f.truncate()
	f.write(Json_To_Send)
	f.close
	##################################################

	os.system('clear')
	print "#####################"
	print "ICAO24\t\tICAO\tSpeed\tHeading\tAlt\tLat\tLon\tTime" 
	for i in Aircraft_List:
		if(curtime - Aircraft_List[i].Last_Time > 60):
			Aircraft_List.pop(i, None)
			continue

		if(Aircraft_List[i].Counter >= 1):
			print Aircraft_List[i].ICAO24,"\t", Aircraft_List[i].ICAO, "\t", Aircraft_List[i].Speed,"\t", int(Aircraft_List[i].Heading)  ,"\t", Aircraft_List[i].ALT, "\t", round(Aircraft_List[i].Lat,3), "\t",round(Aircraft_List[i].Lon,3), "\t",60 - int(curtime - Aircraft_List[i].Last_Time)
	print "#####################"
	print "Planes: ",len(Aircraft_List),"\t Total Messages: ",total,"\t Total DF17:", total17, "\t Fixed Messages: ", fixed1,fixed2
	print "#####################"


#Clear Json File
f = open("GUI/data/planes.json", 'w')
f.truncate()
f.close()


thread1 = threading.Thread(name='Init_SDR',target=Init_SDR, args=(Process_Sample,))

thread1.start()

GUI.Init_Server()
GUI.Init_GUI()


