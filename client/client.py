import character
from states import *
import sys

c = character.Character()

def main():
    print("It's {}! Welcome to {}, delicious friend!".format(c.info['name'], c.user['area']['name']))

    switch = {State.Story: Story,
              State.Messages: Messages,
              State.Myself: Myself,
              State.Possessions: Possessions,
              State.Bazaar: Bazaar,
              State.Fate: Fate,
              State.Plans: Plans}

    while True:
        state = switch.get(c.get_state(), lambda x: sys.exit('Error: unknown state {}'.format(c.get_state())))
        state(c)

if __name__ == '__main__':
    main()
