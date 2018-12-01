import sys


GLOBAL_PROGRESS_BAR_START = 0
__LAST_PROGRESS_PERCENT = 100
DEFAULT_WIDTH = 60


def timing(seconds = None, width_limit = None):
    """
    print [days,] [hours,] [minutes,] seconds [in the specified number of characters].
    Terms above in square-brackets may not be included if zero
    :param seconds: time in seconds. if None, assume there's only one bar that matters right now, and use that one's timing.
    :type seconds: int, float, None
    :param width_limit: if not None, limits size of the returned string (default None)
    :type width_limit: int, None
    :return: seconds converted into more human-readable form, eg: timing(3805) -> " 1h  3m 25s"
    :rtype: str
    """

    if seconds == None:
        import time
        seconds = time.time() - GLOBAL_PROGRESS_BAR_START
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
    output = ""
    noWordLimit = width_limit is None
    if days != 0 and (noWordLimit or len(output)+3 <= width_limit):
        output += "%2dd" % days
    if hours != 0 and (noWordLimit or len(output)+3 <= width_limit):
        if len(output) > 0:
            output += " "
        if noWordLimit or len(output)+3 < width_limit:
            output += "%2dh" % hours
    if minutes != 0 and (noWordLimit or len(output)+3 <= width_limit):
        if len(output) > 0:
            output += " "
        if noWordLimit or len(output)+3 < width_limit:
            output += "%2dm" % minutes
    if seconds != 0 and (noWordLimit or len(output)+3 <= width_limit):
        if len(output) > 0:
            output += " "
        if noWordLimit or len(output)+3 < width_limit:
            output += "%2ds" % seconds
    if not noWordLimit:
        format = "%%-%ds" % width_limit
        output = format % output
    return output

def draw_bar_text(percent, width = DEFAULT_WIDTH, duration_so_far = None):
    """
    :param percent: what percentage the progress bar should be filled
    :param width: how wide to make all output, the progress bar, and estimated time left
    :param duration_so_far: how much time has passed. if None, assume there's only one bar that matters right now, and use that one's timing.
    :return: None
    """

    global GLOBAL_PROGRESS_BAR_START, __LAST_PROGRESS_PERCENT
    if duration_so_far == None:
        import time
        if percent == 0 and __LAST_PROGRESS_PERCENT > percent:
            GLOBAL_PROGRESS_BAR_START = time.time()
        __LAST_PROGRESS_PERCENT = percent
        duration_so_far = time.time() - GLOBAL_PROGRESS_BAR_START
    bar_width = width - 16
    limit = percent * bar_width
    # characters for actual progress bar
    for i in range(bar_width):
        if i < limit:
            sys.stdout.write("#")
        else:
            sys.stdout.write("-")
    # 8 characters for percentage
    sys.stdout.write(" %5.1f%% " % (percent*100))  # total width 5, 1 decimal value
    if duration_so_far is not None:
        # 18 characters for estimated time
        if duration_so_far != 0 and percent != 0:
            total_time_expected = (duration_so_far / percent)
            seconds = total_time_expected - duration_so_far + 0.5
            t = timing(seconds, 8)
            sys.stdout.write("%-8s " % t)
        else:
            sys.stdout.write("         ")
    sys.stdout.flush()


def draw_bar(percent, width = DEFAULT_WIDTH, duration_so_far = None):
    """
    as draw_bar_text, but also pulls the cursor back to the beginning of the line
    :param percent: what percentage the progress bar should be filled
    :param width: how wide to make all output, the progress bar, and estimated time left
    :param duration_so_far: how much time has passed. if None, will not have an estimated time left
    :return: None
    """
    draw_bar_text(percent, width, duration_so_far)
    sys.stdout.write("\r")  # carriage return, restart output at the beginning of the line


def print_finished(processName, width = None, seconds = None):
    if width == None:
        width = DEFAULT_WIDTH
    print(("%-"+str(width)+"s  ") % (processName+" took "+timing(seconds)))


if __name__ == "__main__":
    import time, random
    # an example of how to make a progress bar
    filledPercent = 0
    t_start = time.time()
    while filledPercent < 1:
        draw_bar(filledPercent, 40, time.time() - t_start)
        time.sleep(random.random()*0.25)  # some time consuming operation goes here...
        filledPercent += 0.0125  # estimate addition to progress
    # sys.stdout.write("\n")
    print("%-40s" % ("process took "+timing(time.time()-t_start)))

    # another example
    filledPercent = 0
    while filledPercent < 1:
        draw_bar(filledPercent, 40) # notice time.time() is not required... but only if there is only one progress bar being used right now
        time.sleep(random.random()*0.25)  # some time consuming operation goes here...
        filledPercent += 0.0125  # estimate addition to progress
    print("%-40s" % ("process took "+timing()))

    # another example
    limit = 120
    for i in range(limit):
        draw_bar(float(i)/limit)
        time.sleep(random.random()*0.2)  # some time consuming operation goes here...
    draw_bar(1)
    print_finished("process")
