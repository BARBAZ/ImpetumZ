
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

Temp_data = []

##### Dictionnaries #####

Animation = {}

##### Constants #####



##### Functions / classes #####

# Assigned Objects #

###########################################################################################################################################################

################################################################## Functions Definitions ##################################################################

##### Maya Functions #####

# Math

max = 32767.0
min = max * -1

def Calc_Quat(Short):
    if(Short <= max and Short >= min):
            Quat = Short / max
    else:
        print "internal error value out of range ! Killing process"
        return sys.exit()

    return Quat

def Negate(Var):
    Switched_Var = Var * -1
    return Switched_Var

# Debug

def Set_Quat(Joint,x,y,z,w):
    Transform = om.MFnTransform(Get_MObject(Joint))
    MQuat = om.MQuaternion(x,y,z,w)
    Transform.setRotation(MQuat, 2)
    del Transform


def Get_Rot(Joint, Mode):
    Transform = om.MFnTransform(Get_MObject(Joint))
    return Transform.rotation(2, Mode)

def Joint_Anim_Test(KeyframesList, Joint):
    for i in range(len(KeyframesList[1])):
        x = KeyframesList[1][i][0]
        y = KeyframesList[1][i][1]
        z = KeyframesList[1][i][2]
        w = KeyframesList[1][i][3]
        Set_Quat(Joint,x,y,z,w)
        cmds.setKeyframe(Joint , t=[i+1])
     

##### Pythonic Functions #####

# Array Operations #

def Log_Arrays(array):
    print ""
    for i in range(len(array)):
        element = array[i]
        print element
    print ""

def Exist_Names(text):
    exist = 0
    for j in range(len(Names)):
        if(Names[j][2][0] == text):
            exist = 1
    return exist

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
    print file_object
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

def keyframe12():
    Short0 = struct.unpack('<h',xsm.read(2))[0]
    Short1 = struct.unpack('<h',xsm.read(2))[0]
    Short2 = struct.unpack('<h',xsm.read(2))[0]
    Short3 = struct.unpack('<h',xsm.read(2))[0]
    Float = struct.unpack('<f', xsm.read(4))[0]
    return Short0, Short1, Short2, Short3, Float

def keyframe16():
    Float0 = struct.unpack('<f', xsm.read(4))[0]
    Float1 = struct.unpack('<f', xsm.read(4))[0]
    Float2 = struct.unpack('<f', xsm.read(4))[0]
    Float3 = struct.unpack('<f', xsm.read(4))[0]
    return Float0, Float1, Float2, Float3

def FileData():
    xsm.seek(16, os.SEEK_CUR)
    xsm.seek(16, os.SEEK_CUR)
    xsm.seek(24, os.SEEK_CUR)
    xsm.seek(24, os.SEEK_CUR)
    Type0_Count = struct.unpack('<I', xsm.read(4))[0]
    Type1_Count = struct.unpack('<I', xsm.read(4))[0]
    Type2_Count = struct.unpack('<I', xsm.read(4))[0]
    Type3_Count = struct.unpack('<I', xsm.read(4))[0]
    print("Translation Keyframes %d" % (Type0_Count) )
    print("Rotation Keyframes %d" % (Type1_Count) )
    xsm.seek(4, os.SEEK_CUR) # C++ compiler delimiter 0xFFFF7F7F
    BoneName_Length = struct.unpack('<I', xsm.read(4))[0]
    BoneName = xsm.read(BoneName_Length)
    BoneName = Clean_Name(BoneName)
    #print BoneName
    Keyframes0 = []
    Keyframes1 = []
    Keyframes2 = []
    Keyframes3 = []

    for i in range(Type0_Count):
        Keyframes0.append([])
        Tuple0 = keyframe16()
        x0 = Tuple0[0]
        y0 = Tuple0[1]
        z0 = Tuple0[2]
        time0 = Tuple0[3]
        Keyframes0[i].append(x0)
        Keyframes0[i].append(y0)
        Keyframes0[i].append(z0)
        Keyframes0[i].append(time0)

    for i in range(Type1_Count):
        Keyframes1.append([])
        Tuple1 = keyframe12()
        x1 = Calc_Quat(Tuple1[0])
        y1 = Calc_Quat(Tuple1[1])
        z1 = Calc_Quat(Tuple1[2])
        w1 = Calc_Quat(Tuple1[3]) 
        time1 = Tuple1[4]
        Keyframes1[i].append(x1)
        Keyframes1[i].append(y1)
        Keyframes1[i].append(z1)
        Keyframes1[i].append(w1)
        Keyframes1[i].append(time1)

    for i in range(Type2_Count):
        Keyframes2.append([])
        Tuple2 = keyframe16()
        x2 = Tuple2[0]
        y2 = Tuple2[2]
        z2 = Tuple2[1]
        time2 = Tuple2[3]
        Keyframes2[i].append(x2)
        Keyframes2[i].append(y2)
        Keyframes2[i].append(z2)
        Keyframes2[i].append(time2)

    for i in range(Type3_Count):
        Keyframes3.append([])
        Tuple3 = keyframe12()
        x3 = Tuple3[0]
        y3 = Tuple3[1]
        z3 = Tuple3[2]
        w3 = Tuple3[3]
        time3 = Tuple3[4]
        Keyframes3[i].append(w3)
        Keyframes3[i].append(x3)
        Keyframes3[i].append(y3)
        Keyframes3[i].append(z3)
        Keyframes3[i].append(time3)

    print BoneName
    Log_Arrays(Keyframes0)
    Log_Arrays(Keyframes1)
    Log_Arrays(Keyframes2)
    Log_Arrays(Keyframes3)

    Tuple = (Keyframes0, Keyframes1, Keyframes2, Keyframes3)
    return BoneName, Tuple

def Bind_Keyframes(Keyframe_Count):
    for i in range(Keyframe_Count - 1):
        for key in Animation:
            if(Exist_Names(key)):
                Transform = om.MFnTransform(Get_MObject(key))
                Keyframes_Lists = Animation.get(key)
                List0 = Keyframes_Lists[0]
                List1 = Keyframes_Lists[1]
                List2 = Keyframes_Lists[2]
                List3 = Keyframes_Lists[3]
                Prompt = raw_input()
                if(Prompt == 1):
                    sys.exit()
                else:
                    pass
                if(len(List0) > 0):
                    pass
                    '''
                    Vec3_0 = om.MVector(List0[i+1][0], List0[i+1][1], List0[i+1][2])
                    Transform.setTranslation(Vec3_0,2)'''
                if(len(List1) > 0):
                    rx0 = List1[i][0]
                    ry0 = List1[i][2]
                    rz0 = List1[i][1]
                    rw0 = List1[i][3]
                    Quat_0 = om.MQuaternion(rx0, ry0, Switch_Sign(rz0), rw0)
                    Transform.setRotation(Quat_0,2)
                if(len(List2) > 0):
                    pass
                if(len(List3) > 0):
                    pass

        cmds.setKeyframe(t=[i+1])


###########################################################################################################################################################

################################################################### Script instructions ###################################################################

Args = File_MetaData(File_Header(Open_File()))
xsm = Args[0]

for i in range(Args[1]):
    Args0 = FileData()
    Animation[Args0[0]] = Args0[1]
    if(Args0[0] == "Object_Bip01"):
        Temp_data0 = Args0[1]
    if(Args0[0] == "Object_Bip01_L_Thigh"):
        Temp_data1 = Args0[1]
    if(Args0[0] == "Object_Bip01_R_Thigh"):
        Temp_data2 = Args0[1]
    if(Args0[0] == "Object_Bip01_L_Calf"):
        Temp_data3 = Args0[1]
    if(Args0[0] == "Object_Bip01_R_Calf"):
        Temp_data4 = Args0[1]
    if(Args0[0] == "Object_Bip01_Spine"):
        Temp_data5 = Args0[1]
    if(Args0[0] == "Object_Bip01_Spine1"):
        Temp_data6 = Args0[1]
    if(Args0[0] == "Object_Bip01_Spine2"):
        Temp_data7 = Args0[1]
    if(Args0[0] == "Object_Bip01_Neck"):
        Temp_data8 = Args0[1]
    if(Args0[0] == "Object_Bip01_Head"):
        Temp_data9 = Args0[1]
    if(Args0[0] == "Object_Bip01_L_UpperArm"):
        Temp_data10 = Args0[1]
    if(Args0[0] == "Object_Bip01_L_Forearm"):
        Temp_data11 = Args0[1]
    if(Args0[0] == "Object_Bip01_R_UpperArm"):
        Temp_data12 = Args0[1]
    if(Args0[0] == "Object_Bip01_R_Forearm"):
        Temp_data13 = Args0[1]

Joint_Anim_Test(Temp_data3, "Object_Bip01_L_Calf")
        
#Keyframe_Count = len(Tuple[1])
#Bind_Keyframes(Keyframe_Count)
print "EOF"
xsm.close()
print "\n"
print "EOS"
