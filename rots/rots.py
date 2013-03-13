import traceback
import sys

def main():
    ''' Main routine of the game.'''

    while true:
        # do main routine
        break

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
