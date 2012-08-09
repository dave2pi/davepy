'''
LTSpice interface.
'''
	
def run_sim_ac(cir, signal, sim_name='spice'):
	'''
	Run a simulation. Plot data as an AC simulation.
	'''
	import csv
	from math import pi, log10
	from cmath import polar
	from matplotlib.pyplot import subplot, semilogx, ylabel, xlabel, title, subplots_adjust, show
	
	with open(sim_name+'.cir', 'w') as f:
		f.write(cir)

	# Run simulation using LTSpice
	if run_sim(sim_name+'.cir') != 0:
		return
		
	# Read LTSpice simulation log
	print_sim_log(sim_name+'.log')
	
	# Use external utility to export .RAW file to a .CSV
	if export_ac(sim_name+'.raw', sim_name+'.csv', 'frequency', signal) != 0:
		return
		
	# Read in .CSV data
	f = []
	signal = []
	with open(sim_name+'.csv', 'r') as file:
		csv_reader = csv.reader(file, dialect='excel')
		for row in csv_reader:
			f.append(float(row[0]))
			signal.append(complex(float(row[1]), float(row[2])))

	# convert to polar
	signal_polar = [polar(v) for v in signal]
	mag = [20*log10(p[0]/1.0) for p in signal_polar]
	phase = [360*p[1]/(2*pi) for p in signal_polar]
	# Phase wrap around correction
	phase_graph = phase[:]
	for i in range(1, len(phase)):
		if phase_graph[i-1]-phase_graph[i] < -350:
			phase_graph[i] = phase_graph[i] - 360
		elif phase_graph[i-1]-phase_graph[i] > 350:
			phase_graph[i] = phase_graph[i] + 360
	delay = [abs(phase[i])/(f[i]*360) for i in range(len(f))]
	
	# Delete simulation files
	delete_sim_files(sim_name, cir=1, raw=1, log=1, csv=1, tmp=1)
	
	# Plot response
	subplot(311)
	semilogx(f,mag)
	ylabel('Magnitude (db)')
	xlabel(r'Frequency')
	title(r'Frequency response')
	subplot(312)
	semilogx(f,phase_graph)
	ylabel('Phase (degrees)')
	xlabel(r'Frequency')
	title(r'Phase response')
	subplot(313)
	semilogx(f,delay)
	ylabel('Delay (seconds)')
	xlabel(r'Frequency')
	title(r'Group delay response')
	subplots_adjust(hspace=1.0)
	show()

def export_ac(fin, fout, *sig):
	'''
	Use external utility to export .RAW file to a .CSV
	'''
	print 'Exporting to CSV...'
	# Expand signal args
	signals = ''
	for s in sig:
		signals = signals + s + ' '
	# Run export
	# -x = e[x]port
	# -o = [o]verwrite
	# -t = [t]ranspose to columns
	# -0 = No header data
	return ltsputil('-xot0', fin, fout, '"%14.6e"  "," "" '+signals)

def print_sim_log(filename):
	'''
	Read LTSpice simulation log
	'''
	with open(filename, 'r') as f:
		line = f.readlines()
		for l in line:
			if l.upper().find('WARNING') != -1:
				print l.strip()
			if l.upper().find('ERROR') != -1:
				print l.strip()

def ltspice(filename):
	'''
	Run simulation using LTSpice
	'''
	import os
	print 'Running LTSpice simulation...'
	if os.name == 'posix':
		errorlevel = os.system('wine /home/dave/.wine/drive_c/Program\ Files/LTC/LTSpiceIV/scad3.exe -b '+filename)
	elif os.name == 'nt':
		errorlevel = os.system('C:\\Programs\\LinearTec\\LTspiceIV\\scad3.exe -b '+filename)
	else:
		print 'ERROR: Host environment "{0}" is not recognised.'.format(os.name)
		errorlevel = 1
	if errorlevel != 0:
		print 'ERROR: run_sim() returned {0}.'.format(errorlevel)
	return errorlevel

def ltsputil(cmd, fin, fout, args):
	'''
	Use external utility ltsputil to export .RAW file to a .CSV
	'''
	import os
	print 'Running ltsputil...'
	if os.name == 'posix':
		errorlevel = os.system('wine /home/dave/.wine/drive_c/Program\ Files/LTC/LTSpiceIV/ltsputil.exe {0} {1} {2} {3}'.format(cmd, finfilename, foutfilename, args))
	elif os.name == 'nt':
		errorlevel = os.system('C:\\Programs\\LinearTec\\LTspiceIV\\ltsputil.exe {0} {1} {2} {3}'.format(cmd, fin, fout, args))
	else:
		print 'ERROR: Host environment "{0}" is not recognised.'.format(os.name)
		errorlevel = 1
	if errorlevel != 0:
		print 'ERROR: ltsputil() returned {0}.'.format(errorlevel)
	return errorlevel

def delete_sim_files(name, cir=0, raw=0, log=0, csv=0, tmp=0):
	import os
	print 'Deleting simulation files...'
	args = ''
	if cir != 0:
		args += name+'.cir '
	if raw != 0:
		args += name+'.raw '
	if log != 0:
		args += name+'.log '
	if csv != 0:
		args += name+'.csv '
	if tmp != 0:
		args += '*.tmp '
	if os.name == 'posix':
		errorlevel = os.system('rm {0}'.format(args))
	elif os.name == 'nt':
		errorlevel = os.system('del {0}'.format(args))
	else:
		print 'ERROR: Host environment "{0}" is not recognised.'.format(os.name)
		errorlevel = 1
	if errorlevel != 0:
		print 'ERROR: delete_sim_files() returned {0}.'.format(errorlevel)
	return errorlevel
