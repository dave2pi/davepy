'''
Collection of magnetic equations.
'''

from math import pi
u0 = 4.0*pi*1E-7

def air_coil_B_field(current, turns, length):
	return u0*turns*current/length

	