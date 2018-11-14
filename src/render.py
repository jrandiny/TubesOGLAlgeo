# Lib OpenGL
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("Tidak ada library opengl :(")

import random
import numpy as np

listPoints =[np.zeros([1,2])]
colorList = np.empty((0,3))
zoomRatio = 1.0
aspect = 1.0

is3D = False

translate = [0.0,0.0,-1200.0]
rotate = [0.0,0.0,0.0,0.0]

def grid():
# I.S. : Layar grafik terinisialisasi
# F.S. : Tercetak grid 2D atau 3D sesuai variabel global is3D
    glBegin(GL_LINES)
    # x
    glColor3f(1.0,0,0) # red
    glVertex3f(-500.0, 0.0, 0.0)
    glVertex3f(500.0, 0.0, 0.0)

    # y
    glColor3f(0,1.0,0) # hijau
    glVertex3f(0.0, -500.0, 0.0)
    glVertex3f(0.0, 500.0, 0.0)

    if(is3D):
        glColor3f(0,0,1.0) # biru
        glVertex3f(0.0, 0.0, -500.0)
        glVertex3f(0.0, 0.0, 500.0)
    glEnd()


def displayFunc():
# I.S. : Window grafik terinisialisasi
# F.S. : Digambar titik-titik dengan mode GL_POLYGON(is3D false) atau GL_QUADS(is3D true)
#        Warna akan dirandom jika belum terdapat pada variabel global colorList
    global translate
    global rotate
    global colorList

    renderViewport()

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glTranslatef(translate[0],translate[1],translate[2])

    glRotatef(rotate[0],1,0,0)
    glRotatef(rotate[1],0,1,0)
    glRotatef(rotate[2],0,0,1)

    if(len(listPoints)>len(colorList)):
        tempList = []
        for poly in listPoints:
            tempList.append(np.array([random.random(), random.random(), random.random()]))
        colorList = np.array(tempList)    

    if(is3D):
                 
        for i,poly in enumerate(listPoints):
            glColor3f(colorList[i][0],colorList[i][1],colorList[i][2])
            # glColor3f(random.random(), random.random(), random.random()) 
            glBegin(GL_POLYGON) 
            for point in poly:
                glVertex3f(point[0],point[1],point[2])
            glEnd()

        
    else:             
        for i,poly in enumerate(listPoints):
            glBegin(GL_POLYGON)  
            glColor3f(colorList[i][0],colorList[i][1],colorList[i][2])
            # glColor3f(random.random(), random.random(), random.random()) 
            for point in poly:
                glVertex3f(point[0],point[1],point[2])
            glEnd()

    grid()

    glutSwapBuffers()

def renderViewport():
# I.S. : Sistem grafik terinisialisasi
# F.S. : Viewport diset
    glLoadIdentity()
    gluPerspective(45,aspect,0.1,2000.0)
    # glFrustum(-1.0*zoomRatio*aspect,1.0*zoomRatio*aspect,-1.0*zoomRatio,1.0*zoomRatio,1.0,50.0) 



def windowResized(width,height):
# I.S. : Sistem grafik terinisialisasi, window diresize
# F.S  : Menetapkan aspect dan menetapkan viewport ulang
    glViewport(0,0,width,height)
    global aspect
    aspect = float(width) / float(height)
    renderViewport()

