import os
import sys
import logging

def calc_crc16(string):
		data = bytearray.fromhex(string)
		logging.info(type(data))
		crc = 0xFFFF
		for pos in data:
				crc ^= pos
				for i in range(8):
						if((crc & 1) != 0):
								crc >>= 1
								crc ^= 0xA001
						else:
								crc >>= 1

		return ((crc & 0xff) << 8) + (crc >> 8)
if ( __name__ == '__main__' ):
    data=input()
    # data_int=data.encode().hex()
    crc=calc_crc16(data)
    print(hex(crc))