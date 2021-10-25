from format import clearFormat


# Takes time and delay and returns new time with the delay added 
def addDelay(time, delay):
    hour = int(time[0:2])
    minute = int(time[3:5])
    second = int(time[6:8])
    milli = int(time[9:12])

    new_hour = hour
    new_minute = minute
    new_second = second
    new_milli = milli + delay
    
    if new_milli >= 1000:
        new_milli -= 1000
        new_second += 1

    if new_second >= 60:
        new_second -= 60
        new_minute += 1

    if new_minute >= 60:
        new_minute -= 60
        new_hour += 1

    new_time = f"{new_hour:02}" + ":" + f"{new_minute:02}" + ":" + f"{new_second:02}" + "," + f"{new_milli:03}"
    return new_time


# Creates new file equal to file with all times shifted by delay
def shift(file, delay, no_format):
    reader = open(file, "r")
    lines = reader.readlines()
    writer = open(file[:-13] + ".srt", "w")
    
    line_counter = 0
    while line_counter < len(lines):
        # Write sequence number
        writer.write(lines[line_counter])
        line_counter += 1
    
        # Now we need to add the delay
        times = lines[line_counter]
        start_time = times[0:12]
        end_time = times[17:29]
    
        new_start_time = addDelay(start_time, delay)
        new_end_time = addDelay(end_time, delay)
        
        new_times = new_start_time + " --> " + new_end_time + "\n"
        writer.write(new_times)
        line_counter += 1
    
        # Now we are in the dialogue part. We just want to copy these lines until we get to the next counter.
        # If we also want to clear formatting then we will do so here to save time.
        while line_counter < len(lines) and not lines[line_counter][:-1].isdigit():
            if no_format:
                new_line = clearFormat(lines[line_counter])
                writer.write(new_line)
            else:
                writer.write(lines[line_counter])

            line_counter += 1
    
    reader.close()
    writer.close()
