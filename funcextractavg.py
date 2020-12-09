#!/bin/python3

import os
import re
import csv

def computeAvg(file, fdmap):
    with open(file, 'r') as infile:
        reader = csv.DictReader(infile, delimiter='\t', skipinitialspace=True)
        count = 0
        sum = 0.0
        for row in reader:
            val = row['framewise_displacement']
            try:
                f = float(val)
                sum += f
                count += 1
            except:
                continue

        fdmap[file] = sum / count if count  != 0 else 0

def calcavg(sdir, fdmap):
    os.chdir(sdir)
    files = os.listdir()
    for file in files:
        if re.search("regressors.tsv", file):
            computeAvg(file, fdmap)

def explore(dir, fdmap):
    os.chdir(dir)
    subdirs = os.listdir()
    for sdir in subdirs:
        if os.path.isdir(sdir) and sdir == "func":
            cwd = os.getcwd()
            calcavg(sdir, fdmap)
            os.chdir(cwd)

if __name__ == '__main__':

    # you can set the os.environ['OUTPUT_FILE'] and os.environ['INPUT_PATH'] below or,
    # outside from this app
    os.environ['OUTPUT_FILE'] = os.getcwd() + '/' + 'result.tsv'
    os.environ['INPUT_PATH']  = os.getcwd()

    fptr = open(os.environ['OUTPUT_FILE'], 'w')
    framewise_displacements = dict() # initialize map
    os.chdir(os.environ['INPUT_PATH'])
    subdirs = os.listdir()
    for sdir in subdirs:
        if os.path.isdir(sdir):
            cwd = os.getcwd()
            explore(sdir,framewise_displacements)
            os.chdir(cwd)

    fw_sorted_dispplacements = sorted(framewise_displacements.items())
    fw_disp_dicts = [{'file': f, 'average': avg} for f, avg in fw_sorted_dispplacements]
    with open(os.environ['OUTPUT_FILE'], mode='w') as avg_file:
        csv_writer = csv.DictWriter(avg_file, delimiter='\t', fieldnames=['file', 'average'])
        csv_writer.writeheader()
        for row in fw_disp_dicts:
            csv_writer.writerow(row)
