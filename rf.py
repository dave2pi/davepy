'''
Colection of RF electronics calcs.
'''

from math import pi as _pi
from fr import *

def match_x(r_small, r_large):
	'''
	Impedance match two resistances.
	'''
	from math import sqrt
	rl = r_large
	rs = r_small
	xp = -sqrt(rs*rl**2/(rl-rs))
	xs = -(rl**2*xp/(rl**2+xp**2))
	return (xp, xs)

def match(r_small, r_large, f):
	'''
	Impedance match two resistances.
	'''
	from basic import x_cap_i, x_ind_i
	xc, xl = match_x(r_small,r_large)
	c = x_cap_i(xc, f)
	l = x_ind_i(xl, f)
	return (c, l)

def high_pass_t(z0, f=1E6, a=_pi/2):
	from math import pi, sin, cos
	w = 2*pi*f
	l = z0/(w*sin(a))
	c = sin(a)/(w*z0*(1-cos(a)))
	return (l, c)