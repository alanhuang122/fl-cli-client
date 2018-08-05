import character
from states import *
import sys

c = character.Character()

def main():
    s = State.Story
    print("It's {}! Welcome to {}, delicious friend!".format(c.info['Name'], c.user['Area']['Name']))

    switch = {State.Story: Story,
              State.Messages: Messages,
              State.Myself: Myself,
              State.Possessions: Possessions,
              State.Bazaar: Bazaar,
              State.Fate: Fate,
              State.Plans: Plans}

    while True:
        s = switch.get(s, lambda: sys.exit('Error: unknown state {}'.format(s)))()

if __name__ == '__main__':
    main()
