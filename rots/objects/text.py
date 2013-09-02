import os

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import ImageFont
from math_classes import matrices
from math_classes.vectors import Vector
from math import pi

class TextBox(object):
    def __init__ (self, font_name, pixel_height, x, y, color, enabled = True):
        # We haven't yet allocated textures or display lists
        self._allocated = False
        self._font_height = pixel_height
        self._font_name = font_name
        self._x = x
        self._y = y
        self._color = color
        self._string = ""
        self._rotation = 0
        self._enabled = enabled

        # Try to obtain the FreeType font
        fullname = os.path.join('graphics/texture_data/fonts', font_name)
        try:
            ft = ImageFont.truetype (fullname, pixel_height)
        except:
            raise ValueError, "Unable to locate true type font '%s'" % (font_name)

        # Here we ask opengl to allocate resources for
        # all the textures and displays lists which we
        # are about to create.  
        self._list_base = glGenLists (128)

        # Consturct a list of 128 elements. This
        # list will be assigned the texture IDs we create for each glyph
        self.textures = [None] * 128

        # This is where we actually create each of the fonts display lists.
        for i in xrange (128):
            make_dlist (ft, i, self._list_base, self.textures);

        self._allocated = True

        return

    def get_string(self):
        return self._string

    def set_string(self, s):
        self._string = s

    def append_string(self, s):
        self._string += s

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_orientation(self):
        return matrices.generate_rotation_matrix(Vector([0.0,0.0,1.0]), self._rotation)

    def set_rotation(self, r):
        self._rotation = r

    def rotate(self, angle):
        self._rotation = self._rotation + angle % (2*pi)

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def toggle(self):
        self._enabled = not self._enabled

    def draw(self):

        if not self._enabled:
            return

        glLoadIdentity()
        rotMatrix = self.get_orientation()
        glMultMatrixf(rotMatrix)
        
        # We want a coordinate system where things coresponding to window pixels.
        pushScreenCoordinateMatrix()
    
        # //We make the height about 1.5* that of
        h = float (self._font_height) / 0.63        
    
        string = self._string
        if (string == None):
            pop_projection_matrix()
            return
        if (string == ""):
            pop_projection_matrix()
            return

        lines = string.split ("\n")

        glPushAttrib(GL_LIST_BIT | GL_CURRENT_BIT  | GL_ENABLE_BIT | GL_TRANSFORM_BIT)
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glListBase(self._list_base)
        modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        r = self._color[0]
        g = self._color[1]
        b = self._color[2]
        glColor3f(r, g, b)

        # //This is where the text display actually happens.
        # //For each line of text we reset the modelview matrix
        # //so that the line's text will start in the correct position.
        # //Notice that we need to reset the matrix, rather than just translating
        # //down by h. This is because when each character is
        # //draw it modifies the current matrix so that the next character
        # //will be drawn immediatly after it.  
        for i in xrange (len (lines)):
            line = lines [i]

            glPushMatrix ()
            glLoadIdentity ()
            glTranslatef (self._x, self._y - h*i, 0);
            glMultMatrixf (modelview_matrix);
            glCallLists (line)
            glPopMatrix()

        glPopAttrib()
        # leave coordinate matrix
        pop_projection_matrix()

    def release(self):
        """ Release the gl resources for this Face."""
        if (self._allocated):
            # Free up the glTextures and the display lists for our face
            glDeleteLists ( self._list_base, 128);
            for ID in self.textures:
                glDeleteTextures (ID);
            # Extra defensive. Clients that continue to try and use this object
            # will now trigger exceptions.
            self.list_base = None
            self._allocated = False
        return

    def __del__(self):
        """ Python destructor for when no more refs to this Face object """
        self.release()
        return

    def draw_AABB(self):
        # Hack to be able to keep textboxes in the object list
        # (this function is called to draw the axis-aligned bounding boxes
        # of all other objects.)
        pass

def next_p2 (num):
    """ If num isn't a power of 2, will return the next higher power of two """
    rval = 1
    while (rval<num):
        rval <<= 1
    return rval

def make_dlist (ft, ch, list_base, tex_base_list):
    """ Given an integer char code, build a GL texture into texture_array,
        build a GL display list for display list number display_list_base + ch.
        Populate the glTexture for the integer ch and construct a display
        list that renders the texture for ch.
        Note, that display_list_base and texture_base are supposed
        to be preallocated for 128 consecutive display lists and and 
        array of textures.
    """

    # //The first thing we do is get FreeType to render our character
    # //into a bitmap.  This actually requires a couple of FreeType commands:
    # //Load the Glyph for our character.
    # //Move the face's glyph into a Glyph object.
    # //Convert the glyph to a bitmap.
    # //This reference will make accessing the bitmap easier
    # - This is the 2 dimensional Numeric array

    # Use our helper function to get the widths of
    # the bitmap data that we will need in order to create
    # our texture. L for antialiasing.
    glyph = ft.getmask (chr (ch), mode = "L")
    glyph_width, glyph_height = glyph.size 
    # We are using PIL's wrapping for FreeType. As a result, we don't have 
    # direct access to glyph.advance or other attributes, so we add a 1 pixel pad.
    width = next_p2 (glyph_width + 1)
    height = next_p2 (glyph_height + 1)

    # Here we fill in the data for the expanded bitmap.
    # Notice that we are using two channel bitmap (one for
    # luminocity and one for alpha), but we assign
    # both luminocity and alpha to the value that we
    # find in the FreeType bitmap. 
    expanded_data = ""
    for j in xrange (height):
        for i in xrange (width):
            if (i >= glyph_width) or (j >= glyph_height):
                value = chr (0)
                # two channel data
                expanded_data += value
                expanded_data += value
            else:
                value = chr (glyph.getpixel ((i, j)))
                expanded_data += value
                expanded_data += value

    # -------------- Build the gl texture ------------

    # Now we just setup some texture paramaters.
    ID = glGenTextures(1)
    tex_base_list[ch] = ID
    glBindTexture(GL_TEXTURE_2D, ID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    border = 0
    # Here we actually create the texture itself, notice
    # that we are using GL_LUMINANCE_ALPHA to indicate that
    # we are using 2 channel data.
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, width, height,
        border, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE, expanded_data )

    # With the texture created, we don't need to expanded data anymore
    expanded_data = None

    # --- Build the gl display list that draws the texture for this character ---

    # So now we can create the display list
    glNewList (list_base + ch, GL_COMPILE)

    if (ch == ord (" ")):
        glyph_advance = glyph_width
        glTranslatef(glyph_advance, 0, 0)
        glEndList()
    else:

        glBindTexture (GL_TEXTURE_2D, ID)

        glPushMatrix()

        # Now we need to account for the fact that many of
        # our textures are filled with empty padding space.
        x=float (glyph_width) / float (width)
        y=float (glyph_height) / float (height)

        # Here we draw the texturemaped quads.
        # The bitmap that we got from FreeType was not 
        # oriented quite like we would like it to be,
        # so we need to link the texture to the quad
        # so that the result will be properly aligned.
        glBegin(GL_QUADS)
        glTexCoord2f(0,0), glVertex2f(0,glyph_height)
        glTexCoord2f(0,y), glVertex2f(0,0)
        glTexCoord2f(x,y), glVertex2f(glyph_width,0)
        glTexCoord2f(x,0), glVertex2f(glyph_width, glyph_height)
        glEnd()
        glPopMatrix()

        # Because the advance value is hidden from we will advance
        # the "pen" based upon the rendered glyph's width. This is imperfect.
        glTranslatef(glyph_width + 0.75, 0, 0)

        glEndList()

    return

# A fairly straight forward function that pushes
# a projection matrix that will make object world 
# coordinates identical to window coordinates.
def pushScreenCoordinateMatrix():
    glPushAttrib(GL_TRANSFORM_BIT)
    viewport = glGetIntegerv(GL_VIEWPORT)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(viewport[0],viewport[2],viewport[1],viewport[3])
    glPopAttrib()
    return

# Pops the projection matrix without changing the current
# MatrixMode.
def pop_projection_matrix():
    glPushAttrib(GL_TRANSFORM_BIT)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glPopAttrib()
    return


