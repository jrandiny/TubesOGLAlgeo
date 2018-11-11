import numpy as np
import transformasi
import math

import time

bacaPoint = False
pointBuffer = np.zeros((1,2))
is3D = False

validCommand = np.array(['translate','rotate','dilate','shear','stretch','custom','reflect','multiple'])

def worker(workQueue):
    global is3D
    global bacaPoint
    while(True):
        time.sleep(0.1) # Agar tidak lemot saat queue not empty
        if(workQueue.empty()):
            if(bacaPoint): #sudah membaca input point
                command = input("$ ") #input command
                listCommand = command.split()
                if (len(listCommand)>0): #validasi input tidak kosong

                    if (listCommand[0]=='multiple'): #apakah commandnya multiple
                        if (len(listCommand)==2): #validasi parameter multiple
                            if (isInt(listCommand[1])):
                                multiCommand = []
                                for i in range (1,int(listCommand[1])+1):
                                    multiCommand.append(input("   "))
                                for mcom in multiCommand:
                                    workQueue.put(mcom,False)

                    elif (listCommand[0]=='add'): #apakah commandnya add
                        if (len(listCommand)==1): #validasi parameter add
                            inputPoint()
                            command = "add"

            else: #belum meminta input point
                inputPoint()
                if (is3D):
                    command = '3D'
                    bacaPoint = True
                else:
                    command = "insert"
            workQueue.put(command,False)

def inputPoint():
    global pointBuffer
    global bacaPoint
    global is3D
    if (not bacaPoint and not is3D):
        masukan = ''
        while (masukan!='2D' and masukan!='3D'):
            masukan = input('2D atau 3D: ')
            masukan.replace(' ','')
            if (masukan!='2D' and masukan!='3D'):
                print('Input salah, mohon ulangi!')
        if (masukan=='3D'):
            is3D = True
   
    # jika 3D tidak harus memasukan titik
    if (is3D and not bacaPoint): 
        masukan = ''
        while (masukan!='y' and masukan!='n'):
            masukan = input('Input titik? (y,n): ')
            Temp = masukan.split()
            if(len(Temp)!=1):
                masukan = ''
    else: #inoutnya 2D
        masukan = 'y'
    if(masukan =='y') :
        N = -1 #tipe integer untuk jumlah point, inisiasi dengan -1
        masukan = ''
        while (N<3 or len(Temp)!=1): #validasi input N
            masukan = input("Input N: ") #tipe string untuk validasi
            Temp = masukan.split()
            try:
                N = int(Temp[0])
                if (N<3 and len(Temp)==1):
                    print("N harus > 2")
                elif (len(Temp)!=1):
                    print('Input hanya boleh satu angka')
            except:
                N = -1
                print("Input bukan integer")
        arrPoint = [] # tipe menyimpan array of point
        print("Pastikan input titik sudah clockwise!")
        for i in range(1,N+1,1): #iterasi sebanyak N kali
            point = [] # tipe menyimpan tipe data point
            status = False
            if (is3D):
                while (len(point)!=3 or not status): #meminta input titik 3 dimensi yang benar
                    #input benar saat jumlah titiknya 3
                    print('Titik('+str(i)+') ',end='')
                    point = input("= ").split() # meminta input
                    status = isAllInt(point)
                    if (not status):
                        print('Input harus integer')
                    elif (len(point)!=3):
                        print('Input harus tiga koordinat, x,y,dan z')
            else:
                while (len(point)!=2 or not status): #meminta input titik 3 dimensi yang benar
                    #input benar saat jumlah titiknya 3
                    print('Titik('+str(i)+') ',end='')
                    point = input("= ").split() # meminta input
                    status = isAllInt(point)
                    if (not status):
                        print('Input harus integer')
                    elif (len(point)!=2):
                        print('Input harus dua koordinat, x dan y')
            if (len(point)==2): #jika inputnya adalah titik 2 dimensi
                point.append(0)
            pointIns = [float(point[0]),float(point[1]),float(point[2])] #casting ke float
            arrPoint.append(pointIns) #menambahkan ke arrPoint
        np.resize(pointBuffer,(N,2)) #mengubah isi listPoint
        pointBuffer= arrPoint 
        bacaPoint = True #sudah meminta input point

def parsingCommand(command,listPoint,percent):
    global pointBuffer
    global is3D

    pointBuffer = listPoint
    listCommand = command.split()
    commandValid = False
    if(np.isin(listCommand[0],validCommand)):
        commandValid = True
        step = float(percent)/100.0
        # if (len(listCommand)==4):
        if (listCommand[0]=='translate'):
            if (len(listCommand)-1 ==2):
                listCommand.append(0)
            if (len(listCommand)==4):
                x = float(listCommand[1])
                y = float(listCommand[2])
                z = float(listCommand[3])
                pointBuffer = transformasi.translasi(listPoint,x/step,y/step,z/step)
        elif (listCommand[0]=='dilate'):
            if (len(listCommand)==2):
                k = float(listCommand[2])
                kAnim = (k-1.0)/step
                kAnim += 1.0
                pointBuffer = transformasi.dilatasi(listPoint,kAnim)
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
                k = float(listCommand[2])
                kAnim = (k-1.0)/step
                kAnim += 1.0
                pointBuffer = transformasi.shear(listPoint,listCommand[1],kAnim)
        elif (listCommand[0]=='stretch'):
            if (len(listCommand)==3 and (listCommand[1]=='x' or listCommand[1]=='y' or listCommand[1]=='z')):
                k = float(listCommand[2])
                kAnim = (k-1.0)/step
                kAnim += 1.0
                pointBuffer = transformasi.stretch(listPoint,listCommand[1],kAnim)
        elif (listCommand[0]=='custom'):
            arrCustom = []
            if (len(listCommand)-1 == 4):
                #custom 2D
                arrCustom.append(float(listCommand[1])/step)
                arrCustom.append(float(listCommand[2])/step)
                arrCustom.append(float(listCommand[3])/step)
                arrCustom.append(float(listCommand[4])/step)
            elif(len(listCommand)-1 == 9):
                #custom 3D
                arrCustom.append(float(listCommand[1])/step)
                arrCustom.append(float(listCommand[2])/step)
                arrCustom.append(float(listCommand[3])/step)
                arrCustom.append(float(listCommand[4])/step)
                arrCustom.append(float(listCommand[5])/step)
                arrCustom.append(float(listCommand[6])/step)
                arrCustom.append(float(listCommand[7])/step)
                arrCustom.append(float(listCommand[8])/step)
                arrCustom.append(float(listCommand[9])/step)
            if (len(arrCustom)==9):
                pointBuffer = transformasi.custom(listPoint,arrCustom)
    else:
        print('There is no \''+str(command)+'\' function')
    return commandValid
    

def isInt(param):
    try:
        x = int(param)
        return True
    except:
        return False

def isAllInt(param):
    i = 0
    Int = True
    while (i<len(param) and Int):
        if(not(isInt(param[i]))):
            Int = False
        else:
            i += 1
    return Int