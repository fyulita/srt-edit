# srt-edit

A simple tool to edit .srt subtitles from the command line.

## What does *srt-edit* do?

* It can shift subtitles time.
* It can remove formatting from subtitles.

## How do I use it?

If you want to, for example, shift `The_Shining_1980.en.srt` subtitles forward by 500 milliseconds then use the `-s` or `--shift` flag:

```
srt-edit -s 500 The_Shining_1980.en.srt
```

If you want to shift backwards by 1 second then run:

```
srt-edit -s -1000 The_Shining_1980.en.srt
```

As you can see, the time has to be in milliseconds. If you want to clear formatting just add the `-c` or `--clear-format` flag:

```
srt-edit --clear-format The_Shining_1980.en.srt
```

*srt-edit* changes the input file but also saves a backup with the `.original.srt` ending in case you mess up and wanna go back to the original.
