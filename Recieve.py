from rtlsdr import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

BASE_STATION = int(1090e6)
BASE_SAMPLES = 2000000
BASE_SHIFT = 250000
BASE_FEQ = BASE_STATION - BASE_SHIFT
BASE_SAMPLEAMOUNT = 3200*16



	
def test_callback(samples, rtlsdr_obj):
	return



sdr = RtlSdr()

# configure device
sdr.sample_rate = BASE_SAMPLES  # Hz
sdr.center_freq = BASE_FEQ    # Hz
sdr.set_freq_correction(130)

print sdr.get_freq_correction()
sdr.gain = 'auto'

samples = sdr.read_samples(BASE_SAMPLEAMOUNT)




x1 = np.array(samples).astype('complex64')
fc1 = np.exp(-1.0j*2.0*np.pi* BASE_SHIFT/BASE_SAMPLES*np.arange(len(x1)))
# Now, just multiply x1 and the digital complex expontential
x2 = x1 * fc1 

x3 = np.real(x2)**2 + np.imag(x2)**2
print len(x3)

m = x3
j = []
for i in range(len(m)-56):
  if( m[i+1] < m[i] and m[i+2] > m[i+1] and m[i+2] > m[i+3] and m[i+3] < m[i] and m[i+4] < m[i] and m[i+5] < m[i] and m[i+6] < m[i] and m[i+7] > m[i+6] and m[i+8] < m[i+7]):
    for k in range(0,19):

      j.append(m[i+k])


plt.plot(j)
# plt.subplot(211)
# plt.psd(x3,NFFT=2048, Fs=BASE_SAMPLES)

# plt.subplot(212)
# plt.specgram(x2,NFFT=2048, Fs=BASE_SAMPLES)
# plt.title("x1")  
# plt.ylim(-BASE_SAMPLES/2, BASE_SAMPLES/2)







# x = np.linspace(start=-10, stop=10,num=101)
# plt.plot(x,x3)
# plt.show

# An FM broadcast signal has  a bandwidth of 200 kHz
# f_bw = 200000  
# dec_rate = int(BASE_SAMPLES / f_bw)  
# x4 = signal.decimate(x2, dec_rate)  
# # Calculate the new sampling rate
# Fs_y =  BASE_SAMPLES/dec_rate 


# plt.specgram(x1, NFFT=2048, Fs=BASE_SAMPLES)  
# plt.title("x1")  
# plt.ylim(-BASE_SAMPLES/2, BASE_SAMPLES/2)


# plt.specgram(x2, NFFT=2048, Fs=BASE_SAMPLES)  
# plt.title("x2")  
# plt.xlabel("Time (s)")  
# plt.ylabel("Frequency (Hz)")  
# plt.ylim(-BASE_SAMPLES/2, BASE_SAMPLES/2)  
# plt.xlim(0,len(x2)/BASE_SAMPLES)  
# plt.ticklabel_format(style='plain', axis='y' )  

# plt.specgram(x4, NFFT=2048, Fs=Fs_y)  
# plt.title("x4")  
# plt.ylim(-Fs_y/2, Fs_y/2)  
# plt.xlim(0,len(x4)/Fs_y)  
# plt.ticklabel_format(style='plain', axis='y' )  

### Polar discriminator
# y5 = x4[1:] * np.conj(x4[:-1])  
# x5 = np.angle(y5)  


# plt.psd(x5, NFFT=2048, Fs=Fs_y, color="blue")  
# plt.title("x5")  
# plt.axvspan(0,             15000,         color="red", alpha=0.2)  
# plt.axvspan(19000-500,     19000+500,     color="green", alpha=0.4)  
# plt.axvspan(19000*2-15000, 19000*2+15000, color="orange", alpha=0.2)  
# plt.axvspan(19000*3-1500,  19000*3+1500,  color="blue", alpha=0.2)  
# plt.ticklabel_format(style='plain', axis='y' ) 

plt.show()