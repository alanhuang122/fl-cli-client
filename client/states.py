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

def Story(c):
    # Maybe usable by more things
    def clean(text):
        tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

        # Remove well-formed tags, fixing mistakes by legitimate users
        clean = tag_re.sub('', text)

        # Clean up anything else by escaping
        return cgi.escape(clean)

    def Available(c):
        # print deck, print cards, print storylets
        raise NotImplementedError

    def In(c):
        # print branches, go back, switch state
        branches = c.get_branches()
        raise NotImplementedError

    def End(c):
        # print result, update phase
        raise NotImplementedError

    switch = {'Available': Available,
              'In': In,
              'InItemUse': In,
              'End': End}

    while True:
        switch.get(c.get_phase(), lambda: sys.exit('Error: unknown phase {}'.format(c.get_phase())))
        # if user has switched phases:
        #     return

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
