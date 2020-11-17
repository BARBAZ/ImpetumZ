
###################################################################### Preprocessing ######################################################################

###### Python Builtin modules #####

import io
import os
import struct
import sys

##### Autodesk Maya's API Modules #####

import maya.cmds as cmds
import maya.api.OpenMaya as om

###########################################################################################################################################################

############################################################## Variables / Arrays Definitions ##############################################################

##### Variables #####



##### Arrays #####



##### Dictionnaries #####

Animation = {}

##### Constants #####



##### Functions / classes #####

# Assigned Objects #



###########################################################################################################################################################

################################################################## Functions Definitions ##################################################################

##### Maya Functions #####

# ImpetumZ #

def keyframe12(): 
    Byte_0 = xsm.read(1)
    Byte_1 = xsm.read(1)
    Bytes0 = struct.pack('2c0l', Byte_0, Byte_1)
    Quat0 = struct.unpack('<f', Bytes0)
    Byte_2 = xsm.read(1)
    Byte_3 = xsm.read(1)
    Bytes1 = struct.pack('2c0l', Byte_2, Byte_3)
    Quat1 = struct.unpack('<f', Bytes1)
    Byte_4 = xsm.read(1)
    Byte_5 = xsm.read(1)
    Bytes2 = struct.pack('2c0l', Byte_4, Byte_5)
    Quat2 = struct.unpack('<f', Bytes2)  
    Byte_6 = xsm.read(1)
    Byte_7 = xsm.read(1)
    Bytes3 = struct.pack('2c0l', Byte_6, Byte_7)
    Quat3 = struct.unpack('<f', Bytes3)
    Time = struct.unpack('<f', xsm.read(4))
    return Quat0, Quat1, Quat2, Quat3, Time

def keyframe16():
    Float0 = struct.unpack('<f', xsm.read(4))
    Float1 = struct.unpack('<f', xsm.read(4))
    Float2 = struct.unpack('<f', xsm.read(4))
    Float3 = struct.unpack('<f', xsm.read(4))
    return Float0, Float1, Float2, Float3
    
##### Pythonic Functions #####

# Array Operations #

def Log_Arrays(array):
    print ""
    for i in range(len(array)):
        element = array[i]
        print element
    print ""

# Strings Operations #

def Clean_Name(text):
    text1 = text.replace(' ','_')
    text2 = text1.replace('.','_')
    text3 = text2.replace('\x00','')
    Object_string = "Object_"
    Strings = (Object_string, text3)
    text4 = "".join(Strings)
    return text4

# IO

def Open_File():
    fullpath = cmds.fileDialog2(fileMode=1)
    fullpath = str(fullpath[0])
    cnt = fullpath.count("/")
    splitpath = fullpath.split("/")
    filename = splitpath[cnt]
    realpath = fullpath.replace(filename,"")
    os.chdir(realpath)
    file_object = io.open(filename,'r+b')
    return file_object

# ImpetumZ #

def File_Header(file_object):
    xsm = file_object
    xsm.seek(16, os.SEEK_CUR)
    return xsm

def File_MetaData(file_object):
    xsm = file_object
    xsm.seek(20, os.SEEK_CUR)
    SoftName_Length = struct.unpack('<I', xsm.read(4))[0]
    SoftName = xsm.read(SoftName_Length)
    SoftPath_Length = struct.unpack('<I', xsm.read(4))[0]
    SoftPath = xsm.read(SoftPath_Length)
    CompileDate_Length = struct.unpack('<I', xsm.read(4))[0]
    CompileDate = xsm.read(CompileDate_Length)
    xsm.seek(4, os.SEEK_CUR)
    xsm.seek(12, os.SEEK_CUR)
    Object_Count = struct.unpack('<I', xsm.read(4))[0]
    return xsm, Object_Count #, SoftName, SoftPath, CompileDate

def FileData():
    xsm.seek(16, os.SEEK_CUR)
    xsm.seek(16, os.SEEK_CUR)
    xsm.seek(24, os.SEEK_CUR)
    xsm.seek(24, os.SEEK_CUR)
    Type0_Count = struct.unpack('<I', xsm.read(4))[0]
    Type1_Count = struct.unpack('<I', xsm.read(4))[0]
    Type2_Count = struct.unpack('<I', xsm.read(4))[0]
    Type3_Count = struct.unpack('<I', xsm.read(4))[0]
    xsm.seek(4, os.SEEK_CUR) # C++ compiler delimiter 0xFFFF7F7F
    BoneName_Length = struct.unpack('<I', xsm.read(4))[0]
    BoneName = xsm.read(BoneName_Length)
    print Clean_Name(BoneName)
    Keyframes0 = []
    Keyframes1 = []
    Keyframes2 = []
    Keyframes3 = []

    for i in range(Type0_Count):
        Keyframes0.append([])
        Keyframes0[i].append(keyframe16())
    for i in range(Type1_Count):
        Keyframes1.append([])
        Keyframes1[i].append(keyframe12())
    for i in range(Type2_Count):
        Keyframes2.append([])
        Keyframes2[i].append(keyframe16())
    for i in range(Type3_Count):
        Keyframes3.append([])
        Keyframes3[i].append(keyframe12())

    Log_Arrays(Keyframes0)
    Log_Arrays(Keyframes1)
    Log_Arrays(Keyframes2)
    Log_Arrays(Keyframes3)
    return Keyframes0, Keyframes1, Keyframes2, Keyframes3, BoneName


###########################################################################################################################################################

################################################################### Script instructions ###################################################################

Args = File_MetaData(File_Header(Open_File()))
xsm = Args[0]

for i in range(Args[1]):
    Args0 = FileData()
    for i in range(3):
        if(len(Args0[i]) > 0):
            Animation[Args0[4]] = Args0[i]
  
print "EOF"
xsm.close()
print "\n"
print "EOS"

###########################################################################################################################################################
