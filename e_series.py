'''
Collection of prefered value series over a single decade including a function
to expand the series over multiple decades.
'''
import math

def expand(series, min=1.0, max=10.0E6):
	'''
	Expand a single decade series over multiple decades.

	series = single decade series to expand.
	min = minimum value of expanded series.
	max = maximum value of expanded series.

	eg. expand(E12, 10.0, 100E3)
	'''
	# Calc range of multipliers required.
	# -3/-1: Adjusted because series arrays normalized to 1E2.
	exp_min = int(math.log10(min)-3)
	exp_max = int(math.log10(max))
	# Expand series.
	return [x*10**m for m in range(exp_min, exp_max) 
		for x in series 
			if x*10**m >= min
				if x*10**m <= max]

# Define single decade series E6 to E192
E6 = [100, 150, 220, 330, 470, 680]

E12 = [100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820]

E24 = [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 
390, 430, 470, 510, 560, 620, 680, 750, 910]

E48 = [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 
196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332, 348, 365, 383, 
402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 
825, 866, 909, 953]

E96 = [100, 121, 147, 178, 215, 261, 316, 383, 464, 562, 681, 825, 102, 124, 
150, 182, 221, 267, 324, 392, 475, 576, 698, 845, 105, 127, 154, 187, 226, 
274, 332, 402, 487, 590, 715, 866, 107, 130, 158, 191, 232, 280, 340, 412, 
499, 604, 732, 887, 110, 133, 162, 196, 237, 287, 348, 422, 511, 619, 750, 
909, 113, 137, 165, 200, 243, 294, 357, 432, 523, 634, 768, 931, 115, 140, 
169, 205, 249, 301, 365, 442, 536, 649, 787, 953, 118, 143, 174, 210, 255, 
309, 374, 453, 549, 665, 806, 976]

E192 = [100, 121, 147, 178, 215, 261, 316, 383, 464, 562, 681, 825, 101, 
123, 149, 180, 218, 264, 320, 388, 470, 569, 690, 835, 102, 124, 150, 182, 
221, 267, 324, 392, 475, 576, 698, 845, 104, 126, 152, 184, 223, 271, 328, 
397, 481, 583, 706, 856, 105, 127, 154, 187, 226, 274, 332, 402, 487, 590, 
715, 866, 106, 129, 156, 189, 229, 277, 336, 407, 493, 597, 723, 876, 107, 
130, 158, 191, 232, 280, 340, 412, 499, 604, 732, 887, 109, 132, 160, 193, 
234, 284, 344, 417, 505, 612, 741, 898, 110, 133, 162, 196, 237, 287, 348, 
422, 511, 619, 750, 909, 111, 135, 164, 198, 240, 291, 352, 427, 517, 626, 
759, 920, 113, 137, 165, 200, 243, 294, 357, 432, 523, 634, 768, 931, 114, 
138, 167, 203, 246, 298, 361, 437, 530, 642, 777, 942, 115, 140, 169, 205, 
249, 301, 365, 442, 536, 649, 787, 953, 117, 142, 172, 208, 252, 305, 370, 
448, 542, 657, 796, 965, 118, 143, 174, 210, 255, 309, 374, 453, 549, 665, 
806, 976, 120, 145, 176, 213, 258, 312, 379, 459, 556, 673, 816, 988]

# Define commonly used resistor series
RN73 = expand(E96, 4.7, 1E6)
WCR = expand(E24, 10.0, 10E6)
MRS25 = expand(E96, 1.0, 10E6)