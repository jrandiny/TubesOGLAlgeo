import numpy as np
import math

def parserLocate(x):
    i=0
    idxkb=idxkoma1=idxkoma2=idxkt=-1
    jumlah=0
    while(i<len(x)):
        if(x[i]=='('):
            idxkb=i
        elif(x[i]==')'):
            idxkt=i
        elif(x[i]==',' and jumlah == 0):
            idxkoma1=i
            jumlah+=1
        elif(x[i]==',' and jumlah == 1):
            idxkoma2=i
        i+=1
    result=[idxkb]
    result.append(idxkoma1)
    result.append(idxkoma2)
    result.append(idxkt)
    return result

def toNumber(x):
    a=b=c=0
    result=parserLocate(x)
    idxkb=result[0]
    idxkoma1=result[1]
    idxkoma2=result[2]
    idxkt=result[3]
    a=int(x[idxkb+1:idxkoma1])
    if(idxkoma2==-1):
        b=int(x[idxkoma1+1:idxkt])
    else:
        b=int(x[idxkoma1+1:idxkoma2])
        c=int(x[idxkoma2+1:idxkt])
    result=[a]
    result.append(b)
    result.append(c)
    return result

def toRadian(x):
    return x*math.pi/180

def translasi(points,dx,dy,dz):
    penambah=np.array([dx,dy,dz])
    pengali=np.identity(3)
    return transformasi(points,pengali,penambah)


def rotasi(points,degree,a,b,c,is3D):
    sudut=toRadian(degree)
    if not is3D:
        penambah=np.array([-1*a,-1*b,0])
        pengali=np.array([[math.cos(sudut),-1*math.sin(sudut),0]])
        pengali=np.append(pengali,[[math.sin(sudut),math.cos(sudut),0]],axis=0)
        pengali=np.append(pengali,[[0,0,0]],axis=0)
        hasil=transformasi(points,pengali,penambah)
        hasil=translasi(hasil,a,b,0)
        return hasil
    else:
        penambah=np.zeros(3)
        length=math.sqrt(math.pow(a,2)+math.pow(b,2)+math.pow(c,2))
        a/=length
        b/=length
        c/=length
        pengali=np.array([[math.pow(a,2)*(1-math.cos(sudut))+math.cos(sudut),a*b*(1-math.cos(sudut))-c*math.sin(sudut),a*c*(1-math.cos(sudut))+b*math.sin(sudut)]])
        pengali=np.append(pengali,[[a*b*(1-math.cos(sudut))+c*math.sin(sudut),math.pow(b,2)*(1-math.cos(sudut))+math.cos(sudut),b*c*(1-math.cos(sudut))-a*math.sin(sudut)]],axis=0)
        pengali=np.append(pengali,[[a*c*(1-math.cos(sudut))-b*math.sin(sudut),b*c*(1-math.cos(sudut))+a*math.sin(sudut),math.pow(c,2)*(1-math.cos(sudut))+math.cos(sudut)]],axis=0)
        return transformasi(points,pengali,penambah)
        
def dilatasi(points,k):
    penambah=np.zeros(3)
    pengali=np.array([[k,0,0]])
    pengali=np.append(pengali,[[0,k,0]],axis=0)
    pengali=np.append(pengali,[[0,0,k]],axis=0)
    return transformasi(points,pengali,penambah)
        

def refleksi(points,param,is3D,step):
    penambah=np.zeros(3)    
    k = -2.0*step + 1.0
    if (is3D):
        if (param=="xz"):
            return stretch(points,'y',k)
        elif (param=="yz"):
            return stretch(points,'x',k)
        elif (param=="xy"):
            return stretch(points,'z',k)
        elif (param=="x"):
            points=stretch(points,'z',k)
            return stretch(points,'y',k)
        elif (param=="y"):
            points=stretch(points,'z',k)
            return stretch(points,'x',k)
        elif (param=="z"):
            points=stretch(points,'x',k)
            return stretch(points,'y',k)
        elif (param=="y=x"):
            points=rotasi(points,45,0,0,1,True)
            points=refleksi(points,'y',True,step)
            return rotasi(points,-45,0,0,1,True)
        elif (param=="y=-x"):
            points=rotasi(points,-45,0,0,1,True)
            points=refleksi(points,'y',True,step)
            return rotasi(points,45,0,0,1,True)
        elif (param=="y=z"):
            points=rotasi(points,-45,1,0,0,True)
            points=refleksi(points,'y',True,step)
            return rotasi(points,45,1,0,0,True)
        elif (param=="y=-z"):
            points=rotasi(points,45,1,0,0,True)
            points=refleksi(points,'y',True,step)
            return rotasi(points,-45,1,0,0,True)
        elif (param=="x=z"):
            points=rotasi(points,45,0,1,0,True)
            points=refleksi(points,'x',True,step)
            return rotasi(points,-45,0,1,0,True)
        elif (param=="x=-z"):
            points=rotasi(points,-45,0,1,0,True)
            points=refleksi(points,'x',True,step)
            return rotasi(points,45,0,1,0,True)
        else:
            result=toNumber(param)
            a=result[0]
            b=result[1]
            c=result[2]
            points=translasi(points,-1*a,-1*b,-1*c)
            points=dilatasi(points,k)
            return translasi(points,a,b,c)
    else:
        if (param=="x"):
            return stretch(points,'y',k)
        elif (param=="y"):
            return stretch(points,'x',k)
        elif (param=="y=x"):
            points=rotasi(points,45,0,0,0,False)
            points=stretch(points,'x',k)
            return rotasi(points,-45,0,0,0,False)
        elif (param=="y=-x"):
            points=rotasi(points,-45,0,0,0,False)
            points=stretch(points,'x',k)
            return rotasi(points,45,0,0,0,False)
        else:
            result=toNumber(param)
            a=result[0]
            b=result[1]
            c=result[2]
            points=translasi(points,-1*a,-1*b,-1*c)
            points=dilatasi(points,k)
            return translasi(points,a,b,c)
            
def shear(points,sb,param):
    penambah=np.zeros(3)
    if(sb=="x"):
        pengali=np.array([[1,param,0]])
        pengali=np.append(pengali,[[0,1,0]],axis=0)
        pengali=np.append(pengali,[[0,0,1]],axis=0)
    elif(sb=="y"):
        pengali=np.array([[1,0,0]])
        pengali=np.append(pengali,[[param,1,0]],axis=0)
        pengali=np.append(pengali,[[0,0,1]],axis=0)
    elif(sb=='z'):
        pengali=np.array([[1,0,0]])
        pengali=np.append(pengali,[[0,1,0]],axis=0)
        pengali=np.append(pengali,[[0,param,1]],axis=0)
    return transformasi(points,pengali,penambah)

def stretch(points,sb,param):
    penambah=np.zeros(3)
    if(sb=="x"):
        pengali=np.array([[param,0,0]])
        pengali=np.append(pengali,[[0,1,0]],axis=0)
        pengali=np.append(pengali,[[0,0,1]],axis=0)
    elif(sb=="y"):
        pengali=np.array([[1,0,0]])
        pengali=np.append(pengali,[[0,param,0]],axis=0)  
        pengali=np.append(pengali,[[0,0,1]],axis=0)
    elif(sb=="z"):
        pengali=np.array([[1,0,0]])
        pengali=np.append(pengali,[[0,1,0]],axis=0)  
        pengali=np.append(pengali,[[0,0,param]],axis=0)
    return transformasi(points,pengali,penambah)

def custom(points,array):
    length=len(array)
    penambah=np.zeros(3)
    pengali=np.empty((0,3))
    if length==4:
        pengali=np.append(pengali,[[array[0],array[1],0]],axis=0)
        pengali=np.append(pengali,[[array[2],array[3],0]],axis=0)
        pengali=np.append(pengali,[[0,0,1]],axis=0)
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
