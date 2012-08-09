def const_r_n1_un(r, tgd):
	from si_prefix import si
	a0 = 2.0/tgd
	l = 2.0*r/a0
	c= 2.0/(a0*r)
	print 'component values:'
	print 'R =', si(r)
	print 'L =', si(l)
	print 'C =', si(c)

def const_r_n1_bal(r, tgd):
	from si_prefix import si
	a0 = 2.0/tgd
	l = r/a0
	c= 1.0/(a0*r)
	print 'component values:'
	print 'R =', si(r)
	print 'L =', si(l)
	print 'C =', si(c)

def const_r_n2_un(r, tgd, fr):
	from si_prefix import si
	from math import pi
	wr = 2.0*pi*fr
	q = float(tgd)*wr/4.0
	if q > 1.0:
		print 'Q is greater than 1.0'
		lp = r*q/wr
		cp = 1.0/(wr*q*r)
		ls = r/(wr*q)
		cs = q/(wr*r)
		print 'Q =', si(q)
		print 'component values:'
		print 'Lp =', si(lp)
		print 'Cp =', si(cp)
		print 'Ls =', si(ls)
		print 'Cs =', si(cs)
	else:
		print 'Q is less than 1.0'
		k = (1-q**2)/(1+q**2)
		ls_k = ((q**2+1)*r)/(2*q*wr)
		ls =2*(1+k)*ls_k 
		cs = q/(2*wr*r)
		lp = (1-k)*ls_k/2
		cp = 2/(q*wr*r)
		print 'Q =', si(q)
		print 'component values:'
		print 'Controlled coupling, k:'
		print '  Cp =', si(cp)
		print '  Cs =', si(cs)
		print '  Ls =', si(ls_k)
		print '  k =', si(k)
		print 'Unity coupling (center-tapped) Ls:'
		print '  Cp =', si(cp)
		print '  Lp =', si(lp)
		print '  Cs =', si(cs)
		print '  Ls =', si(ls)
		
def min_l_n2(rs, rl, tgd, fr):
	from math import pi, sqrt
	from si_prefix import si
	import ltspice
	
	wr = 2.0*pi*fr
	q = tgd*wr/4.0
	r = sqrt(rs*rl)
	c = q/(4.0*wr*r)
	l = 1.0/(wr**2.0*c)
	
	n = 5
	print 'q:'.rjust(n), si(q)
	print 'component values:'
	print 'r:'.rjust(n), si(r)
	print 'c:'.rjust(n), si(c)
	print 'l:'.rjust(n), si(l)
	
	# Simulation
	sim_name = 'spice'
	cir_min_l_n2 = '''
* {0}.cir
R1 N001 N002 {1}
R2 0 out {2}
V1 N002 0 AC 1
L1 N001 N003 {3}
L2 N003 out {3}
R3 N003 0 {4}
C1 out N001 {5}
K1 L1 L2 1.0
.ac dec 10000 {6} {7}
.backanno
.end
'''.format(
		sim_name,
		si(rs, space=0),
		si(rl, space=0),
		si(l/4.0, space=0),
		si(r, space=0),
		si(c, space=0),
		si(fr/10.0, space=0),
		si(fr*10.0, space=0)
	)
	ltspice.run_sim_ac(cir_min_l_n2, 'V(out)', sim_name)
	
	return (c, l, r)
	
def min_l_n4(rs, rl, tgd1, fr1, tgd2, fr2):
	from math import pi, sqrt
	from si_prefix import si
	r = sqrt(rs*rl)
	wr1 = 2.0*pi*fr1
	wr2 = 2.0*pi*fr2
	q1 = tgd1*wr1/4.0
	q2 = tgd2*wr2/4.0
	a = wr1**2*wr2**2
	b = a*(1/(wr2*q2)+1/(wr1*q1))
	c = q1*q2/(a*(q2*wr1+q1*wr2))
	d = (q1*q2*(wr1**2+wr2**2)+wr1*wr2)/(a*b*q1*q2)-c-1/(a*b**2*c)
	e = 1/(a*b*c*d)
	l1 = 4*e*r/a
	c1 = (a*d)/(4*r)
	l2 = 4*b*r/a
	c2 = a*c/(4*r)
	
	n = 5
	print 'q1:'.rjust(n), si(q1)
	print 'q2:'.rjust(n), si(q2)
	print 'wr1:'.rjust(n), si(wr1)
	print 'wr2:'.rjust(n), si(wr2)
	print 'component values:'
	print 'r:'.rjust(n), si(r)
	print 'l1:'.rjust(n), si(l1)
	print 'c1:'.rjust(n), si(c1)
	print 'l2:'.rjust(n), si(l2)
	print 'c2:'.rjust(n), si(c2)
