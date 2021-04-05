# Import and reexport altium cad pick and place files
# This file is part of the pickandplaceconverter project distribution (https://github.com/swissembedded/pickandplaceconverter.git).
# Copyright (c) 2019 by Daniel Haensse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import transform
import os
import csv

# get header from pick and place file
def get_header(line):
    head = []
    for i, x in enumerate(line):
        #consider Mid X, Mid Y, Mid Z as one column
        if x == "X" or x == "Y" or x == "Z" :
            l = len(head)
            head[l-1] += " " + x
        else:
            head.append(x)
    return head, len(head)

def get_content(line, cols):
    row = []
    for i, x in enumerate(line):
        if i < cols :
            row.append(x)
        else:
            l = len(row)
            row[l-1] += " " + x
    return row


def export_pick_place_csv(data, header, f):
    with open(f, mode='w', newline='') as file:
        writer = csv.writer(file,quoting=csv.QUOTE_NONNUMERIC)
        newData = []
        newData.append(header)
        for i, line in enumerate(data):
            line, ignore = transform.convert_line(header, line)
            if ignore == True:
                continue
            newData.append(line)
        writer.writerows(newData)

#
def process_csv_header(row):
    header = []
    rowMap = []
    # we are building 
    # <Ref>, <Package>, <Value>, <CenterX>, <CenterY>, <Rotation>, <Side>
    field_remap = {
        'Designator': 'Ref',
        'Layer': 'Side',
        'Footprint': 'Package',
        'Center-X(mm)': 'Center X',
        'Center-Y(mm)': 'Center Y',
        'value': 'Value',
        'Rotation': 'Rotation'
    }
    field_idx = {
        'Ref': 0,
        'Package': 1,
        'Value': 2,
        'Center X': 3,
        'Center Y': 4,
        'Rotation': 5,
        'Side': 6
    }
    for i, field in enumerate(field_idx):
        header.append(field)
    for i, field in enumerate(row):
        if field in field_remap:
            rowMap.append( field_idx[field_remap[field]] )
        else:
            rowMap.append(-1)   # drop
    return header, rowMap

#
def import_pick_place_csv(file):
    data = []
    header = []
    rowMap = []
    cols = 0
    with open(file) as f:
        reader = csv.reader(f,delimiter=',')
        header_processed = False
        for row in reader:
            if len(row) > 1:
                if header_processed == False:
                    header, rowMap = process_csv_header(row)
                    header_processed = True
                else:
                    crow = [None] * len(header)
                    for i, field in enumerate(row):
                        if rowMap[i] >= 0:
                            crow[rowMap[i]] = field
                    data.append(crow)
    return data, header

if len(sys.argv) != 3:
    print(
        "arguments, For example\n"
        "./convert.py in_pp_file.csv out_pp_file.csv\n")
    exit()

in_pp_file = sys.argv[1]
out_pp_file = sys.argv[2]

filename, ext_in = os.path.splitext(in_pp_file)
filename, ext_out = os.path.splitext(out_pp_file)

pp, header = import_pick_place_csv(in_pp_file)

export_pick_place_csv(pp, header, out_pp_file)

print(pp)
