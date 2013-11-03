from OpenGL.GL import *
from OpenGL.GLU import *

class View:

	def __init__(self, width, height, aspect_angle, near = 0.1, far = 100.0):
		self._width = width
		self._height = height
		self._aspect_angle = aspect_angle
		self._near = near
		self._far = far
		self._ratio = float(width)/float(height)

	def setup(self):
		''' Set up the viewport and perspective '''
		glViewport(0, 0, self._width, self._height)
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

	def get_height(self):
		return self._height

	def get_near(self):
		return self._near

	def get_far(self):
		return self._far

	## Setters

	def set_aspect_angle(self, aspect_angle):
		self._aspect_angle = aspect_angle

	def set_width(self, width):
		self._width = width
		self._ratio = float(width)/float(height)

	def set_height(self, height):
		self._height = height
		self._ratio = float(width)/float(height)

	def set_near(self, near):
		self._near = near

	def set_far(self, far):
		self._far = far
