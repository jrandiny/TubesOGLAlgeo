import numpy as np
import transformasi

bacaPoint = False
pointBuffer = np.zeros((1,2))
is3D = False

def worker(workQueue):
    global is3D
    while(True):
        if(workQueue.empty()):
            if(bacaPoint): #sudah membaca input point
                command = input("$ ") #input command
                listCommand = command.split(' ')
                if (listCommand[0]=='multiple'):
                    for i in range (1,listCommand[1]+1):
                        multiCommand = input("   ")
                        workQueue.put(multiCommand,False)
            else: #belum meminta input point
                inputPoint()
                command = "insert"
            workQueue.put(command,False)
            if (is3D):
                is3D = False
                command = '3D'
                workQueue.put(command,False)

def inputPoint():
    global pointBuffer
    global bacaPoint
    global is3D
    N = int(input("Input N: ")) #tipe integer untuk jumlah point
    arrPoint = [] # tipe menyimpan array of point
    print("Pastikan input titik sudah clockwise!")
    for i in range(1,N+1,1): #iterasi sebanyak N kali
        point = [] # tipe menyimpan tipe data point
        while (len(point)<2 or len(point)>3): #meminta input yang benar
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

def parsingCommand(command,listPoint):
    global pointBuffer
    listCommand = command.split(' ')
    if (listCommand[0]=="translate"):
        if (len(listCommand)-1 ==2):
            listCommand.append(0)
        pointBuffer = transformasi.translasi(listPoint,float(listCommand[1]),float(listCommand[2]),float(listCommand[3]))
    elif (listCommand[0]=='dilate'):
        print("dilatasi")
    elif (listCommand[0]=='rotate'):
        # pass
        if (len(listCommand)-1 ==3):
            listCommand.append(0)
            is3D=False
        else:
            is3D=True
        pointBuffer = transformasi.rotasi(listPoint,float(listCommand[1]),float(listCommand[2]),float(listCommand[3]),float(listCommand[4]),is3D)
    elif (listCommand[0]=='reflect'):
        # pass
        pointBuffer = transformasi.refleksi(listPoint,float(listCommand[1]))
    elif (listCommand[0]=='shear'):
        # pass
        pointBuffer = transformasi.shear(listPoint,float(listCommand[2]),float(listCommand[1]))
    elif (listCommand[0]=='stretch'):
        # pass
        pointBuffer = transformasi.stretch(listPoint,float(listCommand[2]),float(listCommand[1]))
    elif (listCommand[0]=='custom'):
        arrCustom = []
        if (len(listCommand)-1 == 4):
            #custom 2D
            arrCustom.append(float(listCommand[1]))
            arrCustom.append(float(listCommand[2]))
            arrCustom.append(float(listCommand[3]))
            arrCustom.append(float(listCommand[4]))
        else:
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
        pointBuffer = transformasi.custom(listPoint,arrCustom)