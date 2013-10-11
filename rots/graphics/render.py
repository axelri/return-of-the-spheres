import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.depth_texture import *
from OpenGL.GL.ARB.shadow import *

from math import asin

import lights
import games
from objects import shapes
from math_classes import matrices
from math_classes.vectors import Vector

shadow_color = [0.1, 0.1, 0.1]
light_color = [1.0, 1.0, 1.0]

def render(game):
    ''' Renders the scene: Clears the screen, sets up the camera
    and lights, draws the player and all other entities at their
    current position and flips the buffers.

    Input:  game: A Game object '''
    
    camera = game.get_camera()
    player = game.get_player()
    object_list = game.get_object_list()
    light_list = game.get_light_list()


    glLoadIdentity()

    camera.view(player)
    #camera_view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    #game.add_constant('camera_view_matrix', camera_view_matrix)


    if game.get_debug_state():
        game.update_debug_screen()

    # Update the light positions

    for light in light_list:
        pos = light.get_pos()
        light.set_pos(pos)

    draw_scene(object_list, game)
    #draw_scene_with_shadows(game, object_list)
    #draw_with_shadows(game, object_list, light_list, player, camera)

    if game.get_debug_state() == 2:
        draw_debug_objects(object_list, light_list)

    pygame.display.flip()


def draw_scene(object_list, game):
    ''' Draws the scene. '''

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    for item in object_list:
        glPushMatrix()
        item.draw()
        glPopMatrix()

def draw_debug_objects(object_list, light_list):
    ''' Draw AABBs and the position of the lights '''

    for item in object_list:
        glPushMatrix()
        item.draw_AABB()
        glPopMatrix()

    for light in light_list:
        glPushMatrix()
        light.draw_pos()
        glPopMatrix()

def draw_with_shadows(game, object_list, light_list, player, camera):
    # Only shadows for the player yet so far...

    glDisable(GL_LIGHTING)
    for i in range(len(light_list)):
        light = light_list[i]

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        #light_pos = light.get_pos()
        #light_focus = obj.get_pos()
        #dist = (light_focus - light_pos).norm()
        # Why 2.9?
        #light_angle = degrees(2 * asin(2.9/dist))
        #near = dist - 2.9
        #far = dist + 2.9

        ## Shadow step 1
        # Create shadowmap
        focus = [0.0, 0.0, 0.0]
        pos = light.get_pos().value
        angle = 100
        near = 0.1
        far = 20
        lights.initialize_shadowmap(lights.GLLIB_SHADOW_MAP1 + i, pos, focus,
                                    lightviewangle = angle, near = near, far = far)
        # Draw all objects
        for item in object_list:
            glPushMatrix()
            item.draw()
            glPopMatrix()

        ## Shadow step 2
        lights.create_shadowmap(lights.GLLIB_SHADOW_MAP1 + i)
    glEnable(GL_LIGHTING)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.view(player)

    # Set lights
    for light in light_list:
        light.change_color(shadow_color)
        light.change_diffuse_color(light_color)

    # Draw all objects
    for item in object_list:
        glPushMatrix()
        item.draw()
        glPopMatrix()    

    # Set light color to shadow color
    for light in light_list:
        light.change_diffuse_color(shadow_color)
        light.disable()

    ## Shadow step 3
    lights.enable_shadowshading()
    for i in range(len(light_list)):
        light_list[i].enable()
        lights.render_shadow_comparison(lights.GLLIB_SHADOW_MAP1 + i)
        # Draw all objects
        for item in object_list:
            glPushMatrix()
            item.draw()
            glPopMatrix()
        light_list[i].disable()

    for light in light_list:
        light.enable()

    lights.disable_shadowshading()

    ## Shadows step 4
    lights.reset_OpenGL_parameters()


# def draw_scene_with_shadows(game, object_list):

#     # TODO: Remove the bug that causes the textures on the shapes to float around...

#     # Constants
#     constants = game.get_constants()
#     shadow_map_size = constants['shadow_map_size']
#     window_width = constants['window_width']
#     window_height = constants['window_height']

#     light_projection_matrix = constants['light_projection_matrix']
#     light_view_matrix_list = constants['light_view_matrix_list']
#     camera_projection_matrix = constants['camera_projection_matrix']
#     camera_view_matrix = constants['camera_view_matrix']
#     bias_matrix = constants['bias_matrix']

#     shadow_map_texture = constants['shadow_map_texture']


#     for light, light_view_matrix in zip(game.get_light_list(), light_view_matrix_list):
        
#         light_index = light.get_light_index()
#         light_pos = light.get_pos()
#         ambient = light.get_ambient()
#         diffuse = light.get_diffuse()
#         specular = light.get_specular()
#         is_spotlight = light.is_spotlight()

#         ### First pass - from light's point of view

#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

#         glMatrixMode(GL_PROJECTION)
#         glLoadMatrixf(light_projection_matrix)

#         glMatrixMode(GL_MODELVIEW)
#         glLoadMatrixf(light_view_matrix)

#         # Use viewport the same size as the shadow map
#         glViewport(0, 0, shadow_map_size, shadow_map_size)

#         # Draw back faces into the shadow map
#         glCullFace(GL_FRONT)

#         # Disable color writes, and use flat shading for speed
#         glShadeModel(GL_FLAT)
#         glColorMask(0, 0, 0, 0)

#         # Draw the scene
#         draw_scene(object_list)

#         # Read the depth buffer into the shadow map texture
#         glBindTexture(GL_TEXTURE_2D, shadow_map_texture)
#         glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 0, 0, shadow_map_size, shadow_map_size)

#         # Restore states
#         glCullFace(GL_BACK)
#         glShadeModel(GL_SMOOTH)
#         glColorMask(1, 1, 1, 1)

#         ### 2nd pass - Draw from camera's point of view
        
#         glClear(GL_DEPTH_BUFFER_BIT)
#         glMatrixMode(GL_PROJECTION)
#         glLoadMatrixf(camera_projection_matrix)

#         glMatrixMode(GL_MODELVIEW)
#         glLoadMatrixf(camera_view_matrix)

#         glViewport(0, 0, window_width, window_height)

#         # Use dim light to represent shadowed areas
#         glLightfv(light_index, GL_POSITION, light_pos.value + tuple([float(not is_spotlight)]))
#         glLightfv(light_index, GL_AMBIENT, (Vector(ambient) * 0.2).value)
#         glLightfv(light_index, GL_DIFFUSE, (Vector(diffuse) * 0.2).value)
#         glLightfv(light_index, GL_SPECULAR, (Vector(specular) * 0).value)

#         # Draw the scene
#         draw_scene(object_list)

#         ### 3rd pass - Draw with bright light

#         # Restore the light
#         light._setup()

#         # Calculate texture matrix for projection
#         # This matrix takes us from eye space to the light's clip space
#         # It is postmultiplied by the inverse of the current view matrix when specifying texgen

#         texture_matrix = matrices.matrix_mult(bias_matrix, matrices.matrix_mult(light_projection_matrix, light_view_matrix))

#         # Set up texture coordinate generation.
#         glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
#         glTexGenfv(GL_S, GL_EYE_PLANE, texture_matrix[0:16:4])
#         glEnable(GL_TEXTURE_GEN_S)

#         glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
#         glTexGenfv(GL_T, GL_EYE_PLANE, texture_matrix[1:16:4])
#         glEnable(GL_TEXTURE_GEN_T)

#         glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
#         glTexGenfv(GL_R, GL_EYE_PLANE, texture_matrix[2:16:4])
#         glEnable(GL_TEXTURE_GEN_R)

#         glTexGeni(GL_Q, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
#         glTexGenfv(GL_Q, GL_EYE_PLANE, texture_matrix[3:16:4])
#         glEnable(GL_TEXTURE_GEN_Q)

#         # Bind & enable shadow map texture
#         glBindTexture(GL_TEXTURE_2D, shadow_map_texture)
#         glEnable(GL_TEXTURE_2D)

#         # Enable shadow comparison
#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE_ARB, GL_COMPARE_R_TO_TEXTURE)

#         # Shadow comparison should be true (ie not in shadow) if r<=texture
#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC_ARB, GL_LEQUAL)

#         # Shadow comparison should generate an INTENSITY result
#         glTexParameteri(GL_TEXTURE_2D, GL_DEPTH_TEXTURE_MODE_ARB, GL_INTENSITY)

#         # Set alpha test to discard false comparisons
#         glAlphaFunc(GL_GEQUAL, 0.99)
#         glEnable(GL_ALPHA_TEST)

#         # Draw the scene
#         draw_scene(object_list)

#         # Disable textures and texgen
#         glDisable(GL_TEXTURE_2D)

#         glDisable(GL_TEXTURE_GEN_S)
#         glDisable(GL_TEXTURE_GEN_T)
#         glDisable(GL_TEXTURE_GEN_R)
#         glDisable(GL_TEXTURE_GEN_Q)

#         # Restore other states
#         glDisable(GL_ALPHA_TEST)
