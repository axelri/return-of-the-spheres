import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import traceback
import sys

from graphics import init_graphics, textures
from math_classes import vectors

def create_display_list():

	displayListIndex = glGenLists(1)
	glNewList(displayListIndex, GL_COMPILE)

	glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0, 1.0, 1.0, 1.0])
	glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
	glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
	glMateriali(GL_FRONT, GL_SHININESS, 64)

	earth_big_str = textures.loadImage('graphics/texture_data/celestial_bodies/earth_big.jpg')
	earth_big_tex = textures.loadTexture(earth_big_str, 1024, 1024)

	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, earth_big_tex)

	quadric = gluNewQuadric()

	gluQuadricTexture(quadric, True)
	gluSphere(quadric, 0.5, 60, 60)
	glDisable(GL_TEXTURE_2D)

	glEndList()
	return displayListIndex



def draw_sphere(index, body):

	x,y,z = body.getPosition()
	R = body.getRotation()
	rot = [R[0], R[3], R[6], 0.,
			R[1], R[4], R[7], 0.,
			R[2], R[5], R[8], 0.,
			x, y, z, 1.0]
	glPushMatrix()
	glMultMatrixd(rot)
	glCallList(index)
	glPopMatrix()

def near_callback(args, geom1, geom2):
	"""Callback function for the collide() method.

	This function checks if the given geoms do collide and
	creates contact joints if they do.
	"""
	# Check if the objects do collide
	contacts = ode.collide(geom1, geom2)

	# Create contact joints
	world,contactgroup = args
	for c in contacts:
		c.setBounce(0.2)
		c.setMu(5000)
		j = ode.ContactJoint(world, contactgroup, c)
		j.attach(geom1.getBody(), geom2.getBody())


def take_input():
	currentEvents = pygame.event.get() # cache current events
	run = True
	for event in currentEvents:
		if event.type == QUIT or \
		(event.type == KEYDOWN and event.key == K_ESCAPE):
			run = False
	keyState = pygame.key.get_pressed()

	xDir = keyState[K_d] - keyState[K_a]
	zDir = keyState[K_s] - keyState[K_w]

	direction = [xDir, 0.0, zDir]

	return run, direction

def main():

	init_graphics.init_window('testODE')

	# Light source
	glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
	glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
	glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
	glEnable(GL_LIGHT0)

	gluLookAt (0.0, 3.6, 4.8, 0.0, 0.5, 0.0, 0.0, 1.0, 0.0)

	# Create a world object
	world = ode.World()
	world.setGravity( (0,-9.81,0) )
	world.setERP(0.8)
	world.setCFM(1E-5)

	# Create a space object
	space = ode.Space()

	# Create a plane geom which prevent the objects from falling forever
	floor = ode.GeomPlane(space, (0,1,0), 0)

	# Create sphere
	sphere_index = create_display_list()

	sphere_body = ode.Body(world)
	M = ode.Mass()
	M.setSphere(1, 0.5)
	sphere_body.setMass(M)
	sphere_body.setPosition((0,2,0))

	sphere_geom = ode.GeomSphere(space, 0.5)
	sphere_geom.setBody(sphere_body)

	# Create group for contact joints
	contactgroup = ode.JointGroup()

	fps = 50
	dt = 1.0/fps
	run = True
	clock = pygame.time.Clock()
	speed = 1

	lastDir = [0.0, 0.0, 0.0]

	while run:

		run, direction = take_input()

		# Move
		if direction == lastDir:
			pass
		else:
			current_vel = vectors.Vector(list(sphere_body.getLinearVel()))
			corr_vel = vectors.Vector(lastDir)*-speed + vectors.Vector(direction)*speed
			new_vel = current_vel + corr_vel
			sphere_body.setLinearVel(new_vel.value)
			lastDir = direction

		# Simulate
		n = 2

		for i in range(n):
			# Detect collisions and create contact joints
			space.collide((world,contactgroup), near_callback)

			# Simulation step
			world.step(dt/n)

			# Remove all contact joints
			contactgroup.empty()

		# Draw
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		draw_sphere(sphere_index, sphere_body)
		pygame.display.flip()

		clock.tick(fps)

if __name__ == '__main__':
	try:
		main()
	except Exception:
		traceback.print_exc(file=sys.stdout)
	finally:
		pygame.quit()
