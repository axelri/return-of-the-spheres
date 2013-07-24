# Test of the physics engine

import pygame
from graphics import glFreeType
from graphics import init_graphics
from pygame.locals import *
from OpenGL.GL import *
from math import cos

import traceback
import sys
import time

def main():
    init_graphics.init_window('testPhysics', HAVE_FULLSCREEN = False)
    our_font = glFreeType.font_data('graphics/texture_data/fonts/test.ttf', 16)

    run = True
    rot = 0
    # Start timing

    while run:

        currentEvents = pygame.event.get() # cache current events
        for event in currentEvents:
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False

        rot = render(our_font, rot)
        #print 'Pos:', player.get_pos().value

def render(font, rot):
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    # Reset The View 
    # Step back (away from objects)
    glTranslatef (0.0, 0.0, -1.0)

    # Red Text
    glColor3f (0, 1, 0)

    glPushMatrix ()
    glLoadIdentity ()
    # Spin the text, rotation around z axe == will appears as a 2d rotation of the text on our screen
    glRotatef (rot, 0, 0, 1)
    glScalef (1, 0.8 + 0.3* cos (rot/5), 1)
    glTranslatef (-180, 0, 0)
    font.glPrint (320, 240, "Active FreeType Text - %7.2f" % (rot))
    glPopMatrix ()

    # //Uncomment this to test out print's ability to handle newlines.
    # font.glPrint (320, 240, "Here\nthere\nbe\n\nnewlines %f\n." % (rot))
    pygame.display.flip()

    return rot + 0.051

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
