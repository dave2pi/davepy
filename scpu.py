



class scpu(object):

	def __init__(self, reg_init=None, ram_init=None, z_init=None, c_init=None, port_init=None):
		if reg_init != None:
			self.r = reg_init
		else:
			self.r = [0,]*16
			
		if ram_init != None:
			self.m = [0,]*256
		else:
			self.m = ram_init
			
		if z_init != None:
			self.z = z_init
		else:
			self.z = False
			
		if c_init != None:
			self.c = c_init
		else:
			self.c = False
			
		if port_init != None:
			self.port = port_init
		else
			self.port = [chr(0),]*256
			
	
	def args(y, k)
		if k == None:
			return self.r[y]
		elif y == None:
			return k
	
	def mov(x, y, k):
		self.r[x] = self.args(y, k)
	
	def in_(x, y, k)
		self.r[x] = self.port[self.args(y, k)]

	def ld(x, y, k):
		self.r[x] = self.m[self.args(y, k)]
		
	def and_(x, y, k):
		self.r[x] &= self.args(y, k)
		self.z = (self.r[x] == 0x00)
		self.c = False
	
	def or_(x, y, k):
		self.r[x] |= self.args(y, k)
		self.z = (self.r[x] == 0x00)
		self.c = False
	
	def xor(x, y, k):
		self.r[x] ^= self.args(y, k)
		self.z = (self.r[x] == 0x00)
		self.c = False
	
	def _xor_byte(b):
		mask = 0x01
		r = False
		for i in range(8):
			r ^= bool(mask << i & b)
		return r
		
	def tst(x, y, k):
		rx = self.r[x] & self.args(y, k)
		self.z = (rx == 0x00)
		self.c = _xor_byte(rx)
	
	def cmp(x, y, k):
		
	