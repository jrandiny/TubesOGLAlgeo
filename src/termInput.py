import numpy as np
import transformasi
import math

import time

bacaPoint = False
pointBuffer = np.zeros((1,2))
is3D = False

validCommand = np.array(['translate','rotate','dilate','shear','stretch','custom','reflect','multiple','help'])
mainCommand = np.array(['exit','add','reset','insert','3D'])
param2Dvalid = np.array(['x', 'y', 'y=x', 'y=-x'])
param3Dvalid = np.array(['x', 'y', 'z', 'xy', 'xz', 'yz', 'y=x', 'y=-x', 'y=z', 'y=-z', 'x=z', 'x=-z'])

def worker(workQueue):
# I.S. : Sistem terinisialisasi dan workQueue terdefinisi
# F.S. : Dikeluarkan prompt dan jika diinput ditambahkan ke workQueue
    global is3D
    global bacaPoint
    while(True):
        workQueue.join()

        if(bacaPoint): #sudah membaca input point
            command = input("$ ") #input command
            listCommand = command.split()
            if (len(listCommand)>0): #validasi input tidak kosong

                if (listCommand[0]=='multiple'): #apakah commandnya multiple
                    if (len(listCommand)==2): #validasi parameter multiple
                        if (isInt(listCommand[1])):
                            multiCommand = []
                            for i in range (1,int(listCommand[1])+1):
                                print('   '+str(i)+'. ',end='')
                                masukan = input()
                                parsed = masukan.split()
                                if (len(parsed)>0):
                                    if(parsed[0]=='multiple'):
                                        masukan='multiple'
                                while (masukan == 'reset' or masukan == 'exit' or masukan=='multiple'): #validasi function dalam multiple
                                    if (len(parsed)>0):
                                        if(parsed[0]=='multiple'):
                                            masukan='multiple'
                                    if (masukan == 'reset' or masukan == 'exit' or masukan=='multiple'):
                                        print('ERROR! Cannot input function '+masukan+' in multiple')
                                    print('   '+str(i)+'. ',end='')
                                    masukan = input()
                                    parsed = masukan.split()
                                multiCommand.append(masukan)
                            for mcom in multiCommand:
                                workQueue.put(mcom,False)
                        else:
                            print('Multiple function take float as argument')
                    else:
                        print('Wrong argument for multiple function')

                elif (listCommand[0]=='add'): #apakah commandnya add
                    if (len(listCommand)==1): #validasi parameter add
                        inputPoint()
                        command = "add"

        else: #belum meminta input point
            inputPoint()
            if (is3D):
                if (len(pointBuffer)==0):
                    command = '3D'
                    bacaPoint = True
                else:
                    command = 'insert'
                    workQueue.put(command,False)
                    command = 'set3Dview'
            else:
                command = "insert"
        workQueue.put(command,False)

def inputPoint():
# I.S. : bacaPoint dan is3D terdefinisi
# F.S. : Dibaca N point dari user lalu ditambahkan ke pointBuffer
    global pointBuffer
    global bacaPoint
    global is3D
    if (not bacaPoint and not is3D):
        masukan = ''
        while (masukan!='2D' and masukan!='3D'):
            masukan = input('2D or 3D: ')
            masukan.replace(' ','')
            if (masukan!='2D' and masukan!='3D'):
                print('Wrong input. Try again!')
        if (masukan=='3D'):
            is3D = True
   
    # jika 3D tidak harus memasukan titik
    if (is3D and not bacaPoint): 
        masukan = ''
        while (masukan!='yes' and masukan!='no'):
            masukan = input('Want to input your own point? (yes/no)\nThe basic shape for 3D is a cube\nChoice: ')
            Temp = masukan.split()
            if(len(Temp)!=1):
                masukan = ''
        if (masukan=='no'):
            pointBuffer=[]
    else: #inputnya 2D
        masukan = 'yes'
    if(masukan =='yes') :
        N = -1 #tipe integer untuk jumlah point, inisiasi dengan -1
        masukan = ''
        while (N<3 or len(Temp)!=1): #validasi input N
            masukan = input("Input N: ") #tipe string untuk validasi
            Temp = masukan.split()
            try:
                N = int(Temp[0])
                if (N<3 and len(Temp)==1):
                    print("N must be bigger than two")
                elif (len(Temp)!=1):
                    print('N can only contain one number')
            except:
                N = -1
                print("The input must be integer")
        arrPoint = [] # tipe menyimpan array of point
        print("Make sure your input is clockwise!")
        print("Use space to separate your input (ex: 10 10)")
        for i in range(1,N+1,1): #iterasi sebanyak N kali
            point = [] # tipe menyimpan tipe data point
            status = False
            if (is3D):
                while (len(point)!=3 or not status): #meminta input titik 3 dimensi yang benar
                    #input benar saat jumlah titiknya 3
                    print('Point('+str(i)+') ',end='')
                    point = input("= ").split() # meminta input
                    status = isAllFloat(point)
                    if (not status):
                        print('The input must be number')
                    elif (len(point)!=3):
                        print('The input has to be in x, y and z')
            else:
                while (len(point)!=2 or not status): #meminta input titik 3 dimensi yang benar
                    #input benar saat jumlah titiknya 3
                    print('Point('+str(i)+') ',end='')
                    point = input("= ").split() # meminta input
                    status = isAllFloat(point)
                    if (not status):
                        print('The input must be number')
                    elif (len(point)!=2):
                        print('The input has to be in x and y')
            if (len(point)==2): #jika inputnya adalah titik 2 dimensi
                point.append(0)
            pointIns = [float(point[0]),float(point[1]),float(point[2])] #casting ke float
            arrPoint.append(pointIns) #menambahkan ke arrPoint
        np.resize(pointBuffer,(N,2)) #mengubah isi listPoint
        pointBuffer= arrPoint 
        bacaPoint = True #sudah meminta input point

def parsingCommand(command,listPoint,percent):
# I.S. : Menerima input command, listPoint yang mau ditransformasi, dan persentase transformasi
# F.S. : Ditaruh ke pointBuffer hasil transformasi jika command valid, return True, jika invalid, return False
    global pointBuffer
    global is3D

    pointBuffer = listPoint
    listCommand = command.split()
    commandValid = False
    if(len(listCommand)>0): #validasi input kosong
        if(np.isin(listCommand[0],validCommand)):
            commandValid = True
            step = float(percent)/100.0
            fungsi = listCommand.pop(0)
            if (fungsi=='translate'):
                if (is3D):
                    if(len(listCommand)==3 and isAllFloat(listCommand)):
                        x = float(listCommand[0]) * step
                        y = float(listCommand[1]) * step
                        z = float(listCommand[2]) * step
                        pointBuffer = transformasi.translasi(listPoint,x,y,z)
                    else:
                        commandValid = False
                        print('Wrong argument for translate function')
                else:
                    if(len(listCommand)==2 and isAllFloat(listCommand)):
                        x = float(listCommand[0]) * step
                        y = float(listCommand[1]) * step
                        z = 0.0 * step
                        pointBuffer = transformasi.translasi(listPoint,x,y,z)
                    else:
                        commandValid = False
                        print('Wrong argument for translate function')
            elif (fungsi=='dilate'):
                if (len(listCommand)==1):
                    if (isFloat(listCommand[0])):
                        k = (float(listCommand[0])-1.0)*step + 1.0
                        pointBuffer = transformasi.dilatasi(listPoint,k)
                    else:
                        commandValid = False
                        print('Dilate function take float as argument')
                else:
                    commandValid = False
                    print('Wrong argument for dilate function')
            elif (fungsi=='rotate'):
                if (is3D):
                    if(len(listCommand)==4 and isAllFloat(listCommand)):
                        deg = float(listCommand[0]) * step
                        x = float(listCommand[1])
                        y = float(listCommand[2])
                        z = float(listCommand[3])
                        if (x!=0.0 or  y!=0.0 or  z!=0.0):
                            pointBuffer = transformasi.rotasi(listPoint,deg,x,y,z,is3D)
                        else:
                            commandValid = False
                            print('Rotation center cannot be vector zero')
                    else:
                        commandValid = False
                        print('Wrong argument for rotate function')
                else:
                    if(len(listCommand)==3 and isAllFloat(listCommand)):
                        deg = float(listCommand[0]) * step
                        x = float(listCommand[1])
                        y = float(listCommand[2])
                        z = 0.0
                        pointBuffer = transformasi.rotasi(listPoint,deg,x,y,z,is3D)
                    else:
                        commandValid = False
                        print('Wrong argument for rotate function')
            elif (fungsi=='reflect'):
                listCommand = ''.join(listCommand)
                if (is3D):
                    if (np.isin(listCommand,param3Dvalid) or isPoint(listCommand)==3):
                        pointBuffer = transformasi.refleksi(listPoint,listCommand,is3D,step)
                    else:
                        commandValid = False
                        print('Wrong parameter for 3D reflect')
                else:
                    if (np.isin(listCommand,param2Dvalid) or isPoint(listCommand)==2):
                        pointBuffer = transformasi.refleksi(listPoint,listCommand,is3D,step)
                    else:
                        commandValid = False
                        print('Wrong parameter for 2D reflect')
            elif (fungsi=='shear'):
                if (len(listCommand)==2):
                    if (isFloat(listCommand[1])):
                        k = (float(listCommand[1]))*step
                        if (is3D):
                            if (listCommand[0]=='x' or listCommand[0]=='y' or listCommand[0]=='z'):
                                pointBuffer = transformasi.shear(listPoint,listCommand[0],k)
                            else:
                                commandValid = False
                                print('Shear function need x, y or z axis as first argument')
                        else:
                            if (listCommand[0]=='x' or listCommand[0]=='y'):
                                pointBuffer = transformasi.shear(listPoint,listCommand[0],k)
                            else:
                                commandValid = False
                                print('Shear function need x or y axis as first argument')
                    else:
                        commandValid = False
                        print('Shear function take float as second argument')
                else:
                    commandValid = False
                    print('Wrong argument for shear function')
            elif (fungsi=='stretch'):
                if (len(listCommand)==2):
                    if (isFloat(listCommand[1])):
                        k = (float(listCommand[1])-1.0)*step + 1.0
                        if (is3D):
                            if (listCommand[0]=='x' or listCommand[0]=='y' or listCommand[0]=='z'):
                                pointBuffer = transformasi.stretch(listPoint,listCommand[0],k)
                            else:
                                commandValid = False
                                print('Stretch function need x, y or z axis as first argument')
                        else:
                            if (listCommand[0]=='x' or listCommand[0]=='y'):
                                pointBuffer = transformasi.stretch(listPoint,listCommand[0],k)
                            else:
                                commandValid = False
                                print('Stretch function need x or y axis as first argument')
                    else:
                        commandValid = False
                        print('Stretch function take float as second argument')
                else:
                    commandValid = False
                    print('Wrong argument for stretch function')
            elif (fungsi=='custom'):
                arrCustom = []
                if (is3D):
                    if(len(listCommand)==9 and isAllFloat(listCommand)):
                        #custom 3D
                        arrCustom.append(float(listCommand[0])*step)
                        arrCustom.append(float(listCommand[1])*step)
                        arrCustom.append(float(listCommand[2])*step)
                        arrCustom.append(float(listCommand[3])*step)
                        arrCustom.append(float(listCommand[4])*step)
                        arrCustom.append(float(listCommand[5])*step)
                        arrCustom.append(float(listCommand[6])*step)
                        arrCustom.append(float(listCommand[7])*step)
                        arrCustom.append(float(listCommand[8])*step)
                        pointBuffer = transformasi.custom(listPoint,arrCustom)
                    else:
                        commandValid = False
                        print('Wrong argument for custom function')
                else:
                    if(len(listCommand)==4 and isAllFloat(listCommand)):
                        #custom 2D
                        arrCustom.append(float(listCommand[0])*step)
                        arrCustom.append(float(listCommand[1])*step)
                        arrCustom.append(float(listCommand[2])*step)
                        arrCustom.append(float(listCommand[3])*step)
                        pointBuffer = transformasi.custom(listPoint,arrCustom)
                    else:
                        commandValid = False
                        print('Wrong argument for custom function')
            elif(fungsi =='help'):
                if (len(listCommand)==0):
                    printHelp()
                elif (len(listCommand)==1):
                    if(listCommand[0]=='translate'):
                        printHelpTranslate()
                    elif(listCommand[0]=='dilate'):
                        printHelpDilate()
                    elif(listCommand[0]=='rotate'):
                        printHelpRotate()
                    elif(listCommand[0]=='reflect'):
                        printHelpReflect()
                    elif(listCommand[0]=='shear'):
                        printHelpShear()
                    elif(listCommand[0]=='stretch'):
                        printHelpStretch()
                    elif(listCommand[0]=='custom'):
                        printHelpCustom()
                    elif(listCommand[0]=='multiple'):
                        printHelpMultiple()
                    elif(listCommand[0]=='reset'):
                        print('reset -- reset object(s) to its original form')
                    elif(listCommand[0]=='exit'):
                        print('exit -- to exit from the program')
                    else:
                        print("Undefined command: '"+str(listCommand[0])+"'.  Try 'help'")
                else:
                    print('Wrong way to call help')
                commandValid= False
        else:
            if (np.isin(listCommand[0],mainCommand)):
                print("'"+str(listCommand[0])+"' function doesn't have any parameter" )
            else:
                print("There is no function called '"+str(listCommand[0])+"'. Try 'help'")
    return commandValid
    

def isInt(param):
# Mengembalikan true jika param integer
    try:
        x = int(param)
        return True
    except:
        return False

def isFloat(param):
# Mengembalikan true jika param float
    try:
        x = float(param)
        return True
    except:
        return False

def isAllFloat(param):
# Mengembalikan true jika semua param float
    i = 0
    Float = True
    while (i<len(param) and Float):
        if(not(isFloat(param[i]))):
            Float = False
        else:
            i += 1
    return Float

def isPoint(param):
# Mengembalikan true jika param adalah tipe point
    try:
        if (param[0]=='(' and param[len(param)-1]==')'):
            param = param.replace(',',' ')
            param = param.replace('(','')
            param = param.replace(')','')
            param = param.split()
            if (isAllFloat(param)):
                return len(param)
        else:
            return 0
    except:
        return 0

def printHelp():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help general
    print('List of available function\n')
    print('translate -- to translate object(s) by moving all its point')
    print('dilate    -- to dilate object(s) by a factor')
    print('rotate    -- to rotate object(s) counter-clockwise')
    print('reflect   -- to reflect object(s) to a surface or point')
    print('shear     -- shear object(s) to one of the axis')
    print('stretch   -- stretch object(s) to one of the axis')
    print('custom    -- apply a linear transformation to object(s) with custom matrix')
    print('multiple  -- apply functions to object(s) several times')
    print('reset     -- reset object(s) to its original form')
    print('exit      -- to exit from the program\n')
    print('Type "help" followed by function name for full documentation')

def printHelpTranslate():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help translate
    print('for 2D: translate <dx> <dy>')
    print('<dx> and <dy> is a parameter for translate function in 2D')
    print('value x will be translated by <dx> and value y by <dy>\n')
    print('for 3D: translate <dx> <dy> <dz>')
    print('for 3D object(s), added one more parameter to translate z by <dz>')
    print('<dx> <dy> <dz> is a floating number')

def printHelpDilate():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help dilatasi
    print('dilate <k>')
    print('dilate the object(s) by <k> factor in all its axis')
    print('<k> is a floating number')

def printHelpRotate():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help rotasi
    print('for 2D: rotate <deg> <a> <b>')
    print('<a> and <b> is the center of rotation in 2D')
    print('object(s) will be rotate by <deg> degree counter-clockwise with <a>,<b> as its center\n')
    print('for 3D: rotate <deg> <u> <v> <w>')
    print('for object(s) in 3D, the object(s) will be rotated <deg> degree counter-clockwise')
    print('with vector(<u>,<v>,<w>) as its center, it cannot be a zero vector')
    print('<deg> <a> <b> <u> <v> <w> is a floating number')

def printHelpReflect():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help refleksi
    print('reflect <param>')
    print('the value <param> for 2D can be one of these expresion:')
    print('x, y, y=x, y=-x or (a,b) with a,b is a point in 2D plane')
    print('as for the 3D, the value <param> can be one of these expresion:')
    print('x, y, z, xy, xz, yz, y=x, y=-x, y=z, y=-z, x=z, x=-z or (a,b,c) with a,b,c is a point in 3D plane')
    print('it will reflect the object(s) with <param> as its mirror')

def printHelpShear():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help shear
    print('shear <param> <k>')
    print("for 2D, <param> can be either 'x' or 'y'")
    print("in 3D, <param> value is the same as in 2D but added 'z' value as it's third axis")
    print('it will shear the object(s) in <param> direction by <k> factor')
    print('<k> is a floating number')

def printHelpStretch():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help stretch
    print('stretch <param> <k>')
    print("for 2D, <param> can be either 'x' or 'y'")
    print("in 3D, <param> value is the same as in 2D but added 'z' value as it's third axis")
    print('it will stretch the object(s) in <param> direction by <k> factor')
    print('<k> is a floating number')

def printHelpCustom():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help custom
    print('for 2D: custom <a> <b> <c> <d>')
    print('for 3D: custom <a> <b> <c> <d> <e> <f> <g> <h> <i>')
    print('apply a linear transformation to object(s) with custom matrix as below')
    print('2D: | a b |    3D: | a b c |')
    print('    | c d |        | d e f |')
    print('                   | g h i |')
    print('<a> <b> <c> <d> <e> <f> <g> <h> <i> is a floating number')

def printHelpMultiple():
# I.S. : Sistem terinisialisasi
# F.S. : Tercetak ke console help multiple
    print('multiple <n>')
    print('apply functions to object(s) <n> times')
    print('the input function can be any function listed except')
    print("'multiple','reset','exit'")
    print('<n> is a integer')