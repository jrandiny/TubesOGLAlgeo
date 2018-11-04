import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices = (
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,1,1),
    (-1,-1,1)
)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,6),
    (5,1),
    (5,4),
    (5,6),
    (7,3),
    (7,4),
    (7,6)
)
'''
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (5,1),
    (5,4),
    (5,7),
    (6,3),
    (6,4),
    (6,7)
)
'''
def Cube():
    glBegin(GL_POLYGON)          
    glColor3f(random.random(), random.random(), random.random()) 
    glVertex3f(-0.5, -0.5,-3)    
    glVertex3f( 0.5, -0.5,-3)
    glVertex3f( 0.5,  0.5,-3)
    glVertex3f(-0.5,  0.5,-3)
    glEnd()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display=(800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45,(display[0]/display[1]),0.1,50.0)

    glTranslatef(0.0,0.0,-5)

    glRotatef(0,0,0,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(1,10,20,30)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

main()