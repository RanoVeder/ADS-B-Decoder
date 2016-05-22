from rtlsdr import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from Decode import *
from Aircraft_Class import Aircraft
import os
import json
import sys
BASE_STATION = int(1090e6) 				#Frequency of ADS-B Signals
BASE_SAMPLES = 2000000					#Amount of Samples per Second
BASE_SHIFT = 200000				#Shift of Frequency, Because of DC Spike
BASE_FEQ = BASE_STATION - BASE_SHIFT	#New Frequency with Shift
BASE_SAMPLEAMOUNT = 32000*16	#Samples taken before calling The CallBack Function


##################################################################
###                                                            ###
###                                                            ### 
#########################Debug Functions##########################

def Plot_Samples(samples):
	l = []
	for i in samples:
		for j in i:
			l.append(j)

	plt.plot(l)
	plt.show()

def Plot_FFT(samples):
	plt.specgram(samples)
	plt.show()

#################################################################

####################UTILITY FUNCTIONS############################


def Shift_Samples(samples):

	samples = np.array(samples).astype('complex64')										#Specify Numpy Array for the Complex Samples
	shift = np.exp(-1.0j*2.0*np.pi* BASE_SHIFT/BASE_SAMPLES*np.arange(len(samples)))	#Shift the Samples (https://en.wikipedia.org/wiki/Discrete_Fourier_transform)
	samples = samples * shift 															#Update 'samples' with the Shifted Samples
	return samples

def Differ_By_1(str1,str2):

	if len(str1) == len(str2):
	    count_diffs = 0
	    for a, b in zip(str1, str2):
	        if a!=b:
	            count_diffs += 1
	            if count_diffs > 1:
	            	return False

	    return True


################################################################
#INIT 

def Init_SDR(callback):
	try:
		sdr = RtlSdr()	#Initialize the RTL Dongle
	except:
		print "Couldn't find RTL2832U!"
		os._exit(1)												
		sys.exit(0)

	sdr.sample_rate = BASE_SAMPLES  								#Set the Sample Rate for Dongle
	sdr.center_freq = BASE_FEQ
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


