#!/usr/bin/python3
# Author: haxrob https://github.com/x1sec
# See LICENSE.md

import csv
import json
from datetime import datetime
import argparse
import sys

def doargs() :
    parser = argparse.ArgumentParser("Convert MVT timeline to Timesketch compatible jsonl format")
    parser.add_argument('--infile', help='MVT timeline file (default: timeline.csv)', default='timeline.csv')
    parser.add_argument('--outfile', help='jsonl output to import into Timesketch')
    args = vars(parser.parse_args())
    if args['outfile'] == None :
        sys.stderr.write("Error: must specify file to write Timesketch jsonl timeline (--outfile)\n\n")
        parser.print_help()
        sys.exit(1)
    return args
    
def convert_timeline(args) :
    lines, no_date, written = 0,0,0

    print("[+] Converting '" + args['infile'] + "'. Please wait ...")
    outfile = open(args['outfile'], 'w')
    with open(args['infile'], newline='') as csvfile :
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader :
            lines = lines + 1
            dt = row["UTC Timestamp"]
            
            # Timesketch doesn't like 1900, so we will snap it to epoch
            if dt == '0' or dt == '1900-01-01 12:00:00.000000':
                d = datetime.fromtimestamp(0)
                no_date = no_date + 1
            else :
                d = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
            iso_time = d.isoformat()
            entry = { 'datetime' : iso_time, 
                    'Event' : row['Event'], 
                    'message' : row['Description'], 
                    'Plugin' : row['Plugin']}
            x = json.dumps(entry)
            outfile.write(x + '\n')
            written = written + 1
    outfile.close()
    print("\n")
    print("[+] " + str(lines) + " entries were parsed")
    if no_date > 0 :
        print("[+] " + str(no_date) + " entries had no valid timestamp")
    print("[+] " + str(written) + " events written to file '" + args['outfile'] + "'")
def main() :
    print("Mobile Verification Toolkit (MVT) timeline to Timesketch compatible import file\n")
    args = doargs()  
    convert_timeline(args)

main()
