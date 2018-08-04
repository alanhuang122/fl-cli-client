from enum import Enum

class State(Enum):
    Story = 0
    Messages = 1
    Myself = 2
    Possessions = 3
    Bazaar = 4
    Fate = 5
    Plans = 6

def clean(text):
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

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
