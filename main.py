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

listPoint = np.array([[-0.5,-0.5,-3],[0.5,-0.5,-3],[0.5,0.5,-3],[-0.5,0.5,-3]])

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

        glutPostRedisplay()

def keySpecialFunc(key,x,y):
    if(key == GLUT_KEY_UP):
        render.rotate[0] = 1.0
        render.rotate[1] = 1.0
    elif(key==GLUT_KEY_DOWN):
        render.rotate[0] = -1.0
        render.rotate[1] = 1.0
    elif(key==GLUT_KEY_RIGHT):
        render.rotate[0] = -1.0
        render.rotate[2] = 1.0
    elif(key==GLUT_KEY_LEFT):
        render.rotate[0] = 1.0
        render.rotate[2] = 1.0
    glutPostRedisplay()

def doInput():
    global listPoint
    if not taskQueue.empty():
        command = taskQueue.get()
        if (command=='exit'):
            glutLeaveMainLoop() #exit
        elif (command=='insert'):
            listPoint = termInput.pointBuffer
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
    global listPoint
    render.listPoint = listPoint
    render.displayFunc()

if __name__ =="__main__":
    # Threading input system
    inputThread = threading.Thread(target=termInput.worker,args=(taskQueue,))

    #setup OGL window
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE)
    glutInitWindowSize(1000, 1000)
    glutCreateWindow("ini layar loh wkwkwkwk!!!")

    inputThread.start()

    # GLUT callbacks
    glutReshapeFunc(render.windowResized)
    glutDisplayFunc(prepareDisplay)
    glutKeyboardFunc(keyboardFunc)
    glutSpecialFunc(keySpecialFunc)
    glutIdleFunc(doInput)

    glutMainLoop()