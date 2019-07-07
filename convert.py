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

import pandas as pd
import math

pp_file = "Pick Place for EnergyMeter.txt"

def get_header(line):
    head = []
    for i, x in enumerate(line):
        if x == "X" or x == "Y" or x == "Z" :
            l = len(head)
            head[l-1] += " " + x
        else:
            head.append(x)
    return head, len(head)

def get_row(line, cols):
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
                row = get_row(x, cols)
                data.append(row)
    return data
         

pp = import_pick_place(pp_file)
print(pp)
