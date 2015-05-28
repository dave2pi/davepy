from math import pi

u0 = 4.0*pi*10**-7

def P_cu(t_celsius):
	return 67.078E-12*(t_celsius+273)-2.560E-9
	
def SkinDepth(f, t=20):
	from math import sqrt
	w = 2*pi*f
	return sqrt(2*P_cu(t)/(w*u0))
	
def Fr(f, a, m, t=20, n=1):
	import cmath
	from math import sqrt
	def N(nt, a, b):
		'''
		Nt = number of turns
		a = bredth of conductor
		b = bredth of winding
		'''
		return Nt*a/b
	def Alpha(w, n, p):
		'''
		\sqrt{\frac{j\omega\mu_{0}\eta}{\rho}}
		j = sqrt(-1)
		w = angular frequency
		u0 = permiability of free space
		n = winding factor, n()
		p = resistivity
		'''
		return cmath.sqrt(1j*w*u0*n/p)
	def Coth(x):
		return cmath.cosh(x)/cmath.sinh(x)
	def M(alpha, h):
		'''
		alpha = alpha()
		h = height of conductor
		'''
		return alpha*h*Coth(alpha*h)
	def D(alpha, h):
		'''
		alpha = alpha()
		h = height of conductor
		'''
		return 2.0*alpha*h*cmath.tanh(alpha*h/2.0)
	def _Fr(M_real, D_real, m):
		'''
		M_real = real part of M()
		D_real = real part of D()
		m = number of whole layers in a winding portion
		'''
		return M_real+(m**2-1.0)*D_real/3.0
	w = 2*pi*f
	h = sqrt(pi)*a/2.0
	p = P_cu(t)
	alpha = Alpha(w, n, p)
	M_complex = M(alpha, h)
	D_complex = D(alpha, h)
	M_real = M_complex.real
	D_real = D_complex.real
	fr = _Fr(M_real, D_real, m)
	return fr
	
if __name__ == '__main__':
	from engpy import si
	print 'Fr =', si(Fr(20E3, 0.265E-3, 5.29, t=20, n=1))
	print 'sd =', si(SkinDepth(20E3, t=20))
	