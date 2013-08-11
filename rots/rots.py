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

def game_loop(game, world, space, player, camera,
             clock, contactgroup, fps, dt):
    #sun_light.set_pos(sun.get_pos())

    # Take input
    run, direction, jump, toggle_debug, toggle_pause = game.take_input()

    if toggle_debug:
        game.toggle_debug()

    # Simulate
    physics.update_physics(world, space, contactgroup, game, dt)

    # Move
    forwardVector = camera.update(player)
    player.move(direction, forwardVector, jump)

    # Render

    render.render(game)
    clock.tick(fps)
    return run, toggle_pause

def pause_loop(game, clock, fps):
    run, direction, jump, toggle_debug, toggle_pause = game.take_input()
    clock.tick(fps)
    return run, toggle_pause

def main():
    ''' Main routine of the game.'''

    width, height = init_graphics.init_window('testODE 2')

    game = scenes.init_scene()

    player = game.get_player()
    world = game.get_world()
    space = game.get_space()
    contactgroup = game.get_contactgroup()
    camera = game.get_camera()
    clock = game.get_clock()

    run = True
    pause = False

    fps = 30
    dt = 1.0/fps
    run = True
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
            # toggling back to unpaused
            pygame.mouse.set_pos(width/ 2.0,
                                height / 2.0)
            x, y = pygame.mouse.get_rel()

        if not pause:
            run, toggle_pause = game_loop(game, world, space, 
                                        player, camera, clock,
                                        contactgroup, fps, dt)
        else:
            run, toggle_pause = pause_loop(game, clock, fps)
    
    pygame.mixer.music.fadeout(2000)
    pygame.time.wait(2000)        


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
