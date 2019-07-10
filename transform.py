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


#convert line
def convert_line(line):
    conv_line = []
    ignore = False
    #if designator begin with R or C, ignore this line
    if line[0][0] == "R" or line[0][0] == "C":
        ignore = True
        return conv_line, ignore

    for i, item in enumerate(line):
        #we will add converstion formula about every item on here
        conv_line.append(item)

    return conv_line, ignore
