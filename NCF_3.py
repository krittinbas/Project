from smartcard.scard import *
from smartcard.util import toHexString
import smartcard.util
from smartcard.ATR import ATR
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import CardConnectionObserver
import time
import struct
import array
import json
import json
from newuser_Otp import newuser_Otp 


'''
RFID/NFC Reader/Writer: ACR122U-A9
Supported Frequency: 13.56MHz
Supported ISO: 14443-4A/B, ISO 18092.
Additional Supported Standards: Mifare, FeliCa, four types of NFC.
Documentation: http://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf


Definitions:
ISO/IEC 14443 Identification cards -- Contactless integrated circuit cards -- Proximity cards is an international standard that defines proximity cards used for identification, and the transmission protocols for communicating with it.
(ATR) Answer To Reset: is a message output by a contact Smart Card conforming to ISO/IEC 7816 standards, following electrical reset of the card's chip by a card reader.
PCD: proximity coupling device (the card reader)
PICC: proximity integrated circuit card


'''
VERBOSE = False

attributes = {
	SCARD_ATTR_ATR_STRING: 'SCARD_ATTR_ATR_STRING',
	SCARD_ATTR_CHANNEL_ID: 'SCARD_ATTR_CHANNEL_ID',
	SCARD_ATTR_CHARACTERISTICS: 'SCARD_ATTR_CHARACTERISTICS',
	SCARD_ATTR_CURRENT_BWT: 'SCARD_ATTR_CURRENT_BWT',
	SCARD_ATTR_CURRENT_CWT: 'SCARD_ATTR_CURRENT_CWT',
	SCARD_ATTR_CURRENT_EBC_ENCODING: 'SCARD_ATTR_CURRENT_EBC_ENCODING',
	SCARD_ATTR_CURRENT_F: 'SCARD_ATTR_CURRENT_F',
	SCARD_ATTR_CURRENT_IFSC: 'SCARD_ATTR_CURRENT_IFSC',
	SCARD_ATTR_CURRENT_IFSD: 'SCARD_ATTR_CURRENT_IFSD',
	SCARD_ATTR_CURRENT_IO_STATE: 'SCARD_ATTR_CURRENT_IO_STATE',
	SCARD_ATTR_DEFAULT_DATA_RATE: 'SCARD_ATTR_DEFAULT_DATA_RATE',
	SCARD_ATTR_DEVICE_FRIENDLY_NAME_A: 'SCARD_ATTR_DEVICE_FRIENDLY_NAME_A',
	SCARD_ATTR_DEVICE_FRIENDLY_NAME_W: 'SCARD_ATTR_DEVICE_FRIENDLY_NAME_W',
	SCARD_ATTR_DEVICE_SYSTEM_NAME_A: 'SCARD_ATTR_DEVICE_SYSTEM_NAME_A',
	SCARD_ATTR_DEVICE_SYSTEM_NAME_W: 'SCARD_ATTR_DEVICE_SYSTEM_NAME_W',
	SCARD_ATTR_DEVICE_UNIT: 'SCARD_ATTR_DEVICE_UNIT',
	SCARD_ATTR_ESC_AUTHREQUEST: 'SCARD_ATTR_ESC_AUTHREQUEST',
	SCARD_ATTR_EXTENDED_BWT: 'SCARD_ATTR_EXTENDED_BWT',
	SCARD_ATTR_ICC_INTERFACE_STATUS: 'SCARD_ATTR_ICC_INTERFACE_STATUS',
	SCARD_ATTR_ICC_PRESENCE: 'SCARD_ATTR_ICC_PRESENCE',
	SCARD_ATTR_ICC_TYPE_PER_ATR: 'SCARD_ATTR_ICC_TYPE_PER_ATR',
	SCARD_ATTR_MAXINPUT: 'SCARD_ATTR_MAXINPUT',
	SCARD_ATTR_MAX_CLK: 'SCARD_ATTR_MAX_CLK',
	SCARD_ATTR_MAX_DATA_RATE: 'SCARD_ATTR_MAX_DATA_RATE',
	SCARD_ATTR_POWER_MGMT_SUPPORT: 'SCARD_ATTR_POWER_MGMT_SUPPORT',
	SCARD_ATTR_SUPRESS_T1_IFS_REQUEST: 'SCARD_ATTR_SUPRESS_T1_IFS_REQUEST',
	SCARD_ATTR_USER_AUTH_INPUT_DEVICE: 'SCARD_ATTR_USER_AUTH_INPUT_DEVICE',
	SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE:
		'SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE',
	SCARD_ATTR_VENDOR_IFD_SERIAL_NO: 'SCARD_ATTR_VENDOR_IFD_SERIAL_NO',
	SCARD_ATTR_VENDOR_IFD_TYPE: 'SCARD_ATTR_VENDOR_IFD_TYPE',
	SCARD_ATTR_VENDOR_IFD_VERSION: 'SCARD_ATTR_VENDOR_IFD_VERSION',
	SCARD_ATTR_VENDOR_NAME: 'SCARD_ATTR_VENDOR_NAME',
}

BLOCK_NUMBER = 0x04
AUTHENTICATE = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x60, 0x00]

COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00]


SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]

GET_UID = [0xFF,0xCA,0x00,0x00,0x04]

READ_BYTES = [0xFF,0xB0,0x00,0x04,0x04]
WRITE_BLOCKS = [0xFF,0xD6,0x00,0x04,0x04,0xFF,0xFF,0xFF,0xFF] # Data are the last three items in the list.


READ_16_BINARY_BLOCKS = [0xFF,0xB0,0x00,0x04,0x10] # Read 16 bytes from the binary block 0x04h.
READ_4_BINARY_BLOCKS = [0xFF,0xB0,0x00,0x04,0x04] # Read 4 bytes from the binary block 0x04h.


NUMBER_BYTES_TO_UPDATE = 0x10
UPDATE_BLOCKS = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, NUMBER_BYTES_TO_UPDATE, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]


UPDATE_FIXED_BLOCKS = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, NUMBER_BYTES_TO_UPDATE]


UPDATE_BLOCKS_WITH_DATA = [0xFF, 0xD6, 0x00, BLOCK_NUMBER]
READ_BLOCKS_RECENTLY_UPDATED = [0xFF,0xB0,0x00,BLOCK_NUMBER]


class NFC_Reader():
	def __init__(self, uid = ""):
		self.uid = uid
		self.uid = ""
		self.hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
		self.hresult, self.readers = SCardListReaders(self.hcontext, [])
		assert len(self.readers) > 0
		self.reader = self.readers[0]
		print("Found reader: " +  str(self.reader))
		
		self.hresult, self.hcard, self.dwActiveProtocol = SCardConnect(
				self.hcontext,
				self.reader,
				SCARD_SHARE_SHARED,
				SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
		self.data_blocks = []

	def get_card_status(self):
		hresult, reader, state, protocol, atr = SCardStatus(self.hcard)
		print("Getting card status...")
		if hresult != SCARD_S_SUCCESS:
			raise error('failed to get status: ' + SCardGetErrorMessage(hresult))
		
		print ('Reader: ', reader)
		print ('State: ', state)
		print ('Protocol: ', protocol)
		print ('ATR: ',)
		for i in range(len(atr)):
			print ('0x%.2X' % i,)
		#print("\n")
		converted = toHexString(atr, format=0)
		print("\n------------------------")
		return converted


	def read_uid(self):
		value, self.uid = self.send_command(GET_UID)
		return(self.uid)

	def send_command(self, command):
		print("Sending command...")
		for iteration in range(1):
			try:
				self.hresult, self.response = SCardTransmit(self.hcard,self.dwActiveProtocol,command)
				value = toHexString(self.response, format=0)
				if(VERBOSE):
					print("Value: " + value +  " , Response:  " + str(self.response) + " HResult: " + str(self.hresult))
			except SystemError:
				print ("No Card Found")
			time.sleep(1)
		print("------------------------\n")
		return self.response, value


	def write_data(self, string):
		int_array = list(map(ord, string))
		#print("Writing data: " + str(int_array))

		# If the string is greater than 16 characters, break.
		if len(int_array) > 16:
			return

		# Replace the existing data in UPDATE_FIXED_BLOCKS with the new values
		UPDATE_FIXED_BLOCKS[5:] = int_array

		# Authenticate with the specified block with the APDU authenticate command.
		response, value = self.send_command(AUTHENTICATE)

		print("Writing " + string + " to card...")
		if response == [144, 0]:
			#print("Authentication successful.")

			if len(string) > 0:
				#print("Writing data blocks...")
				self.send_command(UPDATE_FIXED_BLOCKS)
			else:
				print("Please provide a valid string.")
		else:
			print("Unable to authenticate.")
		#print("------------------------\n")


	def read_data(self):
		response, value = self.send_command(AUTHENTICATE)
		print("Reading data from card...")
		if(response == [144, 0]):
			print("Authentication successful.")
			print("Reading data blocks...")
			result, value = self.send_command(READ_16_BINARY_BLOCKS)
			data_str = bytearray(result).decode('ascii', errors='ignore')

			if(VERBOSE):
				print("Value: " + value +  " , Response:  " + str(result))
			print("------------------------")
			return data_str 
		else:
			print("Unable to authenticate.")

	def monitor_cards(self):
		try:
			# พยายามเชื่อมต่อกับการ์ด
			self.hresult, self.hcard, self.dwActiveProtocol = SCardConnect(
				self.hcontext,
				self.reader,
				SCARD_SHARE_SHARED,
				SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
			

			if self.hresult == SCARD_S_SUCCESS :
				
				return SCARD_S_SUCCESS
				
				
				# ตัวอย่าง: อ่าน UID ของการ์ด
				# uid = reader.read_uid()
				# print(f"Card UID: {uid}")	
				
				# 2. Obtain the card status
				#reader.get_card_status()

				# 3. Read the UID
				#ivalue = reader.read_uid()
				#print("นำข้อมูลนี้ไปใช้ map กับ รหัสนิสิต : ",ivalue)

				# 4. Read the data from the card.
				# value = reader.read_data()
				# print("Read " + str(value) + " from the card.")

				# 5. Write a string to the byte blocks.
				# sad = int(input("enter money: "))
				# all = str(sad)
				# reader.write_data(all)

				# 6. Read the data blocks to verify they were written correctly.
				#value = reader.read_data()
				#print("Read " + str(value) + " from the card.")
				
			else:
				print("\nWaiting for a card...")
			

		except Exception as e:
			print("Error:", str(e))

		time.sleep(2.5)  # รอ 1 วินาทีก่อนที่จะตรวจจับอีกครั้ง

def changestr(ascii_char):
    getstr = ""
    unwanted_characters = ['#','♥','^','h','A','[', '_','~','$','U','F','t']
    for r in ascii_char:
        if r not in unwanted_characters:
            getstr += r
        else:
            break  # Correct indentation for the break statement
    return getstr


def clean_string(input_string):
    # ลบตัวอักษรพิเศษ '\x00' จากข้อความ
    clean_string = input_string.replace('\x00', '')
    return clean_string


def showmoney():
    value = reader.read_data()
    changed = str(value)
    cleaned_str = changestr(changed)
    print("ยอดเงินคงเหลือ " + cleaned_str + " บาท")

def reset_card_data():
    all_data = '0'  # Set the data to 0 for reset
    reader.write_data(all_data)
    print("บัตร NFC ได้รับการรีเซ็ตแล้ว")


def topup():
    ascii_dex = reader.read_data()
    ascii_char = int(clean_string(changestr(str(ascii_dex))))
    total = ascii_char + coin
    all_data = str(total)
    
    reader.write_data(all_data)
    
def buyitem():
    ascii_dex = reader.read_data()
    ascii_char = int(clean_string(changestr(str(ascii_dex))))
    total = ascii_char - buy
    if total < 0:
        print("เงินไม่เพียงพอที่จะซื้อสินค้า")
    else:
        all_data = str(total)
        reader.write_data(all_data)

if __name__ == '__main__':
    # 1. Create an NFC_Reader
    reader = NFC_Reader()
    state = True
    n = 1
    while state:
        check = reader.monitor_cards()
        if check == 0 and n == 1:
            print("------------------------")
            print("\nCard connected!")
            uid = reader.read_uid()
            print(f"Card UID: {uid}")
            print(type(uid))
            with open("data.json", "r") as file:
                data = json.load(file)
                print("...")
                for user in data['USER']:
                    if user['UID'] == uid:
                        print(user['UserName'])
                        while True:
                            # value = reader.read_data()
                            # changed = str(value)
                            # cleaned_str = changestr(changed)
                            print("กรุณาเลือกการดำเนินการ")
                            showmoney()
							# print("ยอดเงินคงเหลือ " + cleaned_str + " บาท")
                            print("1: เติมเงิน")
                            print("2: ซื้อของ")
                            print("3: ออก")
                            choices = input("Enter choice (1/2/3): ")
                            if choices == '1':
                                while True:
                                    try:
                                        coin = int(input("กรุณาใส่จำนวนเงิน: "))
                                        break  # If input is a number, exit the loop
                                    except ValueError:
                                        print("กรุณากรอกเป็นตัวเลขเท่านั้น")
                                # ascii_dex = reader.read_data()
                                # ascii_char = str(ascii_dex)
                                # num_char = changestr(ascii_char)
                                # cleaned_str = clean_string(num_char)
                                # lastnum = int(cleaned_str)
                                # total = lastnum + coin
                                # all_data = str(total)
                                # reader.write_data(all_data)
                                topup()
                            elif choices == '2':
                                while True:
                                    try:
                                        buy = int(input("กรุณาใส่ราคาของสินค้าทั้งหมด: "))
                                        break  # If input is a number, exit the loop
                                    except ValueError:
                                        print("กรุณากรอกเป็นตัวเลขเท่านั้น")
                                # ascii_dex = reader.read_data()
                                # ascii_char = str(ascii_dex)
                                # num_char = int(clean_string(changestr(ascii_char)))
                                # cleaned_str = clean_string(num_char)
                                # lastnum = int(cleaned_str)
                                # total = lastnum - buy
                                # all_data = str(total)
                                # reader.write_data(all_data)
                                buyitem()
                            elif choices == '3':
                                print("ออกจากระบบ")
                                break
                            elif choices == '5':
                                reset_card_data()
                            else:
                                print("ไม่พบตัวเลือกในการดำเนินการ, กรุณาลองใหม่...")
                        n = 0
                        break   
                else:
                    newuser_Otp(uid)
        elif check != 0:
            n=1