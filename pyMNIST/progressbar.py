import sys

def timing(seconds, width_limit = None):
	"""print [days,] [hours,] [minutes,] seconds [in the specifined number of characters]"""
	minutes, hours, days = 0, 0, 0
	def split_timing(seconds, seconds_per_unit):
		unit = 0
		if seconds > seconds_per_unit:
			unit = int(seconds / seconds_per_unit)
			seconds -= (unit * seconds_per_unit)
		return seconds, unit
	seconds, days = split_timing(seconds, 60*60*24)
	seconds, hours = split_timing(seconds, 60*60)
	seconds, minutes = split_timing(seconds, 60)
	# print(days, hours, minutes, seconds)
	output = ""
	if days != 0 and (width_limit == None or len(output)+3 <= width_limit):
		output += "%2dd" % days
	if hours != 0 and (width_limit == None or len(output)+3 <= width_limit):
		if len(output) > 0: output += " "
		if width_limit == None or len(output)+3 < width_limit: output += "%2dh" % hours
	if minutes != 0 and (width_limit == None or len(output)+3 <= width_limit):
		if len(output) > 0: output += " "
		if width_limit == None or len(output)+3 < width_limit: output += "%2dm" % minutes
	if seconds != 0 and (width_limit == None or len(output)+3 <= width_limit):
		if len(output) > 0: output += " "
		if width_limit == None or len(output)+3 < width_limit: output += "%2ds" % seconds
	if width_limit != None:
		format = "%%-%ds" % width_limit
		output = format % output
	return output

def draw_bar_text(percent, width = 80, duration_so_far = None):
	"""
	:param percent: what percentage the progress bar should be filled
	:param width: how wide to make all output, the progress bar, and estimated time left
	:param duration_so_far: how much time has passed. if None, will not have an estimated time left
	:return: None
	"""
	bar_width = width-8
	if duration_so_far != None:
		bar_width -= 8
	limit = percent * bar_width
	# characters for actual progress bar
	for i in range(bar_width):
		if i < limit:
			sys.stdout.write("#")
		else:
			sys.stdout.write("-")
	# 8 characters for percentage
	sys.stdout.write(" %5.1f%% " % (percent*100)) # total width 5, 1 decimal value
	if duration_so_far != None:
		# 12 characters for estimated time
		if duration_so_far != 0 and percent != 0:
			totalTimeExpected = (duration_so_far / percent)
			seconds = totalTimeExpected - duration_so_far + 0.5
			t = timing(seconds)
			sys.stdout.write("%-8s " % t)
		else:
			sys.stdout.write("         ")
	sys.stdout.flush()

def draw_bar(percent, width, duration_so_far = None):
	draw_bar_text(percent, width, duration_so_far)
	sys.stdout.write("\r") # carriage return, restart output at the beginning of the line

if __name__ == "__main__":
	import time, random
	filledPercent = 0
	t_start = time.time()
	while filledPercent < 1:
		draw_bar(filledPercent, 40, time.time() - t_start)
		time.sleep(random.random()*0.25) # some time consuming operation goes here...
		filledPercent += 0.0125 # estimate addition to progress
	#sys.stdout.write("\n")
	print( "%-40s" % ("%.2f seconds" % (time.time()-t_start)) )