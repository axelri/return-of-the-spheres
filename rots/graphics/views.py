from OpenGL.GL import *
from OpenGL.GLU import *

class View:

	def __init__(self, width, heigth, aspect_angle, near = 0.1, far = 100.0):
		self._width = width
		self._heigth = heigth
		self._aspect_angle = aspect_angle
		self._near = near
		self._far = far
		self._ratio = float(width)/float(heigth)

	def setup(self):
		''' Set up the viewport and perspective '''
		glViewport(0, 0, self._width, self._heigth)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(self._aspect_angle, self._ratio, self._near, self._far)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	## Getters

	def get_aspect_angle(self):
		return self._aspect_angle

	def get_width(self):
		return self._width

	def get_heigth(self):
		return self._heigth

	def get_near(self):
		return self._near

	def get_far(self):
		return self._far

	## Setters

	def set_aspect_angle(self, aspect_angle):
		self._aspect_angle = aspect_angle

	def set_width(self, width):
		self._width = width
		self._ratio = float(width)/float(heigth)

	def set_heigth(self, heigth):
		self._heigth = heigth
		self._ratio = float(width)/float(heigth)

	def set_near(self, near):
		self._near = near

	def set_far(self, far):
		self._far = far
