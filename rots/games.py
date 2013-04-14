import shapes
import players
from graphics import lights

class Game():
    ''' A class containing all the objects in the game '''
    def __init__(self, player, objectList, sceneList, lightList):
        # TODO: Use the Player object from fluffy instead?
        assert isinstance(player, players.Player), \
               'Input must be a Player object'
        assert isinstance(objectList, list), 'Input must be a list'
        assert isinstance(sceneList, list), 'Input must be a list'
        assert isinstance(lightList, list), 'Input must be a list'
        if __debug__:
            for item in objectList:
                assert isinstance(item, shapes.Shape), \
                       'All items in objectList must be Shape objects'
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
        # TODO: This should describe the game object in
        # the saved state files (levels):
        # Player = Profile + associated shape
        # objectList, sceneList
        # lighting objects
        # level constants (gravity etc), hashmap

    def get_objects(self):
        return self._player, self._objectList, self._sceneList, self._lightList
