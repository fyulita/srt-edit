#!/usr/bin/env python

"""
  srt-edit - (c) Federico Yulita 2021
  Licensed under GPLv3.0
"""

import argparse
import os


def main():
    # Parse arguments and flags
    parser = argparse.ArgumentParser(prog="srt-edit", description="A simple tool to edit .srt subtitles from the command line")
    
    parser.add_argument("-c", "--clear-format", action="store_true", help="clear formatting")
    parser.add_argument("file", type=str, help="input .srt file")
    parser.add_argument("-s", "--shift", type=int, help="shift subtitles by SHIFT (in ms)")
    
    args = parser.parse_args()
    
    clear_format = args.clear_format
    file = args.file
    delay = args.shift
    
    # Error handling
    if file[-4:] != ".srt":
        print(f"srt-edit: error: argument -f/--file: invalid .srt file: '{file}'")
    else:
        # Save input file as [filename].original.srt
        # Will create new file as [filename].srt with changes added
        original_file = file[:-4] + ".original.srt"
        os.rename(file, original_file)

        if not delay is None or clear_format:
            edit(original_file, delay, clear_format)
        else:
            print(f"srt-edit: error: no instruction given")


# Main loop to read original file and write a new one with all the changes
def edit(file, delay, clear_format):
    # Use original file for reading
    reader = open(file, "r")
    lines = reader.readlines()
    # Create new file to write with changes
    writer = open(file[:-13] + ".srt", "w")
    
    line_counter = 0
    while line_counter < len(lines):
        # Write sequence number
        writer.write(lines[line_counter])
        line_counter += 1
    
        # Now we are in the timings part
        # Add the delay if necessary
        if not delay is None:
            times = lines[line_counter]
            start_time = times[0:12]
            end_time = times[17:29]
    
            new_start_time = addDelay(start_time, delay)
            new_end_time = addDelay(end_time, delay)
            
            new_times = new_start_time + " --> " + new_end_time + "\n"
            writer.write(new_times)
        else:
            writer.write(lines[line_counter])
        line_counter += 1
    
        # Now we are in the dialogue part
        # Clear formatting if necessary
        while line_counter < len(lines) and not lines[line_counter][:-1].isdigit():
            if clear_format:
                new_line = clearFormat(lines[line_counter])
                writer.write(new_line)
            else:
                writer.write(lines[line_counter])
                                                                                                              
            line_counter += 1
    
    reader.close()
    writer.close()


# Takes a time and a delay and returns a new time with the delay added
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


# Clears format of string
def clearFormat(line):
    # Clear bold letters
    line = line.replace("<b>", "")
    line = line.replace("</b>", "")
    line = line.replace("{b}", "")
    line = line.replace("{/b}", "")

    # Clear italics
    line = line.replace("<i>", "")
    line = line.replace("</i>", "")
    line = line.replace("{i}", "")
    line = line.replace("{/i}", "")

    # Clear underlines
    line = line.replace("<u>", "")
    line = line.replace("</u>", "")
    line = line.replace("{u}", "")
    line = line.replace("{/u}", "")

    # Clear font opening
    f = 0
    while f != -1:
        f = line.find("<font")
        if f == -1:
            f = line.find("{font")
        
        if f != -1:
            f_end = line[f:].find(">") + f
            if f_end == -1:
                f_end = line[f:].find("}") + f

            line = line[:f] + line[f_end + 1:]

    # Clear font closing
    line = line.replace("</font>", "")
    line = line.replace("{/font}", "")

    # Clear positioning
    p = 0
    while p != -1:
        p = line.find("</a")
        if p == -1:
            p = line.find("{/a")

        if p != -1:
            p_end = line[p:].find(">") + p
            if p_end == -1:
                p_end = line.find("}") + p

            line = line[:p] + line[p_end + 1:]
    
    return line


if __name__ == "__main__":
    main()
