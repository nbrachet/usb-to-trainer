# simple test program 
# generating packets
# for the arduino board

import sys, serial
import time

BAUDRATE = 115200

# serial port number
# python numbering starts from 0: COM68 -> 67
SERPORT = 79

channels = 1500, 1500, 1500, 1500, 1500, 1500

count = 5 + len(channels) * 2

packet = bytearray()
packet.append(0x01) # start byte
packet.append(count) # length
packet.append(0x01) # type

for ch in channels:
	b = (ch & 0x000000ff)
	packet.append(b)
	b = (ch & 0x0000ff00) >> 8
	packet.append(b)

checksum = 0

for p in packet:
    checksum += p

packet.append(checksum & 0x000000FF) # leave only lower checksum byte
packet.append(0x04) # end byte


for b in packet:
	sys.stdout.write(format(b, '02x'))
	sys.stdout.write(' ')

port = SERPORT

try:
	ser = serial.Serial(port, BAUDRATE)
	ser.flushInput()
	#ser = serial.Serial(port, BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

except Exception, e:
	print e		
	exit(1)	

ser.write(packet)	

ser.flush()
ser.close()		