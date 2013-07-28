import os
import pygame


def load_sound(file_name):
    
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()

    fullname = os.path.join('sound/sound_data', file_name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', file_name
        raise SystemExit, message
    return sound
