#!/usr/bin/env python3

# Amiko webtv list.txt converter for Amiko Set-top boxes.
# This script allows conversions from Amiko format to CSV and M3U playlist and viceversa.
# Author: Mihai Alexandru Vasiliu
# Date: 2023-03-03

import sys

amikoFileName = "webtv list.txt"
convertTypes = ["w2c", "w2p", "p2w", "p2c", "c2w", "c2p"]
sourceList = list()


def printHelp():
    print("")
    print("Error: Missing arguments!")
    print("")
    print("Syntax:")
    print("        ./AmikoWebTVConverter.py <action> <source_file> <destination_file> [sort]")
    print("")
    print("Arguments:")
    print("        - action = the conversion mode: w2c, w2p, p2w, p2c, c2w, c2p (Webtv/Csv/Playlist)")
    print("        - source_file = the input file")
    print("        - destination_file = the output file")
    print("        - sort = choose to sort channels alphabetically")
    print("")
    print("Example:")
    print("        ./AmikoWebTVConverter.py w2p \"webtv list.txt\" playlist.m3u sort\n")


def readWebTVList(fileName):
    lineNo = 0
    expectURL = False
    chanName = ""
    url = ""

    try:
        with open(fileName, "r") as wlFile:
            for line in wlFile:
                lineNo += 1
                if line.strip() == "":
                    continue
                if line.startswith("Channel name:") and not expectURL:
                    chanName = line[len("Channel name:"):]
                    expectURL = True
                elif line.startswith("URL:") and expectURL:
                    url = line[len("URL:"):]
                    sourceList.append((chanName.strip(), url.strip()))
                    expectURL = False
                elif expectURL:
                    print("Error: Input file is corrupted at line %d: URL missing for channel name: '%s'" % (lineNo, chanName.strip()))
                    exit(1)
                elif not expectURL:
                    print("Error: Input file is corrupted at line %d: Channel name missing after URL: '%s'" % (lineNo, url.strip()))
                    exit(1)
    except:
        print("Error: Cannot read from '%s'" % fileName)
        exit(1)

    if expectURL:
        print("Error: Input file is corrupted after line %d: URL missing for channel name: '%s'" % (lineNo, chanName.strip()))
        exit(1)


def readPlayList(fileName):
    lineNo = 0
    expectURL = False
    chanName = ""
    url = ""

    try:
        with open(fileName, "r") as plFile:
            for line in plFile:
                lineNo += 1
                if line.strip() == "":
                    continue
                if lineNo == 1:
                    if not line.startswith("#EXTM3U"):
                        print("Error: Input file is not the correct type! Expected '#EXTM3U' header, but current header is: '%s'" % line.strip())
                        exit(1)
                    continue
                if line.startswith("#EXTINF:") and not expectURL:
                    cpos = line.find(",")
                    if cpos < 0:
                        print("Error: Input file is corrupted at line %d: #EXTINF does not contain channel name" % lineNo)
                        exit(1)
                    chanName = line[cpos + 1:]
                    expectURL = True
                elif line.startswith("#EXTINF") and expectURL:
                    print("Error: Input file is corrupted after line %d: URL missing for channel name: '%s'" % (lineNo, chanName.strip()))
                    exit(1)
                elif line.startswith("#EXT"):
                    continue
                elif expectURL:
                    url = line
                    sourceList.append((chanName.strip(), url.strip()))
                    expectURL = False
                elif not expectURL:
                    print("Error: Input file is corrupted at line %d: Channel name missing after URL: '%s'" % (lineNo, url.strip()))
                    exit(1)
    except:
        print("Error: Cannot read from '%s'" % fileName)
        exit(1)

    if expectURL:
        print("Error: Input file is corrupted after line %d: URL missing for channel name: '%s'" % (lineNo, chanName.strip()))
        exit(1)


def readCSV(fileName):
    lineNo = 0
    chanName = ""
    url = ""

    try:
        with open(fileName, "r") as plFile:
            for line in plFile:
                lineNo += 1
                if line.strip() == "":
                    continue
                if lineNo == 1:
                    if "Channel name" not in line:
                        print("Error: CSV header must contain at least \"Channel name\",\"URL\", current header is: '%s'" % line.strip())
                        exit(1)
                    continue

                cpos = line.find(",")
                if cpos < 0:
                    print("Error: Input file is corrupted at line %d: Channel name,URL pair is missing" % lineNo)
                    exit(1)

                chanName = line[0:cpos]
                url = line[cpos + 1:]
                sourceList.append((chanName.strip().strip("\""), url.strip().strip("\"")))
    except:
        print("Error: Cannot read from '%s'" % fileName)
        exit(1)


def writeWebTVList(fileName):
    try:
        with open(fileName, "w") as wlFile:
            for element in sourceList:
                wlFile.write("Channel name:%s\n" % element[0])
                wlFile.write("URL:%s\n" % element[1])
    except:
        print("Error: Cannot write to '%s'" % fileName)
        exit(1)


def writePlayList(fileName):
    try:
        with open(fileName, "w") as plFile:
            plFile.write("#EXTM3U\n")
            for element in sourceList:
                plFile.write("#EXTINF:-1,%s\n" % element[0])
                plFile.write("%s\n" % element[1])
    except:
        print("Error: Cannot write to '%s'" % fileName)
        exit(1)


def writeCSV(fileName):
    try:
        with open(fileName, "w") as csvFile:
            csvFile.write("\"Channel name\",\"URL\"\n")
            for element in sourceList:
                csvFile.write("\"%s\",\"%s\"\n" % (element[0], element[1]))
    except:
        print("Error: Cannot write to '%s'" % fileName)
        exit(1)


def main(convertMode, inFile, outFile, sort):

    if convertMode not in convertTypes:
        print("")
        print("Error: Unknown conversion type: '%s'" % convertMode)
        print("Supported modes are: ", end = "")
        print(*convertTypes, sep = ", ")
        print("")
        exit(1)

    if str(convertMode).startswith("w"):
        print("Converting WebTV list to ", end = "")
        readWebTVList(inFile)
    elif str(convertMode).startswith("p"):
        print("Converting M3U playlist to ", end = "")
        readPlayList(inFile)
    elif str(convertMode).startswith("c"):
        print("Converting CSV to ", end = "")
        readCSV(inFile)

    if sort:
        sourceList.sort()

    if str(convertMode).endswith("w"):
        print("WebTV list")
        if outFile != amikoFileName:
            print("Warning! Amiko STB expects the filename to be '%s' in order to be uploaded correctly on the box!" % amikoFileName)
        writeWebTVList(outFile)
    elif str(convertMode).endswith("p"):
        print("M3U playlist")
        writePlayList(outFile)
    elif str(convertMode).endswith("c"):
        print("CSV")
        writeCSV(outFile)

    print("Done.")


if __name__ == "__main__":
    sort = False

    if len(sys.argv) < 4:
        printHelp()
        exit(1)

    if len(sys.argv) == 5:
        if str(sys.argv[4]) == "sort":
            sort = True

    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), sort)
