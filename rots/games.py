import shapes
import players
from graphics import lights
from text import TextBox

class Game():
    ''' A class containing all the objects in the game '''
    def __init__(self, player, objectList, sceneList, lightList, textList, camera, clock, debug = False):
        # TODO: Use the Player object from fluffy instead?
        assert isinstance(player, players.Player), \
               'Input must be a Player object'
        assert isinstance(objectList, list), 'Input must be a list'
        assert isinstance(sceneList, list), 'Input must be a list'
        assert isinstance(lightList, list), 'Input must be a list'
        if __debug__:
            # for item in objectList:
                # assert isinstance(item, shapes.Shape), \
                       # 'All items in objectList must be Shape objects'
            for item in sceneList:
                assert isinstance(item, shapes.Shape), \
                       'All items in sceneList must be Shape objects'
            for item in lightList:
                assert isinstance(item, lights.Light), \
                       'All items in lightList must be Light objects'
        self._player = player
        self._objectList = objectList
        self._sceneList = sceneList
        self._lightList = lightList
        self._textList = textList
        self._camera = camera
        self._clock = clock
        self.debug = debug
        # TODO: This should describe the game object in
        # the saved state files (levels):
        # Player = Profile + associated shape
        # objectList, sceneList
        # lighting objects
        # level constants (gravity etc), hashmap

        # TODO: Add more things to the debug screen, move textboxes to better positions
        # (perhaps use pygame.display.Info().current_w /-h to put the text relative
        # the screen's border?)
        
        # Performance
        self._debug_fps = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 150, [1,0,0])
        self._debug_time_used = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 100, [1,0,0])
        
        # Player properties
        self._debug_player_pos = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 350, [1,0,0])
        self._debug_player_vel = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 300, [1,0,0])
        self._debug_player_colliding = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 250, [1,0,0])

        self._debugList = [self._debug_fps, self._debug_time_used, self._debug_player_pos, self._debug_player_vel,
                            self._debug_player_colliding]

    def update_debug_screen(self):
        # Performance
        self._debug_fps.set_string("FPS: " + str(self._clock.get_fps()))
        self._debug_time_used.set_string("Time used last frame [ms]: " + str(self._clock.get_rawtime()))
        
        # Player properties
        self._debug_player_pos.set_string("Player pos: " + str(self._player.get_shape().get_pos()))
        self._debug_player_vel.set_string("Player vel: " + str(self._player.get_shape().get_vel()))
        self._debug_player_colliding.set_string("Player colliding: " + str(self._player.colliding))

    def get_objects(self):
        return self._player, self._objectList, self._sceneList,\
               self._lightList, self._textList, self._camera
