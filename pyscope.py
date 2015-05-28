
import visa
import logging

class Scope(visa.Instrument):
	
	default_name = 'Scope'

	def __init__(self, resource_name, **keyw):
		self.PopKeywords(keyw)
		visa.Instrument.__init__(self, resource_name, **keyw)
		# start log
		self.log = logging.getLogger(self.name)
		self.log.setLevel(self.loglevel)
		if self.logfile != None:
			hdlr = logging.FileHandler(self.logfile)
			formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
			hdlr.setFormatter(formatter)
			self.log.addHandler(hdlr)
		self.ConfigureComms()
		self.GetHorizontalSettings()
	
	def PopKeywords(self, keyw):
		loglevels = {'debug':    logging.DEBUG,
		             'info':     logging.INFO,
		             'warning':  logging.WARNING,
		             'error':    logging.ERROR,
		             'critical': logging.CRITICAL}
		self.name = keyw.pop('name', self.default_name)
		self.logfile = keyw.pop('logfile',  None)
		lvl = keyw.pop('loglevel', 'info')
		if lvl not in loglevels.iterkeys():
			lvl = 'info'
		self.loglevel = loglevels[lvl]
		
	def ConfigureComms(self):
		#Generic all model configure the scope hardcopy settings
		self.log.info('Configuring comms...')
		self.reclen = self.ask('horizontal:recordlength?')
		self.write('header off')
		self.write('VERBOSE OFF')
		self.write('data:start 0')
		self.write('data:stop 10000000')
		self.write('data:encdg ribinary')
		self.write('wfmo:byt_n 2')
		
	def GetHorizontalSettings(self):
		self.log.info('Reading horizontal scale...')
		
		# returned record length?
		self.reclen = self.ask("horizontal:recordlength?")
		self.log.debug('reclen: ' + self.reclen)
		
		# time base horizontal scale?
		self.hscale = float(self.ask("horizontal:scale?"))
		self.log.debug('hscale: {0}'.format(self.hscale))
		
		# horizontal delay time ? (used when delay is on)
		self.hdelay = float(self.ask("horizontal:delay:time?"))
		self.log.debug('hdelay: {0}'.format(self.hdelay))
		
		# horizontal position? (in percent, used when delay if off)
		self.hpos = float(self.ask("horizontal:position?"))
		self.log.debug('hpos: {0}'.format(self.hpos))
		
		# sampling inteval?
		#self.xincr = float(self.ask("wfmoutpre:xincr?"))
		#self.log.debug('xincr: {0}'.format(self.xincr))

		# write time domain axis (x-axis)
		#self.x = [(t-int(self.reclen)*self.hpos/100)*self.xincr + self.hdelay for t in range(int(self.reclen))]
		#self.log.debug('x-axis written, {0} elements, min={1}, max={2}'.format(len(self.x), self.x[0], self.x[len(self.x)-1]))
	
	def GetVerticalSettings(self, channel='CH1'):
		self.log.info('Reading vertical scale...')
		
		# Some commands will timeout and fail if channel is not turned on.
		if int(self.ask('select:{0}?'.format(channel))) == 0:
			ch1off = True
			self.write('select:{0} on'.format(channel))
		else:
			ch1off = False
			
		# Set data source
		self.write('data:sour {0}'.format(channel))
		
		# vertical scale factor per digitizing level?
		self.ymult = float(self.ask("wfmoutpre:ymult?"))
		self.log.debug('ymult: {0}'.format(self.ymult))
		
		# vertical position in digitizing levels?
		self.yoff = float(self.ask("wfmoutpre:yoff?"))
		self.log.debug('yoff: {0}'.format(self.yoff))
		
		# vertical offset? (usually zero)
		self.yzero = float(self.ask("wfmoutpre:yzero?"))	
		self.log.debug('yzero: {0}'.format(self.yzero))
		
		# return channel to original state
		if ch1off == True:
			self.write('select:{0} off'.format(channel))

	def yread_raw(self, channel='CH1'):
		'''read y data - integer list, not scaled, or shifted'''
		from struct import unpack
		
		# setup scope and get curve settings
		recLenNumBytes = len(self.reclen)
		headerLen = 1 + 1 + recLenNumBytes
		
		# get channel data
		self.write('data:sou ' + channel)
		self.write('sel:' + channel + ' ON')
		wave = self.ask('curve?')
		
		# unpack raw data
		# format = "#{6}{100000}{data...."
		byt_n = 2
		ndigits = int(wave[1])
		ndata = int(wave[2:2+ndigits])
		wave = wave[2+ndigits:2+ndigits+ndata]
		wave = unpack('>' + str(ndata/byt_n) + 'h',wave)
		
		return wave
	
	def yread_int(self, channel='CH1'):
		'''read y data - integer list, shifted, not scaled'''
		wave = self.yread_raw(channel)
		return [i-self.yoff for i in wave]
		
	def yread_float(self, channel='CH1'):
		'''read y data - integer list, scaled and shifted'''
		wave = self.yread_raw(channel)
		return [(i-self.yoff) * self.ymult + self.yzero for i in wave]

	def RawToInt(self, wave):
		'''Convert waveform'''
		return [r-self.yoff for r in wave]
		
	def RawToFloat(self, wave):
		'''Convert waveform'''
		return [(r-self.yoff) * self.ymult + self.yzero for r in wave]
		
	def IntToFloat(self, wave):
		'''Convert waveform'''
		return [i * self.ymult + self.yzero for i in wave]	
		
	def IntToRaw(self, wave):
		'''Convert waveform'''
		return [i+self.yoff for i in wave]
		
	def FloatToRaw(self, wave):
		'''Convert waveform'''
		return [(f-self.yzero) / self.ymult + self.yoff for f in wave]
		
	def FloatToInt(self, wave):
		'''Convert waveform'''
		return [(f-self.yzero) / self.ymult for f in wave]
		
