import os
import pygame

def load_sound(file_name):

    if not pygame.mixer:
        print 'Warning: Unable to load module pygame.mixer'
        return None_sound()

    fullname = os.path.join('sound/sound_data', file_name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Pygame error: ', message
        print 'Cannot load sound:', file_name
        return None_sound()
    return sound

class None_sound:
    def play(self):
        pass