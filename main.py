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

import render
import termInput

taskQueue = Queue()
pointQueue = Queue()

listPoints =[np.array([[-0.5,-0.5,-3],[0.5,-0.5,-3],[0.5,0.5,-3],[-0.5,0.5,-3]])]

def keyboardFunc(key,x,y):
    if key==b'Q':
        glutLeaveMainLoop()
    else:
        if(key==b'q'):
            render.translate[2] = -1.0
        elif(key==b'e'):
            render.translate[2] = 1.0
        elif(key==b'a'):
            render.translate[0] = 0.5
        elif(key==b'd'):
            render.translate[0] = -0.5
        elif(key==b'w'):
            render.translate[1] = -0.5
        elif(key==b's'):
            render.translate[1] = 0.5
        elif(key == b'i'):
            render.rotate[0] = 1.0
            render.rotate[1] = 1.0
        elif(key==b'k'):
            render.rotate[0] = -1.0
            render.rotate[1] = 1.0
        elif(key==b'l'):
            render.rotate[0] = -1.0
            render.rotate[2] = 1.0
        elif(key==b'j'):
            render.rotate[0] = 1.0
            render.rotate[2] = 1.0
        elif(key==b'u'):
            render.rotate[0] = 1.0
            render.rotate[3] = 1.0
        elif(key==b'o'):
            render.rotate[0] = -1.0
            render.rotate[3] = 1.0

        glutPostRedisplay()

def doInput():
    global listPoints
    if not taskQueue.empty():
        command = taskQueue.get()
        if (command=='exit'):
            glutLeaveMainLoop() #exit
        elif (command=='insert'):
            listPoints[0] = termInput.pointBuffer
            glutPostRedisplay()
        elif (command=='reset'):
            print("reset")
        elif (command=='3D'):
            render.is3D = True
        else:
            termInput.parsingCommand(command,listPoint)
            listPoint = termInput.pointBuffer
            glutPostRedisplay()
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