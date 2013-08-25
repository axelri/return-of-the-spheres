import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import traceback
import sys

import shapes
import games
import players
from graphics import render, init_graphics, lights, cameras, textures
from math_classes.vectors import Vector
from physics_engine import physics
from text import TextBox
import scenes

def game_loop(game):

    # Take input
    run, direction, jump, toggle_debug, toggle_pause = game.take_input()
    player = game.get_player()
    camera = game.get_camera()
    clock = game.get_clock()
    fps = game.get_fps()

    if toggle_debug:
        game.toggle_debug()

    # Simulate
    physics.update_physics(game)

    # Move
    forwardVector = camera.update(player)
    player.move(direction, forwardVector, jump)

    # Render

    render.render(game)
    clock.tick(fps)
    return run, toggle_pause

def pause_loop(game):
    run, direction, jump, toggle_debug, toggle_pause = game.take_input()
    clock = game.get_clock()
    fps = game.get_fps()
    
    clock.tick(fps)
    return run, toggle_pause

def main():
    ''' Main routine of the game.'''

    width, height, start_screen = init_graphics.init_window('testODE 2', 
                                                            'stars-5.jpg')

    game = scenes.init_scene(start_screen)

    player = game.get_player()
    camera = game.get_camera()
    clock = game.get_clock()

    run = True
    pause = False
    toggle_pause = False

    # Background music
    pygame.mixer.music.load('sound/sound_data/02. II. Molto vivace.ogg')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    while run:

        if toggle_pause:
            pause = not pause
            pygame.mouse.set_visible(int(pause))

            # Hack to prevent sudden rotation of the camera when
            # toggling back to unpaused (doesn't work properly yet...)
            #for i in range(4):
            pygame.mouse.set_pos(width/ 2.0,
                                height / 2.0)
            x, y = pygame.mouse.get_rel()

        if not pause:
            run, toggle_pause = game_loop(game)
        else:
            run, toggle_pause = pause_loop(game)
    
    #Fade out the music after quitting the game
    pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
