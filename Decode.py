from math import sqrt,atan2,pi

Mode_S_Preamble_Length = 8
Mode_S_Data_Length = 112


def Sample_To_Binary(sample):
	binary_string = ''

	for i in range(0,Mode_S_Data_Length):
		first = sample[Mode_S_Preamble_Length*2 + i*2]
		second = sample[Mode_S_Preamble_Length*2 + i*2 + 1]

		if(first > second):
			binary_string += '1'
		elif(first < second):
			binary_string += '0'
		elif(first == second):
			binary_string += '2'

	return binary_string

def Brute_Force_One(binstring):

	String_0 = binstring.replace('2','0')
	if(paritycheck(String_0)):
		return String_0
	String_1 = binstring.replace('2','1')
	if(paritycheck(String_1)):
		return String_1
	return False


def Brute_Force_Two(binstring):


	String_00 = binstring.replace('2','0')
	if(paritycheck(String_00)):
		return String_00

	String_01 = binstring.replace('2','0',1).replace('2','1') 
	if(paritycheck(String_01)):
		return String_01

	String_10 = binstring.replace('2','1',1).replace('2','0') 
	if(paritycheck(String_10)):
		return String_10

	String_11 = binstring.replace('2','1')
	if(paritycheck(String_11)):
		return String_11
	
	return False





def Binary_To_Hex(binstring):
	tmp = int(binstring,2)
	return hex(tmp)

def Check_DF(binstring):
	return int(binstring[0:5],2)

def paritycheck(binarystring):
    poly = '111111111111010000001001'                              #CRC generator polynomial
    i = 23
    register = binarystring[0:24]                               # register of 24 bits, starting value

    # while loop which computes remainder of division of binary string by generator polynomial using CRC arithmetic

    while i < len(binarystring)-1:
        pop = register[:1]                                  # bit which is 'popped' out of the register
        i +=1
        register = register[1:24]+binarystring[i]     # shifts register to the right
        if  pop == '1':                                     # if a 1 is 'popped' out, we know that the current register is divisible by the gen. polynomial
            register = '{0:0{1}b}'.format(int(register,2)^int(poly,2),24)         # fills register with remainder, uses XOR to find remainder
 

    if '1' in register:                                     # if '1' in final register, remainder is not equal to zero and message is corrupted
        return False
    else:
        return True

def Decode_DF17(binstring):
	CA = binstring[5:8]
	ICAO24 = binstring[8:32]
	TC = binstring[32:37]
	DATA = binstring[32:88]
	PC = binstring[88:112]
	ICAO24_HEX = Binary_To_Hex(ICAO24)

	num_TC = int(TC,2)

	if (1 <= num_TC <= 4):  #ICAO 
		ICAO = ''
		Data_Offset = 8
		Mapping = '#ABCDEFGHIJKLMNOPQRSTUVWXYZ#####_###############0123456789######'
		index = int(DATA[Data_Offset+0:Data_Offset+6],2)
		ICAO += Mapping[index]
		index = int(DATA[Data_Offset+6:Data_Offset+12],2)
		ICAO += Mapping[index]
		index = int(DATA[Data_Offset+12:Data_Offset+18],2)
		ICAO += Mapping[index]
		index = int(DATA[Data_Offset+18:Data_Offset+24],2)
		ICAO += Mapping[index]
		index = int(DATA[Data_Offset+24:Data_Offset+30],2)
		ICAO += Mapping[index]
		index = int(DATA[Data_Offset+30:Data_Offset+36],2)
		ICAO += Mapping[index]
		index = int(DATA[Data_Offset+36:Data_Offset+42],2)
		ICAO += Mapping[index]
		index = int(DATA[Data_Offset+42:Data_Offset+48],2)
		ICAO += Mapping[index]

		if(ICAO.count('#') >=1): #Error Catch
			return (ICAO24_HEX,-2)

		return (ICAO24_HEX,"ICAO",ICAO.strip('_'))

	elif (9 <= num_TC <= 18): #Position

		EVEN = 0
		ODD = 1

		Data_Offset = 5
		SS = int(DATA[Data_Offset+0:Data_Offset+2],2)
		NICsb = int(DATA[Data_Offset+2:Data_Offset+3],2)
		ALT = int(DATA[Data_Offset+3:Data_Offset+10] + DATA[Data_Offset+11:Data_Offset+15],2)
		T = int(DATA[Data_Offset+15],2)
		F = int(DATA[Data_Offset+16],2)
		LAT_CPR = int(DATA[Data_Offset+17:Data_Offset+34],2)
		LON_CPR = int(DATA[Data_Offset+34:Data_Offset+51],2)
		Q_Bit = int(DATA[Data_Offset+10],2)


		if(Q_Bit == 0):
			H =  ALT * 100 - 1000
		else:
			H = ALT * 25 - 1000

		if(F == EVEN):
			return (ICAO24_HEX,"EVEN",LAT_CPR,LON_CPR,H)
			
		elif(F == ODD):
			return (ICAO24_HEX,"ODD",LAT_CPR,LON_CPR,H)

	elif (num_TC == 19): #Speed/Heading
		Data_Offset = 5
		SubType = int(DATA[Data_Offset+0:Data_Offset+3],2)
		IC = int(DATA[Data_Offset+3],2)
		RESV_A = int(DATA[Data_Offset+4],2)
		NAC = int(DATA[Data_Offset+5:Data_Offset+8],2)
		S_WE = int(DATA[Data_Offset+8],2)
		V_WE = int(DATA[Data_Offset+9:Data_Offset+19],2)
		S_NS = int(DATA[Data_Offset+19],2)
		V_NS = int(DATA[Data_Offset+20:Data_Offset+30],2)
		VrSrc = int(DATA[Data_Offset+30],2)
		S_Vr = int(DATA[Data_Offset+31],2)
		Vr = int(DATA[Data_Offset+32:Data_Offset+41],2)
		RESV_B = int(DATA[Data_Offset+41:Data_Offset+43],2)
		S_DIF = int(DATA[Data_Offset+43],2)
		DIF = int(DATA[Data_Offset+44:Data_Offset+51],2)
		
		if(V_WE == 0 or V_NS == 0):
	
			return(ICAO24_HEX,-2)

		if(S_WE == 0):
			S_WE = 1
		else:
			S_WE = -1
		if(S_NS == 0):
			S_NS = 1
		else:
			S_NS = -1

		if(SubType == 1 or SubType == 2):
			V_WE *= S_WE
			V_NS *= S_NS

			Speed = int(sqrt(V_WE ** 2 + V_NS ** 2))
			print ICAO24_HEX, V_WE, V_NS
			
			Heading = -1 * atan2(V_NS,V_WE) * (360/(2*pi)) + 90

			return (ICAO24_HEX,"Speed/Heading",Speed,Heading)

	else:
		return (ICAO24_HEX,-2)











		



