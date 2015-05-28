def create_mif(data, signed=True, bits=8, arx='uint', drx='int'):

	from bitstring import BitArray
	from numpy import ceil
	
	radix = { 'bin':'BIN', 'hex':'HEX', 'oct':'OCT', 'int':'DEC', 'uint':'UNS' }

	mif = ""
	mif = mif + "WIDTH={0:d};\r\n".format(bits)
	mif = mif + "DEPTH={0:d};\r\n\r\n".format(len(data))
	mif = mif + "ADDRESS_RADIX={0};\r\n".format(radix[arx])
	mif = mif + "DATA_RADIX={0};\r\n\r\n".format(radix[drx])
	mif = mif + "CONTENT BEGIN\r\n"

	
	if (signed == True):
		for i in range(len(data)):
			data[i] = BitArray(length=bits, int=data[i])
	else:
		for i in range(len(data)):
			data[i] = BitArray(length=bits, uint=data[i])
	
	
	if (drx == 'oct'):
		extra_bits = int(3 * ceil(bits / 3.)) - bits
	elif (drx == 'hex'):
		extra_bits = int(4 * ceil(bits / 4.)) - bits
	else:
		extra_bits = 0


	bits = (len(data)-1).bit_length()
	if (arx == 'oct'):
		bits = int(3 * ceil(bits / 3.))
	if (arx == 'hex'):
		bits = int(4 * ceil(bits / 4.))

	addr = [BitArray(length=bits, uint=i) for i in range(len(data))]

	for i in range(len(data)):
		mif = mif + ("	{0." + arx + ":>8}  :   {1." + drx + ":>8};\r\n").format(addr[i], ([0,]*extra_bits + data[i]))

	mif = mif + "END;\r\n";

	return mif
	
def create_lut(data, signed=True, bits=8, arx='uint', drx='int'):

	from bitstring import BitArray
		
	print("rom : process")
	print("begin")
	print("\twait until rising_edge(clk);")
	print("\tcase (addr) is")
	
	if (signed == True):
		for i in range(len(data)):
			data[i] = BitArray(length=bits, int=data[i])
	else:
		for i in range(len(data)):
			data[i] = BitArray(length=bits, uint=data[i])

	bits = (len(data)-1).bit_length()

	addr = [BitArray(length=bits, uint=i) for i in range(len(data))]

	for i in range(len(data)):
		print(('\t\twhen "{0.' + arx + '}" => q <= "{1.' + drx + '}";').format(addr[i], data[i]))

	print("\tend case;")
	print("end process rom;")
	
