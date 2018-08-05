from enum import Enum

class State(Enum):
    Story = 0
    Messages = 1
    Myself = 2
    Possessions = 3
    Bazaar = 4
    Fate = 5
    Plans = 6

def choose_state():
    states = list(State)
    for i in range(len(states)):
        print('{}: {}'.format(i+1, str(states[i]).split('.')[1]))
    while True:
        try:
            choice = int(input('Type the number of the tab you want to switch to: '))
            if choice > len(states) or choice < 1:
                print("Invalid input.")
                continue
            return State(choice - 1)
        except:
            print("Invalid input.")
            continue

    # Remove well-formed tags, fixing mistakes by legitimate users
    clean = tag_re.sub('', text)

    # Clean up anything else by escaping
    return cgi.escape(clean)

def Story():
    raise NotImplementedError

def Messages():
    raise NotImplementedError

def Myself():
    raise NotImplementedError

def Possessions():
    raise NotImplementedError

def Bazaar():
    raise NotImplementedError

def Fate():
    raise NotImplementedError

def Plans():
    raise NotImplementedError
