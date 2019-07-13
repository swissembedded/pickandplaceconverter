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

# RES_0402 -> R0402
# RES_0603 -> R0603
# RES_0805 -> R0805
# CAP_0402 -> C0402
# CAP_0603 -> C0603
# CAP_0805 -> C0805
# SOT23 -> SOT23-3
# SOT23-6L -> SOT23-6
# SOT23_L -> SOT23-3
# MCHP-SOT-23-OT6_M -> SOT23-6
# INDC1608X95N -> F0603
# D8 -> SOIC8
# CAPC2012X145N -> C0805
def convert_footprint(item):
    if item == 'RES_0402':
        item = 'R0402'
    elif item == 'RES_0603':
        item = 'R0603'
    elif item == 'RES_0805':
        item = 'R0805'
    elif item == 'CAP_0402':
        item = 'C0402'
    elif item == 'CAP_0603':
        item == 'C0603'
    elif item == 'CAP_0805':
        item = 'C0805'
    elif item == 'SOT23':
        item = 'SOT23-3'
    elif item == 'SOT23-6L':
        item = 'SOT23-6'
    elif item == 'SOT23_L':
        item = 'SOT23-3'
    elif item == 'MCHP-SOT-23-OT6_M':
        item = 'SOT23-6'
    elif item == 'INDC1608X95N':
        item = 'F0603'
    elif item == 'D8':
        item = 'SOIC8'
    elif item == 'CAPC2012X145N':
        item = 'C0805'
    return item

# xxxR -> xxx
# xKx -> x.xk
# xMx -> x.xM
# RES 34K 0603 1% -> 34k
def convert_comment_fomular1(item):
    if item[3] == 'R' and len(item) == 4:
        return item[:3]
    if item[1] == 'K' and len(item) == 3:
        return item[0] + '.' + item[2] + 'k'
    if item[1] == 'M' and len(item) == 3:
        return item[0] + '.' + item[2] + 'M'
    if item == 'RES 34K 0603 1%':
        return '34k'
    return item
# xxxnF -> xxxn
# xxxuF -> xxxu
# xxxpF -> xxxp
# xuxF -> x.xu
# xnxF -> x.xn
# xpxF -> x.xp
# CAP 4n7, 0603, 50V -> 4.7n
def convert_comment_fomular2(item):
    if item[3:5] == 'nF' and len(item) == 5:
        return item[:4]
    if item[3:5] == 'uF' and len(item) == 5:
        return item[:4]
    if item[1] == 'u' and item[3] == 'F' and len(item) == 4:
        return item[0] + "." + item[2] + 'u'
    if item[1] == 'n' and item[3] == 'F' and len(item) == 4:
        return item[0] + "." + item[2] + 'n'
    if item[1] == 'p'  and item[3] == 'F' and len(item) == 4:
        return item[0] + '.' + item[2] + 'p'
    if item == 'CAP 4n7, 0603, 50V':
        return '4.7n'
    return item

#convert line
def convert_line(header, line):
    conv_line = []
    ignore = False
    #if designator begin with R or C, ignore this line
    #if line[0][0] == "R" or line[0][0] == "C":
    #    ignore = True
    #    return conv_line, ignore

    for i, item in enumerate(line):
        #convert footprint
        if header[i] == 'Footprint':
            item = convert_footprint(item)
            footprint = item
        if header[i] == 'Comment':
            if footprint == 'RES_0402' or footprint == 'RES_0603' or footprint == 'RES_0805':
                item = convert_comment_fomular1(item)

            if footprint == 'CAP_0402' or footprint == 'CAP_0603' or footprint == 'CAP_0805':
                item = convert_comment_fomular2(item)

        conv_line.append(item)

    return conv_line, ignore
