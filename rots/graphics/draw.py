# Drawing routines for the objects

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numbers
import random
from math import radians, tan, pi

import textures

from math_classes.vectors import Vector

BOX_QUAD_VERTS = ((0, 3, 2, 1), (3, 6, 7, 2), (6, 4, 5, 7),
                   (4, 0, 1, 5), (1, 2, 7, 5), (4, 6, 3, 0))

BOX_EDGES = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
              (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))

BOX_NORMALS = ([0.0, 0.0, -1.0], [-1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0], [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0], [0.0, -1.0, 0.0])

BOX_TEX_COORDS = ((0,0), (1,0), (1,1), (0,1))

def box(box):
    ''' Draws a box '''

    x_size, y_size, z_size = box.get_sides()
    x = x_size/2.0
    y = y_size/2.0
    z = z_size/2.0
    
    points = ((x, -y, -z), (x, y, -z), 
                (-x, y, -z), (-x, -y, -z), 
                (x, -y, z), (x, y, z),
                (-x, -y, z), (-x, y, z))


    ambient, diffuse, specular, shininess, emissive = box.get_material_properties()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, emissive)

    if box.get_texture():
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, box.get_texture())

    #glEnable(GL_COLOR_MATERIAL)

    glBegin(GL_QUADS)
    for face in BOX_QUAD_VERTS:

        # Dimensions of the box's surface
        down_left = points[face[0]]
        down_right = points[face[1]]
        up_right = points[face[2]]
        up_left = points[face[3]]
        up_left_vec = Vector(up_left)   # Will be used a lot, that's
                                        # why it's created here

        length = (Vector(up_right) - Vector(down_right)).norm()
        width = (Vector(up_right) - Vector(up_left)).norm()

        # The directions of the surface
        down_vec = (Vector(down_right) - Vector(up_right)).normalize()
        right_vec = (Vector(up_right) - Vector(up_left)).normalize()

        # The wanted subdivision size
        goal_sub_size = box.get_subdivision_size()

        # Number of subdivisions
        length_subs = int(length // goal_sub_size) + 1
        width_subs = int(width // goal_sub_size) + 1

        # Actual size of the subdivisions
        length_sub_size = length / float(length_subs)
        width_sub_size = width / float(width_subs)

        # Size as fractions of the whole surface
        length_sub_frac = 1.0 / length_subs
        width_sub_frac = 1.0 / width_subs

        # Draw the surface
        for l in range(length_subs):
            for w in range(width_subs):

                # To show the subdivisions of the surface, uncomment this, aswell as
                # glEnable/Disable GL_COLOR_MATERIAL (directly before and after glBegin/End)
                #random_color = [random.random(), random.random(), random.random()]
                #glColor3fv(random_color)

                glNormal3fv(BOX_NORMALS[BOX_QUAD_VERTS.index(face)])

                glTexCoord2f(w * width_sub_frac, 1 - l * length_sub_frac)
                glVertex3fv((up_left_vec + right_vec * w * width_sub_size + \
                            down_vec * l * length_sub_size).value)

                glTexCoord2f(w * width_sub_frac, 1 - (l + 1) * length_sub_frac)
                glVertex3fv((up_left_vec + right_vec * w * width_sub_size + \
                            down_vec * (l + 1) * length_sub_size).value)

                glTexCoord2f((w + 1) * width_sub_frac, 1 - (l + 1) * length_sub_frac)
                glVertex3fv((up_left_vec + right_vec * (w + 1) * width_sub_size + \
                            down_vec * (l + 1) * length_sub_size).value)

                glTexCoord2f((w + 1) * width_sub_frac, 1 - l * length_sub_frac)
                glVertex3fv((up_left_vec + right_vec * (w + 1) * width_sub_size + \
                            down_vec * l * length_sub_size).value)

    glEnd()

    #glDisable(GL_COLOR_MATERIAL)


    # TODO: Use something like "box.get_line_color()" instead?
    glColor3f(0.0, 0.0, 0.0)    
    glBegin(GL_LINES)
    for line in BOX_EDGES:
        for vert in line:
            glVertex3fv(points[vert])
    glEnd()

    glDisable(GL_TEXTURE_2D)

def surface(surface):
    ''' The drawing routine for a Surface object.
        Calls OpenGL to draw the surface. '''

    # TODO: Tesselate the surface for better lighting effects

    ambient, diffuse, specular, \
             shininess , emissive = surface.get_material_properties()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, emissive)

    if surface.get_texture():
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, surface.get_texture())

    # The dimensions of the surface
    length = surface.get_length()
    width = surface.get_width()
    half_length = length / 2.0
    half_width = width / 2.0
    
    # The wanted subdivision size
    goal_sub_size = surface.get_subdivision_size()

    # Number of subdivisions
    length_subs = int(length // goal_sub_size)
    width_subs = int(width // goal_sub_size)

    # Actual size of the subdivisions
    length_sub_size = length / float(length_subs)
    width_sub_size = width / float(width_subs)

    # Size as fractions of the whole surface
    length_sub_frac = 1.0 / length_subs
    width_sub_frac = 1.0 / width_subs
    
    #glEnable(GL_COLOR_MATERIAL)

    glBegin(GL_QUADS)
    

    for l in range(length_subs):
        for w in range(width_subs):

            # To show the subdivisions of the surface, uncomment this, aswell as
            # glEnable/Disable GL_COLOR_MATERIAL (directly before and after glBegin/End)
            #random_color = [random.random(), random.random(), random.random()]
            #glColor3fv(random_color)

            glNormal3fv(surface.get_normal().value)
            glTexCoord2f(w * width_sub_frac, 1 - l * length_sub_frac)
            glVertex3f(-half_width + w * width_sub_size, 
                        0.0,
                        -half_length + l * length_sub_size)
            glTexCoord2f(w * width_sub_frac, 1 - (l + 1) * length_sub_frac)
            glVertex3f(-half_width + w * width_sub_size, 
                        0.0,
                        -half_length + (l + 1) * length_sub_size)
            glTexCoord2f((w + 1) * width_sub_frac, 1 - (l + 1) * length_sub_frac)
            glVertex3f(-half_width + (w + 1) * width_sub_size, 
                        0.0,
                        -half_length + (l + 1) * length_sub_size)
            glTexCoord2f((w + 1) * width_sub_frac, 1 - l * length_sub_frac)
            glVertex3f(-half_width + (w + 1) * width_sub_size, 
                        0.0,
                        -half_length + l * length_sub_size)
    glEnd()

    #glDisable(GL_COLOR_MATERIAL)

    glDisable(GL_TEXTURE_2D)


def sphere(sphere):
    ''' The drawing routine for a Sphere object.
        Calls OpenGL to draw the sphere. '''
    
    ambient, diffuse, specular, \
             shininess, emissive = sphere.get_material_properties()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, emissive)

    if sphere.get_texture():
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, sphere.get_texture())

    if sphere.get_texture():
        gluQuadricTexture(sphere.get_quadric(), True)

    gluSphere(sphere.get_quadric(),sphere.get_radius(), 60, 60)

    glDisable(GL_TEXTURE_2D)

def loading_screen(texture, ratio):
    ''' Draws a loading screen. It draws a Quad that
        fills the screen, textured with 'texture' '''

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0,0)
    glVertex3f(-ratio, -1.0, 0)
    glTexCoord2f(1,0)
    glVertex3f(ratio, -1.0, 0)
    glTexCoord2f(1,1)
    glVertex3f(ratio, 1.0, 0)
    glTexCoord2f(0,1)
    glVertex3f(-ratio, 1.0, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def AABB(aabb, color):
    ''' Draws an AABB.
        Input: 
            * aabb:
                An AABB as given by ODE (6-tuple:
                (minx, maxx, miny, maxy, minz, maxz))
            * color:
                A 4-tuple describing the wanted color
                of the AABB, given in RGBA. '''

    minx, maxx, miny, maxy, minz, maxz = aabb

    points = ((maxx, miny, minz), (maxx, maxy, minz), 
                (minx, maxy, minz), (minx, miny, minz), 
                (maxx, miny, maxz), (maxx, maxy, maxz),
                (minx, miny, maxz), (minx, maxy, maxz))

    glEnable(GL_COLOR_MATERIAL)

    glColor4fv(color)

    glBegin(GL_LINES)
    for line in BOX_EDGES:
        for vert in line:
            glVertex3fv(points[vert])
    glEnd()

    glDisable(GL_COLOR_MATERIAL)

def draw2D_box(color, width, height):
    glColor4fv(color)
    glBegin(GL_QUADS)

    glVertex3f(-width/2, -height/2, 0.0)
    glVertex3f(width/2, -height/2, 0.0)
    glVertex3f(width/2, height/2, 0.0)
    glVertex3f(-width/2, height/2, 0.0)

    glEnd()
