# Drawing routines for the objects

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numbers
import random
from math import radians, tan, pi

import textures

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

    # TODO: Add subdivision

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

    glBegin(GL_QUADS)
    for face in BOX_QUAD_VERTS:
        glNormal3fv(BOX_NORMALS[BOX_QUAD_VERTS.index(face)])
        for vert, i in zip(face, range(4)):
            tex_coord = BOX_TEX_COORDS[i]
            glTexCoord2f(tex_coord[0], tex_coord[1])
            glVertex3fv(points[vert])
    glEnd()

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

    Input:  surface: A Surface object

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
            glTexCoord2f(w * width_sub_frac, 1 - (l + 1) *length_sub_frac)
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

    Input:  surface: A Sphere object

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

def start_screen(start_texture, ratio):
    ''' Draws a start screen. It draws a Quad that
        fills the screen, textured with 'start_screen_texture' '''

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, start_texture)
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

def AABB(aabb):
    ''' Draws an AABB.
        Input: An AABB as given by ODE (6-tuple:
                (minx, maxx, miny, maxy, minz, maxz)) '''
    
    # TODO: Add possibility to change color?

    minx, maxx, miny, maxy, minz, maxz = aabb

    points = ((maxx, miny, minz), (maxx, maxy, minz), 
                (minx, maxy, minz), (minx, miny, minz), 
                (maxx, miny, maxz), (maxx, maxy, maxz),
                (minx, miny, maxz), (minx, maxy, maxz))

    glBegin(GL_LINES)
    for line in BOX_EDGES:
        for vert in line:
            glVertex3fv(points[vert])
    glEnd()
