'''
Some NMR calcs.
'''

gamma = 42.58E6

def probe_tune(l, ca, cb, cc):
	'''
	Calculate resonant frequency of probe.
	|| = parallel
	_ = series
	circuit = l || ca || (cb _ cc)
	'''
	from basic import cap_series
	from filters import lc_f
	c = sum((cap_series(cb, cc), ca))
	return lc_f(l, c)
	
def match_inductor(f, ca, cb, cc):
	'''
	Calculate matching inductance required for a given 
	set of matching capacitors.
	'''
	from math import pi
	from basic import x_capacitor as xcap
	xa = xcap(ca, f)
	xb = xcap(cb, f)
	xc = xcap(cc, f)
	return 2*-1*((xa+2*xb)*xc)/(4*pi*f*(xa+2*xb+xc))

def lamour_f(b):
	return gamma*b
	
def lamour_b(f):
	return f/gamma

def spectral_window(b_rf):
	b1 = b_rf/2.0
	omega = lamour_f(b1) / 10
	return omega
	
def t90(b1):
	w1 = lamour_f(b1)
	return 0.25 / w1
	
def t180(b1):
	w1 = lamour_f(b1)
	return 0.5 / w1

def stats_for_i(i):
	from si_prefix import si
	from magnetics import air_coil_B_field as field
	brf = field(i, 50, 0.110)
	b1 = brf/2.0
	omega = spectral_window(b1)
	t_90 = t90(b1)
	t_180 = t180(b1)
	n = 10
	print 'brf:'.rjust(n), si(brf)
	print 'b1:'.rjust(n), si(b1)
	print 'omega:'.rjust(n), si(omega)
	print 't90:'.rjust(n), si(t_90)
	print 't180:'.rjust(n), si(t_180)
	