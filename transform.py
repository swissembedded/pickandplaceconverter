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
        item = 'C0603'
    elif item == 'CAP_0805':
        item = 'C0805'
    elif item == 'SOD-323':
        item = 'SOD323'
    elif item == 'SOT23_L':
        item = 'SOT23-3'
    elif item == 'MF_PSMF':
        item = 'MF-PSMF0XXX'
    elif item == 'D8':
        item = 'SOIC8'
    elif item == 'SOT23-3N':
        item = 'SOT23-3'
    elif item == 'SOT23-6L':
        item = 'SOT23-6'
    elif item == 'TSL257T_(PACKAGE_T)':
        item = 'TSL257T'
    elif item == 'SOT95P245X110-5N':
        item = 'SOT23-5'
    elif item == 'SOT23' :
        item = 'SOT23-3'
    elif item == 'MCHP-SOT-23-OT6_M':
        item = 'SOT23-6'

    #elif item == 'INDC1608X95N':
    #    item = 'F0603'
    #elif item == 'D8':
    #    item = 'SOIC8'
    #elif item == 'CAPC2012X145N':
    #    item = 'C0805'
    
    return item

# xxxR -> xxx
# xKx -> x.xk
# xMx -> x.xM
# RES 34K 0603 1% -> 34k
    #if item[3] == 'R' and len(item) == 4:
    #    return item[:3]
    #if item[1] == 'K' and len(item) == 3:
    #    return item[0] + '.' + item[2] + 'k'
    #if item[1] == 'M' and len(item) == 3:
    #    return item[0] + '.' + item[2] + 'M'
    #if item == 'RES 34K 0603 1%':
    #    return '34k'

# xxxnF -> xxxn
# xxxuF -> xxxu
# xxxpF -> xxxp
# xuxF -> x.xu
# xnxF -> x.xn
# xpxF -> x.xp
# CAP 4n7, 0603, 50V -> 4.7n
def convert_value(item):
    if item == 'MF-PSMF020X-2':
        item = 'MF-PSMF020X'
    elif item[:8] == 'BC817-40' :
        item = 'BC817'  
    return item

    #if item[3:5] == 'nF' and len(item) == 5:
    #    return item[:4]
    #if item[3:5] == 'uF' and len(item) == 5:
    #    return item[:4]
    #if item[1] == 'u' and item[3] == 'F' and len(item) == 4:
    #    return item[0] + "." + item[2] + 'u'
    #if item[1] == 'n' and item[3] == 'F' and len(item) == 4:
    #    return item[0] + "." + item[2] + 'n'
    #if item[1] == 'p'  and item[3] == 'F' and len(item) == 4:
    #    return item[0] + '.' + item[2] + 'p'
    #if item == 'CAP 4n7, 0603, 50V':
    #    return '4.7n'

    #if item[3:5] == 'nF' and len(item) == 5:
    #    return item[:4]
    #if item[3:5] == 'uF' and len(item) == 5:
    #    return item[:4]
    #if item[1] == 'u' and item[3] == 'F' and len(item) == 4:
    #    return item[0] + "." + item[2] + 'u'
    #if item[1] == 'n' and item[3] == 'F' and len(item) == 4:
    #    return item[0] + "." + item[2] + 'n'
    #if item[1] == 'p'  and item[3] == 'F' and len(item) == 4:
    #    return item[0] + '.' + item[2] + 'p'
    #if item == 'CAP 4n7, 0603, 50V':
    #    return '4.7n'

# TopLayer -> TOP
# BottomLayer -> BOT
def convert_side(item):
    return item[:3].upper()

# 360 -> 360.0
def convert_rotation(item):    
    return "{:.1f}".format(float(item))

def convert_reference(item):
    return item

def correct_angle(rotation, correction):
    angle = float(rotation)
    angle += correction
    if angle > 360.0:
        angle-=360.0
    return "{:.1f}".format(float(angle))

def convert_entry(ref, x, y, side, rotation, footprint, value, ignore):
    # rules for mechatronika vision M10V
    # Testpoints
    if footprint=='TP' or value =='TP' or ref[:2]=='TP':
        ignore = True
    # Mechanical mounts, except fiducials, they are needed for vision to calculate pcb offset
    elif ref[:1] == 'M' and footprint!='PASSER-KREIS':
        ignore = True
    # THT diodes
    elif value[:3] == 'SFH' :
        ignore = True
    # all sort of connectors, place by hand for now
    elif ref[:1]=='J' or ref[:1]=='X':
        ignore = True
    elif (footprint == 'L0805' or footprint == 'L0603') and value[:5] == 'BLM21':
        # Black ferrite package, use different footprint for vision
        footprint = 'F0805'                  
    
    # Rotate some components
    if footprint == 'SOT23-3' or footprint=='TI_SIL' or footprint == 'SOIC8' or footprint == 'MCP9808-DFN' or footprint=='TSL257T' or footprint=='SM1204BC' or footprint =='ILD205T' or footprint=='SOT23-5' or (footprint == 'SOT23-6' and value=='24AA025E48T-I/OT'):
        # rotate 90° clockwise on toplayer or 90° counterclockwise on bottomlayer
        if side == 'TOP':
            rotation=correct_angle(rotation, 270.0)
        else:
            rotation=correct_angle(rotation, 90.0)
    #elif  :
    # rotate 90° counterclockwise on toplayer or 90° clockwise on bottomlayer
    #    if side == 'TOP':
    #        rotation=correct_angle(rotation, 90.0)
    #    else:
    #        rotation=correct_angle(rotation, 270.0)
    elif footprint == 'SOT23-6':
        # rotate 180° 
        rotation=correct_angle(rotation, 180.0)


     #elif footprint == 'TI_SIL' or footprint == 'SOIC8':
     #   # rotate 90° clockwise on toplayer or 90° counterclock on bottomlayer
     #   if side == 'TOP':
     #       rotation=correct_angle(rotation, 270.0)
     #   else
     #       rotation=correct_angle(rotation, 90.0)
                     
        
    return ref, x, y, side, rotation, footprint, value, ignore

#convert line
def convert_line(header, line):
    conv_line = []
    ignore = False
    #if designator begin with R or C, ignore this line
    #if line[0][0] == "R" or line[0][0] == "C":
    #    ignore = True
    #    return conv_line, ignore

    # parse values
    for i, item in enumerate(line):
        if header[i] == 'Side':
            side = convert_side(item)

        if header[i] == 'Rotation':
            rotation = convert_rotation(item)

        if header[i] == 'Package':
            footprint = convert_footprint(item)

        if header[i] == 'Value':
            value = convert_value(item)

        if header[i] == 'Center X':
            x = item

        if header[i] == 'Center Y':
            y = item

        if header[i] == 'Ref':
            ref = convert_reference(item)
        
    ref, x, y, side, rotation, footprint, value, ignore = convert_entry(ref, x, y, side, rotation, footprint, value, ignore)

    # fillin converted line                                
    for i, item in enumerate(line):
                
        if header[i] == 'Side':
            conv_line.append(side)
            
        if header[i] == 'Rotation':
            conv_line.append(rotation)
                             
        if header[i] == 'Package':
            conv_line.append(footprint)
            
        if header[i] == 'Value':
            conv_line.append(value)

        if header[i] == 'Center X':
            conv_line.append(x)

        if header[i] == 'Center Y':
            conv_line.append(y)

        if header[i] == 'Ref':
            conv_line.append(ref)        

    return conv_line, ignore
