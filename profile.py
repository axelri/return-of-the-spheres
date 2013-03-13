from pygame.locals import *
class Profile:
    ''' The current profile containing player preferences.'''

    def __init__(self, visual, control, debug):
        assert isinstance(visual, dict)
        assert isinstance(control, dict)
        assert isinstance(debug, dict)

        self._visual = visualDict
        self._control = controlDict
        self._debug = debugDict

    def current_width(self):
        return 0

    def current_heght(self):
        return 0

    def _convert_to_pygame_keys(self, keys):
        ''' Format according to the pygame constant naming.
        The fetch the actual constant value from the local variable pool.'''
        # single letter keys are denoted 'K_<letter>', whereas all
        # the other keys are denoted 'K_<KEY_NAME>'
        if len(keys[0]) == 1:
            keys[0] = keys[0].lower()
        else:
            keys[0] = keys[0].upper()
        if len(keys[1]) == 1: 
            keys[1] = keys[1].lower()
        else:
            keys[1] = keys[1].upper()


        keys = ['K_' + x for x in keys]
        return [locals()[keys[0]], locals()[keys[1]]

    def get_forward_keys(self):
        keys = self._control['forward']

        return _convert_to_pygame_keys(keys)

    def get_backward_keys(self):
        keys = self._control['backward']

        return _convert_to_pygame_keys(keys)

    def get_right_keys(self):
        keys = self._control['right']

        return _convert_to_pygame_keys(keys)
    
    def get_left_keys(self):
        keys = self._control['left']

        return _convert_to_pygame_keys(keys)

    # TODO: Finish setters, write unit tests
    def set_forward_keys(self, keys):
        return 'a'

    def set_backward_keys(self, keys):
        return 'a'

    def set_right_keys(self, keys):
        return 'a'
    
    def set_left_keys(self, keys):
        return 'a'
