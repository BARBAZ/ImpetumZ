
###################################################################### Preprocessing ######################################################################

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

# Misc #

def Open_File():
    fullpath = cmds.fileDialog2(fileMode=1)
    fullpath = str(fullpath[0])
    cnt = fullpath.count("/")
    splitpath = fullpath.split("/")
    filename = splitpath[cnt]
    realpath = fullpath.replace(filename,"")
    os.chdir(realpath)
    file_object = io.open(filename,'r+b')
    Import_File(file_object)

def Main_Loop(run_count, loop):
    Open_File()    

def Import_File(file_object):
    xsm = file_object
    XSM_Magic = struct.unpack('<4p', xsm.read(4))
    print XSM_Magic
 
###########################################################################################################################################################

################################################################### Script instructions ###################################################################

Open_File()

print "\n"
print "EOS"


###########################################################################################################################################################
