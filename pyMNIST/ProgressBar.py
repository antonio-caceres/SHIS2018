import sys


GLOBAL_PROGRESS_BAR_START = 0
__last_progress_percent = 1
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

def draw_bar_text(percent, width = DEFAULT_WIDTH, duration_so_far = None, filled_and_unfilled = ('#', '-')):
    """
    :param percent: what percentage the progress bar should be filled. from 0 to 1 (inclusive)
    :type percent: float
    :param width: how wide to make all output, the progress bar, and estimated time left
    :type width: int
    :param duration_so_far: how much time has passed. if None, assume there's only one bar that matters right now, and use that one's timing.
    :type duration_so_far: int, None
    :return: None
    """

    global GLOBAL_PROGRESS_BAR_START, __last_progress_percent
    if duration_so_far == None:
        import time
        if percent == 0 and __last_progress_percent > percent:
            GLOBAL_PROGRESS_BAR_START = time.time()
        __last_progress_percent = percent
        duration_so_far = time.time() - GLOBAL_PROGRESS_BAR_START
    bar_width = width - 16
    filled_chars = int(percent * bar_width)
    # draw characters for actual progress bar
    def draw_bar_portion(texture, count, start_index):
        num_chars = len(texture)
        if num_chars == 1:
            sys.stdout.write(texture*count)
        else:
            start_index %= num_chars
            chars_written = 0
            while chars_written < count:
                space_left = count - chars_written
                if space_left > num_chars - start_index:
                    sys.stdout.write(texture[start_index:])
                    chars_written += num_chars - start_index
                    start_index = 0
                else:
                    sys.stdout.write(texture[start_index:start_index+space_left])
                    chars_written += space_left
    offset = int(duration_so_far*4)
    draw_bar_portion(filled_and_unfilled[0], filled_chars, offset)
    draw_bar_portion(filled_and_unfilled[1], bar_width - filled_chars, filled_chars + offset)
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


def draw_bar(percent, width = DEFAULT_WIDTH, duration_so_far = None, filled_and_unfilled = ('#', '-')):
    """
    as draw_bar_text, but also pulls the cursor back to the beginning of the line
    :param percent: what percentage the progress bar should be filled. from 0 to 1 (inclusive)
    :type percent: float
    :param width: how wide to make all output, the progress bar, and estimated time left
    :type width: int
    :param duration_so_far: how much time has passed. if None, assume there's only one bar that matters right now, and use that one's timing.
    :type duration_so_far: int, None
    :return: None
    """

    draw_bar_text(percent, width, duration_so_far, filled_and_unfilled)
    sys.stdout.write("\r")  # carriage return, restart output at the beginning of the line


def print_finished(process_name, width = None, seconds = None):
    """
    this function can be called once a progressbar is finished, to show how long it took
    :param process_name: the name of the progress bar that just finished
    :type process_name: str
    :param width: how many characters were used for the progressbar. if None, use the DEFAULT_WIDTH
    :type width: int, None
    :param seconds: how many seconds have passed. if None, calculate automatically
    :type width: int, None
    :return: None
    """

    if width == None:
        width = DEFAULT_WIDTH
    print(("%-"+str(width)+"s  ") % (process_name+" took "+timing(seconds)))


if __name__ == "__main__":
    import time, random
    # an example of how to make a progress bar
    filledPercent = 0
    t_start = time.time()
    while filledPercent < 1:
        draw_bar(filledPercent, 40, time.time() - t_start, ("@@@0","-~"))
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
        draw_bar(float(i)/limit, filled_and_unfilled = ("__processing","."))
        time.sleep(random.random()*0.2)  # some time consuming operation goes here...
    print_finished("process")
