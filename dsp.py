import scipy.signal as signal
import cmath
import pylab as pl 
from scipy.signal import freqz

def filter_length(fs, f, c1, c2, dB=True):
	nyq = fs/2
	fc = float(f)/nyq
	leg_p = []
	leg_l = []
	for i in range(5, 13):
		n = 2**i-1
		h = signal.firwin(n, cutoff=fc, window='hamming')
		w, H = signal.freqz(h, 1, 4096)
		if dB:
			H = 20 * pl.log10 (abs(H[:]))
		else:
			H = abs(H[:])
		p, = pl.plot(nyq*w/pl.pi, H)
		leg_p.append(p)
		leg_l.append('n={0}'.format(n))
	pl.legend(leg_p, leg_l)
	pl.axvline(x=c1, linewidth=1, color='k', ls='-')
	pl.axvline(x=c2, linewidth=1, color='k', ls='-')
	
def view_filter(h, fp=None, fs=None):
	'''view filter'''
	w, H = signal.freqz(h,1)
	H_phase = pl.unwrap([pl.degrees(cmath.phase(H[i])) for i in range(len(H))], 180)
	H = 20 * pl.log10 (abs(H[:]))
	x = range(0,len(h))
	step = pl.cumsum(h)
	
	pl.figure(figsize=(16, 6.6), dpi=80)
	
	pl.subplot(221)
	pl.stem(x, h)
	pl.ylabel('Amplitude')
	pl.xlabel(r'n (samples)')
	pl.title(r'Impulse response')
	pl.text(0.2, 0.7, 'N_taps = {0}'.format(len(h)))
	
	pl.subplot(222)
	pl.stem(x, step)
	pl.ylabel('Amplitude')
	pl.xlabel(r'n (samples)')
	pl.title(r'Step response')	

	pl.subplot(223)
	pl.plot(w/(2.0*pl.pi), H)
	pl.ylabel('Magnitude (db)')
	pl.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
	pl.title(r'Frequency response')
	if fp != None:
		pl.axvline(fp, linewidth=1, color='k', ls='-')
	if fs != None:
		pl.axvline(fs, linewidth=1, color='k', ls='-')
	
	pl.subplot(224)
	pl.plot(w/(2.0*pl.pi), H_phase)
	pl.ylabel('Phase (radians)')
	pl.xlabel(r'Normalized Frequency (Hz)')
	pl.title(r'Phase response')
	
def view_freq(h, fp=None, fs=None, log=True):
	'''view filter'''
	w, H = signal.freqz(h,1)
	H = abs(H[:])
	if log == True:
		H = 20 * pl.log10(H[:])
	
	pl.figure(figsize=(16, 6.6), dpi=80)
	
	pl.subplot(111)
	pl.plot(w/(2.0*pl.pi), H)
	pl.ylabel('Magnitude (db)')
	pl.xlabel(r'Normalized Frequency (Hz)')
	pl.title(r'Frequency response')
	if fp != None:
		pl.axvline(fp, linewidth=1, color='k', ls='-')
	if fs != None:
		pl.axvline(fs, linewidth=1, color='k', ls='-')

def remez(numtaps, bands, desired, weight=None, Hz=1, type='bandpass', maxiter=25, grid_density=16, numtaps_max=256):
	from scipy.signal.fir_filter_design import remez as _remez
	try:
		return _remez(numtaps, bands, desired, weight=weight, Hz=Hz, type=type, maxiter=maxiter, grid_density=grid_density)
	except:
		N = []
		for n in range(0, numtaps_max+1):
			try:
				h = _remez(n, bands, desired, weight=weight, Hz=Hz, type=type, maxiter=maxiter, grid_density=grid_density)
				N.append(n)
			except:
				pass
		print 'Did not converge for {0} taps.'.format(numtaps)
		print 'Will converge for the following:'
		print N
