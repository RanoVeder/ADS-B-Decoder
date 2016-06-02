from rtlsdr import *
import numpy as np
from Decode import *
from Aircraft_Class import Aircraft
import os
import json
import sys
BASE_STATION = int(1090e6) 				#Frequency of ADS-B Signals
BASE_SAMPLES = 2000000					#Amount of Samples per Second
BASE_SAMPLEAMOUNT = 32000*16	#Samples taken before calling The CallBack Function


##################################################################
###                                                            ###
###                                                            ### 
#########################Debug Functions##########################


def BinString_Saver(binstring):
	f = open('DATA.txt', 'a')
	f.write(binstring +' '+ Binary_To_Hex(binstring[8:32]) + '\n')
	f.close()


#################################################################

####################UTILITY FUNCTIONS############################


def Brute_Force_Errors(binstring):
	fixed1 = 0
	fixed2 = 0
	Error_Counter = binstring.count('2')

	if(Error_Counter > 2):
		return False

	elif(Error_Counter == 1): 
		binstring = Brute_Force_One(binstring)
		if(binstring == False):
			return False
		fixed1+=1

	elif(Error_Counter == 2):
		binstring = Brute_Force_Two(binstring)
		if(binstring == False):
			return False
		fixed2+=1


	return (binstring,fixed1,fixed2)





################################################################
#INIT 

def Init_SDR(callback):
	try:
		sdr = RtlSdr()	#Initialize the RTL Dongle
	except:
		print "Couldn't find RTL2832U!"
		os._exit(1)												
		# sys.exit(0)

	sdr.sample_rate = BASE_SAMPLES  								#Set the Sample Rate for Dongle
	sdr.center_freq = BASE_STATION
	sdr.set_freq_correction(130)     								#Set the Frequency for Dongle
	sdr.gain = 49.6
	
	print "Frequency Set To: ",sdr.get_center_freq()
	print "Gain Set To: ",sdr.get_gain()

	try:
		sdr.read_samples_async(callback,BASE_SAMPLEAMOUNT)		#Start Capturing Samples Asynchronously
	except:
		print "Problem with RTL2832U, Please Restart"
		os._exit(1)
	return


	
#################################################################
#Packet Checking


def Extract_ModeS_Packets(samples):

	packets = []																		#Main Array that Will Contain all the Mode-S Signals

	for i in range(len(samples) - (112*2 + 8*2) -1):									#Loop Through each index in 'samples' and check if that's the start of a preamble

		highval = (samples[i] + samples[i+2] + samples[i+7] + samples[i+9])/float(4)	#Set The 
		
		if(highval < 0.05):
			continue


		if(samples[i] > samples[i+1] and\
			samples[i+1] < samples[i+2] and\
			samples[i+1] < highval and\
			samples[i+2] > samples[i+3] and\
			samples[i+3] < highval and\
			samples[i+4] < highval and\
			samples[i+5] < highval and\
			samples[i+6] < highval and\
			samples[i+6] < samples[i+7] and\
			samples[i+7] > samples[i+8] and\
			samples[i+8] < samples[i+9] and\
			samples[i+8] < highval and\
			samples[i+9] > samples[i+10] and\
			samples[i+10] < highval and\
			samples[i+11] < highval and\
			samples[i+12] < highval and\
			samples[i+13] < highval and\
			samples[i+14] < highval and\
			samples[i+15] < highval):

			packet = []
			
			for k in range(0,112*2 + 8*2):

				packet.append(samples[i+k])

			packets.append(packet)

	return packets


