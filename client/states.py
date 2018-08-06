from enum import Enum
#import html2text

#texter = html2text.HTML2Text()
#texter.body_width = 0

class State(Enum):
    Story = 0
    Messages = 1
    Myself = 2
    Possessions = 3
    Bazaar = 4
    Fate = 5
    Plans = 6

def choose_option(options, header=None, prompt=None, display=None):
    if header:
        print(header)
    for i in range(len(options)):
        if display:
            print('{}: {}'.format(i+1, display[i]))
        else:
            print('{}: {}'.format(i+1, options[i]))
    while True:
        try:
            if prompt:
                choice = int(input(prompt))
            else:
                choice = int(input('Type the number of your choice: '))
            if choice > len(options) or choice < 1:
                print("Invalid input.")
                continue
            return options[choice-1]
        except:
            print("Invalid input.")
            continue

def choose_state():
    states = list(State)
    display = [str(s).split('.')[1] for s in states]
    return choose_option(states, prompt='Type the number of the tab you want to switch to: ', display=display)

def Story(c):
    def Available(c):
        # print deck, print cards, print storylets
        raise NotImplementedError

    def In(c):
        storylet = c.get_storylet()
        print('Storylet: {}'.format(storylet['Name']))
        print('Description: {}'.format(texter.handle(storylet['Description'])))
        # print branches, go back, switch state
        branches = c.get_branches()
        branch = choose_option(branches, header='Branches:', prompt='Choose a branch: ', display=[x['Name'] for x in branches])
        raise NotImplementedError

    def End(c):
        # print result, update phase, try again / continue?
        raise NotImplementedError

    switch = {'Available': Available,
              'In': In,
              'InItemUse': In,
              'End': End}

    while True:
        switch.get(c.get_phase(), lambda x: sys.exit('Error: unknown phase {}'.format(c.get_phase())))(c)
#        if
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
