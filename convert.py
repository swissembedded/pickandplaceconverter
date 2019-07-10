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

def import_pick_place(file):
    data = []
    cols = 0
    with open(file) as f:
        lines = [line.split() for line in f]
        
        pass_header = False

        for i, x in enumerate(lines):
            if len(x) == 0:
                continue
            if pass_header == False:
                head, cols = get_header(x)
                data.append(head)     
                pass_header = True
            else:
                row = get_content(x, cols)
                data.append(row)
    return data

def export_pick_place(data, f):
    with open(f, mode='w') as file:
        for i, line in enumerate(data):
            # not convert first line
            if i == 0:
                for j, item in enumerate(line):
                    file.write('%-15s' % (item))
                # add a space line after header
                file.write('\n\n')
                continue
            #convert line
            line, ignore = transform.convert_line(line)
            #if ignore line, do not export
            if ignore == True:
                continue
            #print line
            for j, item in enumerate(line):
                file.write('%-15s' % (item))
            file.write('\n')


if len(sys.argv) != 3:
    print(
        "arguments, For example\n"
        "./convert.py in_pp_file.txt out_pp_file.txt\n")
    exit()

in_pp_file = sys.argv[1]
out_pp_file = sys.argv[2]

pp = import_pick_place(in_pp_file)
export_pick_place(pp, out_pp_file)

print(pp)
