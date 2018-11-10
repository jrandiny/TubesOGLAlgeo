# Lib OpenGL
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("Tidak ada library opengl :(")

import random
import numpy as np

listPoints =[np.array([[-0.5,-0.5,-3],[0.5,-0.5,-3],[0.5,0.5,-3],[-0.5,0.5,-3]])]
zoomRatio = 1.0
aspect = 1.0

is3D = False

translate = [0.0,0.0,-5.0]
rotate = [0.0,0.0,0.0,0.0]

def grid():
    glBegin(GL_LINES)
    # x
    glColor3f(1.0,0,0) # red
    glVertex3f(-4.0, 0.0, 0.0)
    glVertex3f(4.0, 0.0, 0.0)

    # y
    glColor3f(0,1.0,0) # hijau
    glVertex3f(0.0, -4.0, 0.0)
    glVertex3f(0.0, 4.0, 0.0)

    if(is3D):
        glColor3f(0,0,1.0) # biru
        glVertex3f(0.0, 0.0, -4.0)
        glVertex3f(0.0, 0.0, 4.0)
    glEnd()


def displayFunc():
    global translate
    global rotate

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # print("called display")

    glTranslatef(translate[0],translate[1],translate[2])
    translate = [0.0,0.0,0.0]

    glRotatef(rotate[0],rotate[1],rotate[2],rotate[3])
    rotate = [0.0,0.0,0.0,0.0]



    
    glBegin(GL_POLYGON)          
    glColor3f(random.random(), random.random(), random.random()) 
    for poly in listPoints:
        for point in poly:
            glVertex3f(point[0],point[1],point[2])

    glEnd()

    grid()

    glutSwapBuffers()

def renderViewport():
    glLoadIdentity()
    glFrustum(-1.0*zoomRatio*aspect,1.0*zoomRatio*aspect,-1.0*zoomRatio,1.0*zoomRatio,1.0,50.0) 



def windowResized(width,height):
    glViewport(0,0,width,height)
    global aspect
    aspect = float(width) / float(height)
    renderViewport()

