# Lib OpenGL
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("Tidak ada library opengl :(")

import random
import numpy as np

from queue import Queue
import threading

import sys
sys.path.append('../src')
import render
import termInput

taskQueue = Queue()
pointQueue = Queue()

step = 100
scaleNow = 101
saveComm = ""
savePoints =[]

basicShape = []
listPoints =[np.array([[-50,-50,0],[50,-50,0],[50,50,0],[-50,50,0]])]

def getCube():
    return [
                # depan belakang
                np.array([[50,50,50],[50,-50,50],[-50,-50,50],[-50,50,50]]),
                np.array([[50,50,-50],[50,-50,-50],[-50,-50,-50],[-50,50,-50]]),
                # atas bawah
                np.array([[50,50,50],[-50,50,50],[-50,50,-50],[50,50,-50]]),
                np.array([[50,-50,50],[-50,-50,50],[-50,-50,-50],[50,-50,-50]]),
                # kiri kanan
                np.array([[50,50,-50],[50,-50,-50],[50,-50,50],[50,50,50]]),
                np.array([[-50,50,-50],[-50,-50,-50],[-50,-50,50],[-50,50,50]])
                ]


def keyboardFunc(key,x,y):
    if key==b'Q':
        glutLeaveMainLoop()
    else:
        if(key==b'q'):
            render.translate[2] += -5.0
        elif(key==b'e'):
            render.translate[2] += 5.0
        elif(key==b'a'):
            render.translate[0] += 2.5
        elif(key==b'd'):
            render.translate[0] += -2.5
        elif(key==b'w'):
            render.translate[1] += -2.5
        elif(key==b's'):
            render.translate[1] += 2.5
        
        if(render.is3D):
            if(key == b'i'):
                render.rotate[0] += 1.0
            elif(key==b'k'):
                render.rotate[0] += -1.0
            elif(key==b'l'):
                render.rotate[1] += -1.0
            elif(key==b'j'):
                render.rotate[1] += 1.0
            elif(key==b'u'):
                render.rotate[2] += 1.0
            elif(key==b'o'):
                render.rotate[2] += -1.0

        glutPostRedisplay()

def doInput():
    global listPoints
    global basicShape
    global scaleNow
    global saveComm
    global savePoints

    waitTask = False

    if not taskQueue.empty() and scaleNow>100:
        command = taskQueue.get()
        if (command=='exit'):
            glutLeaveMainLoop() #exit
        elif (command=='insert'):
            basicShape[0] = termInput.pointBuffer
            listPoints[0] = termInput.pointBuffer
            glutPostRedisplay()
        elif (command=='add'):
            basicShape.append(termInput.pointBuffer)
            listPoints.append(termInput.pointBuffer)
            glutPostRedisplay()
        elif (command=='reset'):
            listPoints = basicShape
            glutPostRedisplay()
        elif (command=='set3Dview'):
            render.is3D = True
        elif (command=='3D'):
            render.is3D = True
            termInput.is3D = True
            basicShape = getCube()
            listPoints = getCube()
            glutPostRedisplay()
        else:
            if(termInput.parsingCommand(command,np.array([[0,0,0]]),1)):
                scaleNow = 1
                savePoints = listPoints.copy()
                saveComm = command
                waitTask = True
        
        if(not waitTask):
            taskQueue.task_done()     
       
    else:
        if (scaleNow<=step):
            for i,poly in enumerate(savePoints):
                termInput.parsingCommand(saveComm,poly,scaleNow)
                listPoints[i] = termInput.pointBuffer
            # print(listPoints)
            glutPostRedisplay()
            scaleNow +=1
            if(scaleNow==step+1):
                taskQueue.task_done()
        


def prepareDisplay():
    global listPoints
    render.listPoints = listPoints
    render.displayFunc()

if __name__ =="__main__":
    # Threading input system
    inputThread = threading.Thread(target=termInput.worker,args=(taskQueue,))

    #setup OGL window
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_DEPTH)
    glutInitWindowSize(1000, 1000)
    glutCreateWindow("ini layar loh wkwkwkwk!!!")

    glEnable(GL_DEPTH_TEST)

    inputThread.start()

    # GLUT callbacks
    glutReshapeFunc(render.windowResized)
    glutDisplayFunc(prepareDisplay)
    glutKeyboardFunc(keyboardFunc)
    glutIdleFunc(doInput)

    glutMainLoop()