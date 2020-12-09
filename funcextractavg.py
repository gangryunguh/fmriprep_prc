#!/bin/python3

import os
import re
import csv

def computeAvg(file, fdmap):
    with open(file, 'rU') as infile:
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

    framewise_displacements = dict() # initialize map
    subdirs = os.listdir()
    for sdir in subdirs:
        if os.path.isdir(sdir):
            cwd = os.getcwd()
            explore(sdir,framewise_displacements)
            os.chdir(cwd)

    fw_disp_dicts = [{'file': f, 'average': avg} for f,avg in framewise_displacements.items()]
    with open('result.csv', mode='wt') as avg_file:
        csv_writer = csv.DictWriter(avg_file, delimiter='\t', fieldnames=['file', 'average'])
        csv_writer.writeheader()
        for row in fw_disp_dicts:
            csv_writer.writerow(row)
