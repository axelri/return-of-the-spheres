from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.shadow import *
from OpenGL.GL.ARB.depth_texture import *
from OpenGL.GL.ARB.transpose_matrix import *
from math_classes.vectors import Vector

# TODO: Add other attributes to the light, such as color, direction,
# angle of the spreading light etc.

class Light:
    ''' A class to hold Light objects, contains the OpenGL-index
    for the light and the properties of the light. '''
    
    def __init__(self, light_index, pos, is_spotlight = False,
                 ambient = [0.2, 0.2, 0.2, 1.0],
                 diffuse = [0.8, 0.8, 0.8, 1.0],
                 specular = [0.5, 0.5, 0.5, 1.0],
                 shadow_color = [0.2, 0.2, 0.2, 1.0]):
        ''' Initializes the Light object, sets the OpenGL-index
        of the light and its starting position.

        Input:  light_index: An OpenGL constant referencing the
                    light in OpenGL.
                pos: A vector describing the position of the light. '''

        self._light_index = light_index
        self._pos = pos
        self._is_spotlight = False
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular
        self._shadow_color = shadow_color

        glEnable(self._light_index)

        self._setup()

        # TODO: Add spotlight properties like cutoff etc.

    def move(self):
        ''' Moves the light to its current position '''
        # The last part (+[float(not self._is_spotlight)])
        # is there because the fourth element in the position
        # is used by OpenGL to define if it is a spotlight
        # or not: 1.0 means no spotlight, 0.0 means spotlight.
        glLightfv(self._light_index, GL_POSITION,
                  self._pos.value+tuple([float(not self._is_spotlight)]))

    def _setup(self):
        ''' Sets the wanted properties of the light in OpenGL '''
        glLightfv(self._light_index, GL_AMBIENT, self._ambient)
        glLightfv(self._light_index, GL_DIFFUSE, self._diffuse)
        glLightfv(self._light_index, GL_SPECULAR, self._specular)
        self.move()

    def disable(self):
        ''' Disables the light '''
        glDisable(self._light_index)

    def enable(self):
        glEnable(self._light_index)

    def change_diffuse_color(self,newcolor):
        self.diffuse_color = newcolor
        glLightfv(self._light_index,GL_AMBIENT,[0.0,0.0,0.0,1.0])
        glLightfv(self._light_index,GL_DIFFUSE,[self.diffuse_color[0], 
                    self.diffuse_color[1],self.diffuse_color[2],1.0])
    def change_color(self,newcolor):
        self.color = newcolor
        glLightfv(self._light_index,GL_SPECULAR,[self.color[0],self.color[1],
                            self.color[2],1.0])

    def draw_pos(self):
        ''' Shows the position and color of the light by drawing 
            a small point. '''

        # Check if they are enabled now in order to
        # be able to restore everything to the previous state
        lighting_enabled = glGetBooleanv(GL_LIGHTING)
        texturing_enabled = glGetBooleanv(GL_TEXTURE_2D)
        current_color = glGetFloatv(GL_CURRENT_COLOR)

        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)

        # Draw a point at the light's position
        # TODO: Make smaller when looking from a distance.
        glPointSize(10)
        glColor4fv(self._diffuse)
        glBegin(GL_POINTS)
        glVertex3f(*self._pos.value)   #pos[0], pos[1], pos[2])
        glEnd()

        # Restore everything we changed
        if lighting_enabled:
            glEnable(GL_LIGHTING)
        if texturing_enabled:
            glEnable(GL_TEXTURE_2D)
        glColor4fv(current_color)

    ### Getters

    def get_light_index(self):
        return self._light_index

    def get_pos(self):
        return self._pos

    def get_ambient(self):
        return self._ambient

    def get_diffuse(self):
        return self._diffuse
    
    def get_specular(self):
        return self._specular

    def is_spotlight(self):
        return self._is_spotlight

    ### Setters

    def set_pos(self, pos):
        self._pos = pos
        self.move()

    def add_pos(self, pos):
        self._pos += pos
        self.move()

    def set_ambient(self, ambient):
        self._ambient = ambient
        self._setup()

    def set_diffuse(self, diffuse):
        self._diffuse = diffuse
        self._setup()

    def set_specular(self, specular):
        self._specular = specular
        self._setup()

# The code for shadow rendering is almost entirely copied from
# http://geometrian.com/programming/projects/index.php?project=glLib
GLLIB_SHADOW_MAP1 = 5
GLLIB_SHADOW_MAP2 = 6
GLLIB_SHADOW_MAP3 = 7
GLLIB_SHADOW_MAP4 = 8
GLLIB_SHADOW_MAP5 = 9
GLLIB_SHADOW_MAP6 = 10
GLLIB_SHADOW_MAP7 = 11
GLLIB_SHADOW_MAP8 = 12

def init_shadows(shadowmaps=[[256,0]]):
    global ShadowMaps
    ShadowMaps = []
    for newmap in shadowmaps:
        ShadowMap = resize_shadowmap(newmap[0],newmap[1])
        ShadowMaps.append([ShadowMap,newmap[0],None])

def resize_shadowmap(newresolution,antialiaslevel=0):
    texturing = glGetBooleanv(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    ShadowMapSize = newresolution
    mods = ["depthtex","clamp"]
    if   antialiaslevel == 0: pass
    elif antialiaslevel == 1: mods.append("filter")
    elif antialiaslevel == 2: mods.append("mipmap")
    elif antialiaslevel == 3: mods.append("mipmap"); mods.append("filter")
    elif antialiaslevel == 4: mods.append("mipmap blend")
    elif antialiaslevel == 5: mods.append("mipmap blend"); mods.append("filter")
    ShadowMapTexture = glLibTexture(None,mods,[ShadowMapSize,ShadowMapSize])
    if not texturing: glDisable(GL_TEXTURE_2D)
    return ShadowMapTexture

def initialize_shadowmap(shadowmap,lightpos,lightfocus=(0,0,0),lightviewangle=100,near=0.1,far=100.0,offset=0.5):
    ShadowMap = ShadowMaps[shadowmap-GLLIB_SHADOW_MAP1]
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(lightviewangle,1.0,near,far)
    LightProjectionMatrix = glGetFloatv(GL_PROJECTION_MATRIX)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(lightpos[0],lightpos[1],lightpos[2],
              lightfocus[0],lightfocus[1],lightfocus[2],
              0.0,1.0,0.0)
    LightViewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    #Use viewport the same size as the shadow map
    
    glViewport(0, 0, ShadowMap[1], ShadowMap[1])
    glPolygonOffset(offset,offset)
    glEnable(GL_POLYGON_OFFSET_FILL) 
    #eval projection matrix
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadMatrixf([[0.5,0.0,0.0,0.0],
                   [0.0,0.5,0.0,0.0],
                   [0.0,0.0,0.5,0.0],
                   [0.5,0.5,0.5,1.0]])
    glMultMatrixf(LightProjectionMatrix)
    glMultMatrixf(LightViewMatrix)
    TextureMatrix = glGetFloatv(GL_TRANSPOSE_MODELVIEW_MATRIX)
    ShadowMap[2] = TextureMatrix
    glPopMatrix()

def create_shadowmap(shadowmap):
    ShadowMap = ShadowMaps[shadowmap-GLLIB_SHADOW_MAP1]
    #Write texture into texture obj
    texturing = glGetBooleanv(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ShadowMap[0])
    glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 0, 0, ShadowMap[1], ShadowMap[1])
    glDisable(GL_POLYGON_OFFSET_FILL)
    if not texturing: glDisable(GL_TEXTURE_2D)

def enable_shadowshading():
    glBlendFunc(GL_SRC_COLOR,GL_DST_COLOR)
    glEnable (GL_BLEND)

def disable_shadowshading():
    glDisable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def render_shadow_comparison(shadowmap):
    global Texturing
    Texturing = glGetBooleanv(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glEnable(GL_TEXTURE_GEN_R)
    glEnable(GL_TEXTURE_GEN_Q)
    ShadowMap = ShadowMaps[shadowmap-GLLIB_SHADOW_MAP1]
    TextureMatrix = ShadowMap[2]
    #Evaluate where to draw shadows using ARB extension        
    glBindTexture(GL_TEXTURE_2D, ShadowMap[0])
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_S, GL_EYE_PLANE, TextureMatrix[0])
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_T, GL_EYE_PLANE, TextureMatrix[1])
    glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_R, GL_EYE_PLANE, TextureMatrix[2])
    glTexGeni(GL_Q, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
    glTexGenfv(GL_Q, GL_EYE_PLANE, TextureMatrix[3])
    #Enable shadow comparison
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE_ARB, GL_COMPARE_R_TO_TEXTURE_ARB)
    #Shadow comparison should be True (in shadow) if r > texture
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC_ARB, GL_GREATER)
    #Shadow comparison should generate an INTENSITY result
    glTexParameteri(GL_TEXTURE_2D, GL_DEPTH_TEXTURE_MODE_ARB, GL_INTENSITY)
    #Set alpha test to discard false comparisons
    glAlphaFunc(GL_EQUAL, 1.0)

def reset_OpenGL_parameters():
    #reset gl params after comparison
##    if not Texturing: glDisable(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_TEXTURE_GEN_R)
    glDisable(GL_TEXTURE_GEN_Q)

# This part should be moved, is here since I didn't know which parts
# were needed

def glLibTexturing(value):
    if value:glEnable(GL_TEXTURE_2D)
    else:glDisable(GL_TEXTURE_2D)
def glLibTexture(surface,filters=[],size="automatic"):
    if type(surface) == type(""):
        surface = pygame.image.load(os.path.join(*surface.split("/"))).convert_alpha()
    if surface == None:
        data = surface
    else:
        data = pygame.image.tostring(surface,"RGBA",True)
    if size == "automatic":
        width,height = surface.get_size()
    else:
        width = size[0]
        height = size[1]
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texture)
    #Format
    InternalFormat = GL_RGBA
    if "depthtex" in filters:
        InternalFormat = GL_DEPTH_COMPONENT
    #Mag filter
    if "filter" in filters: glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    else:                   glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    #Min filter
    if "mipmap" in filters:
        if "mipmap blend" in filters:
            if "filter" in filters: mipmap_param = GL_LINEAR_MIPMAP_LINEAR
            else:                   mipmap_param = GL_NEAREST_MIPMAP_LINEAR
        else:
            if "filter" in filters: mipmap_param = GL_LINEAR_MIPMAP_NEAREST
            else:                   mipmap_param = GL_NEAREST_MIPMAP_NEAREST
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,mipmap_param)
        glPixelStoref(GL_UNPACK_ALIGNMENT,1)
        gluBuild2DMipmaps(GL_TEXTURE_2D,3,width,height,InternalFormat,GL_UNSIGNED_BYTE,data)
    else:
        if "filter" in filters: glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        else:                   glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D,0,InternalFormat,width,height,0,InternalFormat,GL_UNSIGNED_BYTE,data)
    #Misc.
    if "clamp" in filters:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    #Return
    return texture
def glLibSelectTexture(texture):
    glBindTexture(GL_TEXTURE_2D,texture)