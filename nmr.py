'''
Some NMR calcs.
'''

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
	