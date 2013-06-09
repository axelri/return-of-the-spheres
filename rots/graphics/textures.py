import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# NOTE: loadImage and loadTexture could be merged into one 
# single function, loadTexture(image_file)

def loadImage(image_file):
    ''' Takes an image file and converts it into a string 
        that OpenGL can read. 

    Input:
    * image_file:   The name of the image file containing 
                    the image you want to load. It can be
                    of most of the normal formats (jpg etc).
                    It must be a string with the relative
                    or absolute path to the file, including
                    the file ending. If you use a relative 
                    path, it is the relative path from the
                    file the main routine is run that should
                    be used, NOT the path relative this file.

    Output:
    * image_str:    A string containing the information from
                    the image file in a format readable for 
                    OpenGL. '''

    # Load the image
    image = pygame.image.load(image_file)
    image_str = pygame.image.tostring(image, 'RGB', True)
    return image_str    

def loadTexture(image_str):
    ''' Creates a texture object from the image given in 
        image_str and returns the index of that object.

    Input:
    * image_str:    A string containing the information from
                    an image file in a format readable for 
                    OpenGL. 

    Output:
    * tex:          The OpenGL index of the generated texture.
    '''

    # Create a texture object
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)

    glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )

    # Specify some paramaters 
    # (What to do when they "run out of picture": here repeat it)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, 
                    GL_LINEAR_MIPMAP_LINEAR)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, 
    #                GL_LINEAR_MIPMAP_LINEAR) #Why doesn't this line work?

    gluBuild2DMipmaps( GL_TEXTURE_2D, 3, 256, 256, 
                     GL_RGB, GL_UNSIGNED_BYTE, image_str )

    # Return the texture index
    return tex