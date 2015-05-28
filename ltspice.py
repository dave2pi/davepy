'''
LTSpice interface.
Require ltsputil to be installed at the location defined below.
'''
	
def format(v):
	from si_prefix import si
	return si(v, space=0).replace('M', 'meg')
	
def run_sim_ac(cir, signal, sim_name='spice', view_raw=False, plot=0, quiet=True):
	'''
	Run a simulation. Plot data as an AC simulation.
	'''
	import csv
	from math import pi, log10, floor
	from cmath import polar
	from matplotlib.pyplot import subplot, semilogx, ylabel, xlabel, title, subplots_adjust, show
	import numpy as np
	
	with open(sim_name+'.cir', 'w') as f:
		f.write(cir)

	# Run simulation using LTSpice
	lt_error = ltspice_sim(sim_name+'.cir', quiet=quiet)
		
	# Read LTSpice simulation log
	try:
		print_sim_log(sim_name+'.log')
	except:
		print 'Error:', sys.exc_info()[0]
	
	if lt_error != 0:
		return
	
	# View .RAW file
	if view_raw != False:
		ltspice_raw(sim_name+'.raw', quiet=quiet)
	
	# Use external utility to export .RAW file to a .CSV
	errorlevel = export_ac(sim_name+'.raw', sim_name+'.csv', quiet, 'frequency', signal)
		
	# Read in .CSV data
	f = []
#	signal = []
	mag = []
	phase = []
	phase_wrapped = []
	with open(sim_name+'.csv', 'r') as file:
		csv_reader = csv.reader(file, dialect='excel')
		for row in csv_reader:
			f.append(float(row[0]))
			#signal.append(complex(float(row[1]), float(row[2])))
			mag.append(float(row[1]))
			phase.append(float(row[2]))
			phase_wrapped.append(float(row[3]))
	
	# Calculate phase delay
	#phase_delay = [abs(phase[i])/(f[i]*360) for i in range(len(f))]
	
	# Calculate group delay
	#group_delay = np.gradient(np.array([sp[1] for sp in signal_polar]), np.array([2.0*pi*hz for hz in f]))
	
	# Delete simulation files
	delete_sim_files(sim_name, cir=1, raw=1, log=1, csv=1, tmp=1, quiet=quiet)
	
	return f, mag, phase

def export_ac(fin, fout, quiet, *sig):
	'''
	Use external utility to export .RAW file to a .CSV
	'''
	if quiet==False:
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
	# -d = dB
	# -q = phase +/-pi
	return ltsputil('-xot0dqp', fin, fout, '"%14.6e"  "," "" '+signals, quiet=quiet)

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

def ltspice_sim(filename, quiet=False):
	if quiet==False:
		print 'Starting simulation...'
	return ltspice('-b '+filename, quiet=quiet)

def ltspice_raw(filename, quiet=False):
	if quiet==False:
		print 'Viewing .RAW file...'
	return ltspice(filename, quiet=quiet)

def ltspice(args, quiet=False):
	'''
	Run simulation using LTSpice
	'''
	import os
	if quiet==False:
		print 'Launching LTSpice...'
	if os.name == 'posix':
		errorlevel = os.system(_escape_shell_chars('wine /home/dave/.wine/drive_c/Program\ Files/LTC/LTspiceIV/scad3.exe '+args))
	elif os.name == 'nt':
		errorlevel = os.system('C:\\Programs32\\LTC\\LTspiceIV\\scad3.exe '+args)
	else:
		print 'ERROR: Host environment "{0}" is not recognised.'.format(os.name)
		errorlevel = 1
	if errorlevel != 0:
		print 'ERROR: run_sim() returned {0}.'.format(errorlevel)
	return errorlevel

def ltsputil(cmd, fin, fout, args, quiet=False):
	'''
	Use external utility ltsputil to export .RAW file to a .CSV
	'''
	import os
	if quiet==False:
		print 'Running ltsputil...'
		quiet = ' > nul'
	else:
		quiet = ''
	if os.name == 'posix':
		errorlevel = os.system(_escape_shell_chars('wine /home/dave/.wine/drive_c/Program\ Files/LTC/LTspiceIV/ltsputil.exe {0} {1} {2} {3}'.format(cmd, fin, fout, args)))
	elif os.name == 'nt':
		errorlevel = os.system('C:\\Programs32\\LTC\\LTspiceIV\\ltsputil.exe {0} {1} {2} {3} > nul'.format(cmd, fin, fout, args))
	else:
		print 'ERROR: Host environment "{0}" is not recognised.'.format(os.name)
		errorlevel = 1
	if errorlevel != 0:
		print 'ERROR: ltsputil() returned {0}.'.format(errorlevel)
	return errorlevel

def delete_sim_files(name, cir=0, raw=0, log=0, csv=0, tmp=0, quiet=False):
	import os
	if quiet==False:
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
		errorlevel = os.system(_escape_shell_chars('rm {0}'.format(args)))
	elif os.name == 'nt':
		errorlevel = os.system('del {0}'.format(args))
	else:
		print 'ERROR: Host environment "{0}" is not recognised.'.format(os.name)
		errorlevel = 1
	if errorlevel != 0:
		print 'ERROR: delete_sim_files() returned {0}.'.format(errorlevel)
	return errorlevel
	
def _escape_shell_chars(sh):
	sh = sh.replace('(', '\(')
	sh = sh.replace(')', '\)')
	return sh
