
from nmr import *

# These are some values calculated in mathcad 
# using different seed values and target frequencies
cset = [
#     ca          cb          cc
# f = 1022k									# Seed values:
(5.13723e-10, 1.57e-12,    1.04512e-10),	# 100p,  100p,  100p
(5.09152e-10, 6.21e-12,    4.13438e-10),	# 1000p, 100p,  100p
(2.0727e-11,  5.0197e-10,  3.3421e-08),		# 100p,  1000p, 100p
(4.64318e-10, 5.1717e-11,  3.443e-09),		# 1000p, 1000p, 100p
(4.95662e-10, 1.9902e-11,  1.325e-09),		# 100p,  100p,  1000p
(5.13125e-10, 2.176e-12,   1.44908e-10),	# 1000p, 100p,  1000p
(7.0654e-11,  4.51294e-10, 3.0047e-08),		# 100p,  1000p, 1000p
(2.8832e-10,  2.10264e-10, 1.4564e-08),		# 1000p, 1000p, 1000p
# f = 1030k
(4.15204e-10, 9.3348e-11,  6.265e-09),
(4.82774e-10, 2.4808e-11,  1.665e-09),
(6.9468e-11,  4.4271e-11,  2.9824e-08),
(4.36671e-10, 7.1598e-11,  4.806e-09),
(2.48621e-10, 2.6245e-10,  1.7616e-08),
(5.06174e-10, 1.06e-12,    7.1139e-11),
(1.08065e-10, 4.051e-10,   2.719e-08),
(4.11392e-10, 9.7254e-11,  6.528e-09),
# f = 1040k
(4.8285e-10,  1.4782e-11,  1.002e-09),
(4.77711e-10, 1.9996e-11,  1.356e-09),
(4.66182e-10, 2.149e-12,   2.149e-09),
(4.75601e-10, 2.2138e-11,  1.501e-09),
(4.94148e-10, 3.317e-12,   2.24871e-10),
# skipped small cb
(2.87433e-10, 2.43081e-10, 1.4446e-08),
(4.22337e-10, 7.6187e-11,  5.165e-09),

# a.n.other
(249.5E-12, 262E-12, 17.6E-9)]
 
def nmr_loop(target, l, ca, cb, cc, cdamp):
	'''
	Evaluate best capacitor combinations for the
	given ideal capacitances.
	
	target = target resonant frequency.
	l      = coil inductance
	ca     = capacitor a
	cb     = capacitor b
	cc     = capacitor c
	cdamp  = capacitance of damping circuit in parallel with ca.
	'''
	from find import find_cap_parallel
	ca = find_cap_parallel(ca-cdamp)
	cb = find_cap_parallel(cb)
	cc = find_cap_parallel(cc)
	def _calc(sa, sb, sc):
		calc = probe_tune(l, sa, sb, sc)
		l_match_required = match_inductor(target, sa, sb, sc)
		within = calc/target*100.0-100.0
		return (calc, l_match_required, within)
	results = [a+b+c+_calc(sum(a)+cdamp, sum(b), sum(c))
		for a in ca 
			for b in cb 
				for c in cb ]
	results.sort(key=lambda x: abs(x[-1]))
	#for x in results[:15]:
			#print '{0}+{1}, {2}+{3}, {4}+{5} = {6}, {7} ({8}%)'.format(*x)
	return results
	
def nmr_loop2(target, l, cdamp, cset, printno=15):
	'''
	Evaluate best capacitor combinations.
	
	target  = target resonant frequency.
	l       = coil inductance.
	cdamp   = capacitance of damping circuit in parallel with coil.
	          this will become part of ca and so need to be 
			  accounted for.
	cset    = list of tuples to evaluate of the form (ca, cb, cc).
	printno = number of combinations to print.
	'''
	from si_prefix import si
	results = []
	for c in cset:
		results = results + nmr_loop(target, l, c[0], c[1], c[2], cdamp)
	results.sort(key=lambda x: abs(x[-1]))
	for x in results[:printno]:
		print '{0}+{1}, {2}+{3}, {4}+{5} = {6}, {7} ({8}%)'.format(*[si(i) for i in x])
	return results
	
def nmr_probe_tune(l, ca, cb, cc):
	'''
	Calculate resonant frequency of probe.
	|| = parallel
	_ = series
	circuit = l || ca || (cb _ cc)
	'''
	from basic import cap_series
	c = sum((cap_series(cb, cc), ca))
	return filter_lc_f(l, c)
	
def nmr_l_match(f, ca, cb, cc):
	'''
	Calculate matching inductance required for a given 
	set of matching capacitors.
	'''
	from math import pi
	from basic import x_capacitor as xcap
	xa = xcap(ca)
	xb = xcap(cb)
	xc = xcap(cc)
	return 2*-1*((xa+2*xb)*xc)/(4*pi*f*(xa+2*xb+xc))
	
def print_comb(x):
	from si_prefix import si
	print 'ca=[{0}||{1}], cb=[{2}||{3}], cc=[{4}||{5}] = {6}, {7} ({8}%)'.format(*[si(i) for i in x])