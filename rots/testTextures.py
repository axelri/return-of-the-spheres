#!/usr/bin/env python
import pygame
from pygame.locals import *

import traceback
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def loadTexture(image_file):
    '''creates a texture'''
    # Load an image
    image = pygame.image.load(image_file)
    image_str = pygame.image.tostring(image, 'RGB', True)

    # Create a texture object
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)

    glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )

    # Specify some paramaters 
    # (What to do) when they "run out of picture": here repeat it
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_LINEAR) #Why doesn't this line work?

    gluBuild2DMipmaps( GL_TEXTURE_2D, 3, 256, 256, 
                     GL_RGB, GL_UNSIGNED_BYTE, image_str )

    # Return the texture index
    return tex

def drawTexture(tex):
    '''draws a quad with our texture on it'''
    # Select our texture (must be called before glBegin)
    glBindTexture(GL_TEXTURE_2D, tex)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0,  0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0, -1.0,  0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0,  0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0,  0.0)
    glEnd()


def main():
    "run the demo"
    #initialize pygame and setup an opengl display
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)        #use our zbuffer
    glEnable(GL_TEXTURE_2D)

    #setup the camera
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0,640/480.0,0.1,100.0)    #setup lens
    glTranslatef(0.0, 0.0, -3.0)                #move back
    #glRotatef(25, 1, 0, 0)                      #orbit higher
    tex = loadTexture('graphics/textures/puppy.jpeg')

    while 1:
        #check for quit'n events
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        #clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #orbit camera around by 1 degree
        glRotatef(1, 0, 1, 0)                    

        # draw the texture
        drawTexture(tex)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
