
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



##### Constants #####



##### Functions / classes #####

# Assigned Objects #



###########################################################################################################################################################

################################################################## Functions Definitions ##################################################################

##### Maya Functions #####

# UI #


# 3D #


# Anim #


         
##### Pythonic Functions #####

# Array Operations #

def Log_Arrays(array):
    print ""
    for i in range(len(array)):
        element = array[i]
        print element
    print ""

def create_list(itm_cnt, list, num_element): # Itm_cnt = numbers of items in list - list = an initialized python list item - Num_element = number of element per row 
    index = 0
    for i in range(itm_cnt):
        list.append([])
        for j in range(num_element):
            list[index].append([])
        index += 1
    return list

# Strings Operations #

def Clean_Name(text):
    text1 = text.replace(' ','_')
    text2 = text1.replace('.','_')
    text3 = text2.replace('\x00','')
    Object_string = "Object_"
    Strings = (Object_string, text3)
    text4 = "".join(Strings)
    return text4

# ImpetumZ #

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

def File_Header(file_object):
    xsm = file_object
    print xsm.tell()
    xsm.seek(16, os.SEEK_CUR)
    return xsm

def File_MetaData(file_object):
    xsm = file_object
    print xsm.tell()
    xsm.seek(20, os.SEEK_CUR)
    SoftName_Length = struct.unpack('<I', xsm.read(4))[0]
    print SoftName_Length
    SoftName = xsm.read(SoftName_Length)
    SoftPath_Length = struct.unpack('<I', xsm.read(4))[0]
    print SoftPath_Length
    SoftPath = xsm.read(SoftPath_Length)
    CompileDate_Length = struct.unpack('<I', xsm.read(4))[0]
    print CompileDate_Length
    CompileDate = xsm.read(CompileDate_Length)
    xsm.seek(4, os.SEEK_CUR)
    xsm.seek(12, os.SEEK_CUR)
    Object_Count = struct.unpack('<I', xsm.read(4))[0]
    return xsm, Object_Count #, SoftName, SoftPath, CompileDate

def FileData(file_object):
    xsm = file_object
    print xsm.tell()
    xsm.seek(16, os.SEEK_CUR)
    xsm.seek(16, os.SEEK_CUR)
    xsm.seek(24, os.SEEK_CUR)
    xsm.seek(24, os.SEEK_CUR)
    Type0_Count = struct.unpack('<I', xsm.read(4))[0]
    Type1_Count = struct.unpack('<I', xsm.read(4))[0]
    Type2_Count = struct.unpack('<I', xsm.read(4))[0]
    Type3_Count = struct.unpack('<I', xsm.read(4))[0]
    if(Type0_Count > 0):
        print "Type 0 anim"
    if(Type1_Count > 0):
        print "Type 1 anim"
    if(Type2_Count > 0):
        print "Type 2 anim"
    if(Type3_Count > 0):
        print "Type 3 anim"
    xsm.seek(4, os.SEEK_CUR)
    BoneName_Length = struct.unpack('<I', xsm.read(4))[0]
    print xsm.tell()
    BoneName = xsm.read(BoneName_Length)
    print BoneName
    for i in range(Type0_Count):
        xsm.seek(16, os.SEEK_CUR)
    for i in range(Type1_Count):
        xsm.seek(12, os.SEEK_CUR)
    for i in range(Type2_Count):
        xsm.seek(16, os.SEEK_CUR)
    for i in range(Type3_Count):
        xsm.seek(12, os.SEEK_CUR)
    
    return xsm  #, KeyFrames_Count, BonesName
    
 
###########################################################################################################################################################

################################################################### Script instructions ###################################################################

Args = File_MetaData(File_Header(Open_File()))
print Args
xsm = Args[0]

for i in range(Args[1]):
    FileData(xsm)

print xsm.tell()
print "EOF"
xsm.close()
print "\n"
print "EOS"

###########################################################################################################################################################
