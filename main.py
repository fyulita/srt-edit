import argparse
import os
from shift import shift
from format import formatting


parser = argparse.ArgumentParser(prog="srt-edit", description="A simple tool to adjust .srt subtitles to video.")

parser.add_argument("-c", "--no-format", action="store_true", help="clear formatting")
parser.add_argument("file", type=str, help="input .srt file")
parser.add_argument("-s", "--shift", type=int, help="shift subtitles by DELAY (in ms)")

args = parser.parse_args()

no_format = args.no_format
file = args.file
delay = args.shift

if file[-4:] != ".srt":
    print(f"srt-edit: error: argument -f/--file: invalid .srt file: '{file}'")
else:
    original_file = file[:-4] + ".original.srt"
    os.rename(file, original_file)
    if not delay is None:
        shift(original_file, delay, no_format)
    elif no_format:
        formatting(original_file)
    else:
        print(f"srt-edit: error: no instruction given")
