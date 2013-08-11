import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL.glget import *
from OpenGL.GL.EXT.texture_filter_anisotropic import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def load_image(file_name):
    ''' Takes an image file and converts it into a string 
        that OpenGL can read. 

    Input:
    * file_name:   The name of the image file containing 
                    the image you want to load. It can be
                    of most of the normal formats (jpg etc).

    Output:
    * image_str:    A string containing the information from
                    the image file in a format readable for 
                    OpenGL. '''

    # Load the image
    fullname = os.path.join('graphics/texture_data', file_name)
    try:
        image = pygame.image.load(fullname)
        image_size = image.get_size()
        image_str = pygame.image.tostring(image, 'RGB', True)
    except pygame.error, message:
        print 'Pygame error: ', message
        print 'Cannot load texture:', file_name
        try:
            # Try to load default texture
            missing_tex_path = os.path.join('graphics/texture_data',
                                            'missing_texture.png')
            missing_tex = pygame.image.load(missing_tex_path)
            missing_tex_size = 512, 512
            missing_tex_str = pygame.image.tostring(missing_tex,
                                                        'RGB', True)
            return missing_tex_str, missing_tex_size
        except Exception, message:
            raise SystemExit, message
        
    return image_str, image_size

def load_texture(image_file):
    ''' Creates a texture object from the image file and 
        returns the index of that object.

    Input:
    * image_file:   The name of the image file containing 
                    the image you want to load. It can be
                    of most of the normal formats (jpg etc).
    * width:        The width of the image, in pixels.
    * heigth:       The heigth of the image, in pixels.

    Output:
    * tex:          The OpenGL index of the generated texture.
    '''

    # Create image string
    image_str, image_size = load_image(image_file)

    width, heigth = image_size

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

    # Cleanup
    del image_str

    # Return the texture index
    return tex
