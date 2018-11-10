import numpy as np
import transformasi
import math

import time

bacaPoint = False
pointBuffer = np.zeros((1,2))
is3D = False

def worker(workQueue):
    global is3D
    while(True):
        time.sleep(0.1)
        if(workQueue.empty()):
            if(bacaPoint): #sudah membaca input point
                command = input("$ ") #input command
                listCommand = command.split(' ')
                if (listCommand[0]=='multiple'):
                    if (len(listCommand)==2): #validasi input multiple
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                        multiCommand = []
                        for i in range (1,int(listCommand[1])+1):
                            multiCommand.append(input("   "))
                        
                        for mcom in multiCommand:
                            workQueue.put(mcom,False)

=======
=======
>>>>>>> Stashed changes
                        if (isInt(listCommand[1])):
                            for i in range (1,int(listCommand[1])+1):
                                multiCommand = input("   ")
                                workQueue.put(multiCommand,False)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
                elif (listCommand[0]=='add'):
                    if (len(listCommand)==1): #validasi input add
                        inputPoint()
                        command = "add"
            else: #belum meminta input point
                inputPoint()
                command = "insert"
            workQueue.put(command,False)
            if (is3D):
                command = 'set3Dview'
                workQueue.put(command,False)

def inputPoint():
    global pointBuffer
    global bacaPoint
    global is3D
    N = -1 #tipe integer untuk jumlah point, inisiasi dengan -1
    masukan = []
    while (N<3 or len(masukan)!=1):
        Temp = input("Input N: ") #tipe string untuk validasi
        masukan = Temp.split(' ')
        try:
            N = int(masukan[0])
        except:
            print('inputnya integer')
        if (len(masukan)!=1):
            print('inputya 1 angka')
        else:
            if (N<3):
                print('inputnya minimal 3 titik')
    arrPoint = [] # tipe menyimpan array of point
    print("Pastikan input titik sudah clockwise!")
    for i in range(1,N+1,1): #iterasi sebanyak N kali
        point = [] # tipe menyimpan tipe data point
        while ((len(point)<2 or len(point)>3)): #meminta input yang benar
            #input benar saat jumlah titiknya 2 atau 3
            print('titik('+str(i)+') ',end='')
            point = input("= ").split(' ') # meminta input
        if (len(point)==2): #jika inputnya adalah titik 2 dimensi
            point.append(0)
        elif (len(point)==3):
            is3D = True
        pointIns = [float(point[0]),float(point[1]),float(point[2])] #casting ke float
        arrPoint.append(pointIns) #menambahkan ke arrPoint
    np.resize(pointBuffer,(N,2)) #mengubah isi listPoint
    pointBuffer= arrPoint 
    bacaPoint = True #sudah meminta input point

def parsingCommand(command,listPoint,step):
    global pointBuffer
    global is3D
    pointBuffer = listPoint
    listCommand = command.split(' ')
    if (listCommand[0]=="translate"):
        if (len(listCommand)-1 ==2):
            listCommand.append(0)
        if (len(listCommand)==4):
            x = float(listCommand[1])
            y = float(listCommand[2])
            z = float(listCommand[3])
            pointBuffer = transformasi.translasi(listPoint,x/step,y/step,z/step)
    elif (listCommand[0]=='dilate'):
        if (len(listCommand)==2):
            pointBuffer = transformasi.dilatasi(listPoint,float(listCommand[1]))
    elif (listCommand[0]=='rotate'):
        if (len(listCommand)-1 ==3):
            listCommand.append(0)
        if (len(listCommand)==5):
            x = float(listCommand[2])
            y = float(listCommand[3])
            z = float(listCommand[4])
            pointBuffer = transformasi.rotasi(listPoint,float(listCommand[1])/step,x,y,z,is3D)
    elif (listCommand[0]=='reflect'):
        if (len(listCommand)==2):
            pointBuffer = transformasi.refleksi(listPoint,listCommand[1])
    elif (listCommand[0]=='shear'):
        if (len(listCommand)==3 and (listCommand[1]=='x' or listCommand[1]=='y' or listCommand[1]=='z')):
            pointBuffer = transformasi.shear(listPoint,listCommand[1],float(listCommand[2]))
    elif (listCommand[0]=='stretch'):
        if (len(listCommand)==3 and (listCommand[1]=='x' or listCommand[1]=='y' or listCommand[1]=='z')):
            pointBuffer = transformasi.stretch(listPoint,listCommand[1],float(listCommand[2]))
    elif (listCommand[0]=='custom'):
        arrCustom = []
        if (len(listCommand)-1 == 4):
            #custom 2D
            arrCustom.append(float(listCommand[1]))
            arrCustom.append(float(listCommand[2]))
            arrCustom.append(float(listCommand[3]))
            arrCustom.append(float(listCommand[4]))
        elif(len(listCommand)-1 == 9):
            #custom 3D
            arrCustom.append(float(listCommand[1]))
            arrCustom.append(float(listCommand[2]))
            arrCustom.append(float(listCommand[3]))
            arrCustom.append(float(listCommand[4]))
            arrCustom.append(float(listCommand[5]))
            arrCustom.append(float(listCommand[6]))
            arrCustom.append(float(listCommand[7]))
            arrCustom.append(float(listCommand[8]))
            arrCustom.append(float(listCommand[9]))
        if (len(arrCustom)==9):
            pointBuffer = transformasi.custom(listPoint,arrCustom)

def isInt(param):
    try:
        x = int(param)
        return true
    except:
        return false

def isAllInt(param):
    i = 0
    Int = True
    while (i<len(param) and Int):
        if(not(isInt(param[i]))):
            Int = False
        else:
            i += 1
    return Int

def jarak0(x,y,z):
    return math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))