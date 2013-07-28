import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL.glget import *
from OpenGL.GL.EXT.texture_filter_anisotropic import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# TODO: Better loading functions with error handling
# (better example in sound_effects)

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

def loadTexture(image_file, width, heigth):
    ''' Creates a texture object from the image file and 
        returns the index of that object.

    Input:
    * image_file:   The name of the image file containing 
                    the image you want to load. It can be
                    of most of the normal formats (jpg etc).
                    It must be a string with the relative
                    or absolute path to the file, including
                    the file ending. If you use a relative 
                    path, it is the relative path from the
                    file the main routine is run that should
                    be used, NOT the path relative this file    (or is it?)
    * width:        The width of the image, in pixels.
    * heigth:       The heigth of the image, in pixels.

    Output:
    * tex:          The OpenGL index of the generated texture.
    '''

    # Create image string
    image_str = loadImage(image_file)

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
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, 
                    GL_LINEAR)

    gluBuild2DMipmaps( GL_TEXTURE_2D, GL_RGBA, width, heigth, 
                     GL_RGB, GL_UNSIGNED_BYTE, image_str )

    # get the largest anisotropy supported by the graphics card
    largest = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, largest)

    # Return the texture index
    return tex
