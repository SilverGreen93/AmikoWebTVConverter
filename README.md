# AmikoWebTVConverter
Amiko webtv list.txt converter for Amiko Set-top boxes.
This script allows conversions from Amiko format to CSV and M3U playlist and viceversa.

## Requirements
The converter is a single Python 3 script and must be used in a CLI interface.
Tested with Python 3.8 and ran in Bash for Windows.

## Usage
Syntax:

`./AmikoWebTVConverter.py <action> <source_file> <destination_file> [sort]`

Arguments:
- action = the conversion mode: w2c, w2p, p2w, p2c, c2w, c2p (Webtv/Csv/Playlist)
- source_file = the input file
- destination_file = the output file
- sort = choose to sort channels alphabetically

Examples:
- convert an Amiko webtv list to a playlist:

`./AmikoWebTVConverter.py w2p "webtv list.txt" playlist.m3u`
- convert a CSV list to an Amiko webtv list and make it sorted alphabetically:

`./AmikoWebTVConverter.py c2w playlist.csv "webtv list.txt" sort`

Tips:
- You can use the CSV format to easily open and edit the file in LibreOffice Calc or Microsoft Excel, reorganize and sort the channels according to your preferences.

## Importing the generated list to the Amiko STB
After generating the webtv list file, you must place it on a FAT32 formatted USB flash drive. The only accepted file name is "webtv list.txt".
From the WebTV menu, press the blue button on the remote (Upload) and the list will be imported.
Tested with Amiko Impulse 3.
