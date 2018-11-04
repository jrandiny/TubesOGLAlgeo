import numpy as np
import math

def toRadian(x):
    return x*math.pi/180

def translasi(points,dx,dy,dz):
    penambah=np.array([dx,dy,dz])
    pengali=np.identity(3)
    return transformasi(points,pengali,penambah)


def rotasi(points,degree,a,b,c):
    penambah=np.array([-1*a,-1*b])
    pengali=np.array([[math.cos(toRadian(degree)),-1*math.sin(toRadian(degree))]])
    pengali=np.append(pengali,[[math.sin(toRadian(degree)),math.cos(toRadian(degree))]],axis=0)
    hasil=transformasi(points,pengali,penambah)
    hasil=translasi(hasil,-a,-b)
    return hasil

def refleksi(points,param):
    penambah=np.zeros((1,2))    
    if (param=="x"):
        pengali=np.array([[1,0]])
        pengali=np.append(pengali,[[0,-1]],axis=0)
    elif (param=="y"):
        pengali=np.array([[-1,0]])
        pengali=np.append(pengali,[[0,1]],axis=0)
    elif (param=="y=x"):
        pengali=np.array([[0,1]])
        pengali=np.append(pengali,[[1,0]],axis=0)
    elif (param=="y=-x"):
        pengali=np.array([[0,-1]])
        pengali=np.append(pengali,[[-1,0]],axis=0)
    else:
        return rotasi(points,180,param[0],param[1])        
    return transformasi(points,pengali,penambah)

def shear(points,param,sb):
    penambah=np.zeros((1,2))
    if(sb=="x"):
        pengali=np.array([[1,param]])
        pengali=np.append(pengali,[[0,1]],axis=0)
    elif(sb=="y"):
        pengali=np.array([[1,0]])
        pengali=np.append(pengali,[[param,1]],axis=0)
    return transformasi(points,pengali,penambah)

def stretch(points,param,sb):
    penambah=np.zeros((1,2))
    pengali=[]
    if(sb=="x"):
        pengali=np.array([[1,0]])
        pengali=np.append(pengali,[[0,param]],axis=0)
    elif(sb=="y"):
        pengali=np.array([[param,0]])
        pengali=np.append(pengali,[[0,1]],axis=0)  
    return transformasi(points,pengali,penambah)

def custom(points,array):
    length=len(array)
    penambah=np.zeros(3)
    pengali=np.empty((0,3))
    if length==4:
        pengali=np.append(pengali,[[array[0],array[1],0]],axis=0)
        pengali=np.append(pengali,[[array[2],array[3],0]],axis=0)
        pengali=np.append(pengali,[[0,0,0]],axis=0)
    elif length==9:
        pengali=np.append(pengali,[[array[0],array[1],array[2]]],axis=0)
        pengali=np.append(pengali,[[array[3],array[4],array[5]]],axis=0)
        pengali=np.append(pengali,[[array[6],array[7],array[8]]],axis=0)
    return transformasi(points,pengali,penambah)


def transformasi(points, pengali, penambah):
    temp=np.empty((0,3))
    for point in points:
        temp=np.append(temp,[pengali.dot(np.add(point,penambah))],axis=0)
    return temp



#point -> array([[x1,y1],[x2,y2],[x3,y3]])
