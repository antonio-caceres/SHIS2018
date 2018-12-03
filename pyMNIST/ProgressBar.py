import time
import random

GLOBAL_PROGRESS_BAR_START = 0
DEFAULT_WIDTH = 40
__last_progress_percent = 1
__has_colorama = False
if not __has_colorama:  # colorama abstracts colors in the terminal
    import pkgutil
    __has_colorama = pkgutil.find_loader('colorama')
    if __has_colorama:
        import colorama


def time_to_string(seconds=None, max_num_units=None):
    """
    Produce a printable string to represent a time in days, hours, minutes, and seconds,
    with the specified number of "significant units".
    :param seconds: time in seconds.
        if None, assume there's only one bar that matters right now, and use the time that bar has been running.
    :type seconds: int, float, None
    :param max_num_units: the number of units with which to represent the time. Understood as "significant units".
        For example, if a time is in hours, minutes, and seconds, limiting max_num_units to two produces a string that
        only includes the hours and minutes. if not None, limits size of the returned string (default None).
    :type max_num_units: int, None
    :return: seconds converted into more human-readable form, eg: time_to_string(3805) -> " 1h 3m 25s"
    :rtype: str
    """
    if seconds is None:
        seconds = time.time() - GLOBAL_PROGRESS_BAR_START
    if max_num_units is None:
        max_num_units = 2

    def split_timing(num_seconds, seconds_per_unit):
        unit = 0
        if num_seconds > seconds_per_unit:
            unit = int(num_seconds / seconds_per_unit)
            num_seconds -= (unit * seconds_per_unit)
        return num_seconds, unit

    seconds, days = split_timing(seconds, 60*60*24)
    seconds, hours = split_timing(seconds, 60*60)
    seconds, minutes = split_timing(seconds, 60)
    unit_names = ['d', 'h', 'm', 's']
    unit_values = [days, hours, minutes, seconds]

    output = ""
    used = 0
    for j in range(len(unit_names)):
        if unit_values[j] != 0:
            output += "{:02d}{} ".format(int(unit_values[j]), unit_names[j])
            used += 1
        if used >= max_num_units:
            break
    return output


def draw_bar(percent, width=DEFAULT_WIDTH, duration_so_far=None, filled_and_unfilled=('#', '-')):
    """
    :param percent: what percentage the progress bar should be filled. from 0 to 1 (inclusive)
    :type percent: float
    :param width: how wide to make all output, the progress bar, and estimated time left
    :type width: int
    :param duration_so_far: how much time has passed.
        if None, assume there's only one bar that matters right now, and use that one's timing.
    :type duration_so_far: int, None
    :param filled_and_unfilled: two strings, the first and second representing the filled and unfilled progress bar
        characters, respectively.
    :type filled_and_unfilled: (str, str)
    :return: None
    """
    global GLOBAL_PROGRESS_BAR_START, __last_progress_percent  # initializes to the outer scope variables

    if duration_so_far is None:
        # check if a new progress bar is beginning
        if __last_progress_percent > percent:
            GLOBAL_PROGRESS_BAR_START = time.time()  # resets the starting time for the progress bar because new bar.
        __last_progress_percent = percent
        duration_so_far = time.time() - GLOBAL_PROGRESS_BAR_START

    bar_width = width - 16
    filled_chars = int(percent * bar_width)+1
    if filled_chars > bar_width:
        filled_chars = bar_width

    # draw characters for actual progress bar
    def draw_bar_portion(texture, count, start_index):
        num_chars = len(texture)
        if num_chars == 1:
            print(texture*count, end='')
        else:
            start_index %= num_chars
            chars_written = 0
            while chars_written < count:
                space_left = count - chars_written
                if space_left > num_chars - start_index:
                    print(texture[start_index:], end='')
                    chars_written += num_chars - start_index
                    start_index = 0
                else:
                    print(texture[start_index:start_index+space_left], end='')
                    chars_written += space_left
    offset = int(duration_so_far*4)
    draw_bar_portion(filled_and_unfilled[0], filled_chars, offset)
    if __has_colorama:
        print(colorama.Style.DIM, end='')
    draw_bar_portion(filled_and_unfilled[1], bar_width - filled_chars, filled_chars + offset)
    if __has_colorama:
        print(colorama.Style.RESET_ALL, end='')

    # 8 characters for percentage
    print(" %5.1f%% " % (percent*100), end='')  # total width 5, 1 decimal value
    if duration_so_far is not None:
        # 18 characters for estimated time
        if duration_so_far != 0 and percent != 0:
            total_time_expected = (duration_so_far / percent)
            seconds = total_time_expected - duration_so_far + 0.5
            t = time_to_string(seconds, 2)
            print("%-7s " % t, end='')
        else:
            print("         ", end='')
    print('', end='\r', flush=True)


def print_finished(process_name, width=None, seconds=None):
    """
    this function can be called once a progressbar is finished, to show how long it took
    :param process_name: the name of the progress bar that just finished
    :type process_name: str
    :param width: how many characters were used for the progressbar. if None, use the DEFAULT_WIDTH
    :type width: int, None
    :param seconds: how many seconds have passed. if None, calculate automatically
    :type width: int, float, None
    :return: the number of seconds that the process took
    :rtype: int, float
    """

    if width is None:
        width = DEFAULT_WIDTH
    print(("%-"+str(width)+"s  ") % (process_name +" took " + time_to_string(seconds)))
    if seconds is None:
        import time
        seconds = time.time() - GLOBAL_PROGRESS_BAR_START
    return seconds


if __name__ == "__main__":
    if not __has_colorama:
        print("consider installing colorama with: python -m pip install colorama --user")
    # an example of how to make a progress bar
    filledPercent = 0
    t_start = time.time()
    while filledPercent < 1:
        draw_bar(filledPercent, 40, time.time() - t_start, ("/-\\|", "-~"))
        time.sleep(random.random()*0.25)  # some time consuming operation goes here...
        filledPercent += 0.0125  # estimate addition to progress
    # print('')
    print("%-40s" % ("process took " + time_to_string(time.time() - t_start)))

    # another example
    filledPercent = 0
    while filledPercent < 1:
        draw_bar(filledPercent, 40)  # notice time.time() is not required...
        # but only if there is only one progress bar being used right now
        time.sleep(random.random()*0.25)  # some time consuming operation goes here...
        filledPercent += 0.0125  # estimate addition to progress
    print("%-40s" % ("process took " + time_to_string()))

    # another example
    limit = 120
    for i in range(limit):
        draw_bar(float(i) / limit, filled_and_unfilled=("##PROCESSING", "  processing"))
        time.sleep(random.random()*0.2)  # some time consuming operation goes here...
    print_finished("process")
