#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
import fileinput
from getpass import getpass
import netrc
import os
import requests
import stat
#from states import *
import sys
import types

api = 'https://api.fallenlondon.com/api/{}'

class Character:
    def __login(self):
        if self.s.get(api.format('login/user')).status_code == 200:
            return True
        #print('logging in')
        try:
            login = netrc.netrc().authenticators('fallenlondon')

            r = self.s.post(api.format('login'), data={'email': login[0], 'password': login[2]})

            if r.status_code == 401:
                print('Invalid saved credentials!')
                raise Exception
        except:
            while True:
                email = input('Email: ')
                pw = getpass('Password: ')

                r = self.s.post(api.format('login'), data={'email': email, 'password': pw})

                if r.status_code == 401:
                    choice = input('Invalid credentials. Retry? (y/n) ')
                    if choice.lower().startswith('y'):
                        continue
                    else:
                        sys.exit("Login failed.")
                elif r.status_code == 200:
                    break

        try:
            email, pw
            while True:
                choice = input('Do you want to save these credentials? (y/n): ')
                if choice.lower().startswith('y'):
                    home = os.path.expanduser('~')
                    path = os.path.join(home, '.netrc')
                    if os.path.isfile(path): # replace or append
                        append = True
                        for line in fileinput.input(path, inplace=True):
                            if line.startswith('machine fallenlondon'):
                                print("machine fallenlondon login {} password {}".format(email, pw))
                                append = False
                            else:
                                print(line, end='')
                        if append:
                            with open(path, 'a') as f:
                                f.write("machine fallenlondon login {} password {}\n".format(email, pw))
                    elif not os.path.exists(path):
                        with open(path, 'x') as f:
                            f.write("machine fallenlondon login {} password {}\n".format(email, pw))
                        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
                    else:
                        print('Error trying to access {}'.format(path))
                    break
                elif choice.lower().startswith('n'):
                    break
        except NameError:
            pass

        self.s.headers.update({'Authorization': 'Bearer {}'.format(r.json()['jwt'])})
        return True

    def __init__(self):
        self.s = requests.Session()

        self.__login()

        r = self.s.get(api.format('login/user'))
        self.user = r.json()
        #self.state = State.Story

        self.info = None
        self.items = None
        self.qualities = None
        self.outfit = None

        self.update_sidebar()
        self.update_status()
        self.update_items()
        self.update_qualities()

    def logout(self):
        self.__api_post('login/logout')
        self.s = requests.Session()

    def __api_get(self, endpoint, *args, **kwargs):
        r = self.s.get(api.format(endpoint), *args, **kwargs)
        if r.status_code != 200:
            self.__login()
            r = self.s.get(api.format(endpoint), *args, **kwargs)
            if r.status_code != 200:
                raise ConnectionError
        return r

    def __api_post(self, endpoint, *args, **kwargs):
        r = self.s.post(api.format(endpoint), *args, **kwargs)
        if r.status_code != 200:
            self.__login()
            r = self.s.post(api.format(endpoint), *args, **kwargs)
            if r.status_code != 200:
                raise ConnectionError
        return r

#    def get_state(self):
#        return self.state

#    def set_state(self, state):
#        if isinstance(state, State):
#            self.state = state

    def time_to_refresh(self):
        self.update_sidebar()
        now = datetime.strptime(self.sidebar['currentTime'].rsplit('.')[0], '%Y-%m-%dT%H:%M:%S')
        later = datetime.strptime(self.sidebar['nextActionsAt'].rsplit('.')[0], '%Y-%m-%dT%H:%M:%S')
        print(later - now)

    def update_items(self):
        r = self.__api_get('character/possessions')
        self.items = r.json()['possessions']

    def get_items(self):
        return self.items

    def update_qualities(self):
        r = self.__api_get('character/myself')
        self.info = r.json()['character']
        self.qualities = r.json()['possessions']

    def get_qualities(self):
        return self.qualities

    def get_outfits(self):
        return self.info['outfits']

    def equip_outfit(self, id):
        r = self.__api_post('outfit/change/{}'.format(id))
        self.outfit = r.json()

    def update_equipment(self):
        r = self.__api_get('outfit')
        self.outfit = r.json()

    def get_equipment(self):
        return self.outfit

    def update_sidebar(self):
        r = self.__api_get('character/sidebar', params={'full': True})
        self.sidebar = r.json()

    def get_sidebar(self):
        return self.sidebar

    def get_actions(self):
        update_sidebar()
        return (self.sidebar.get('actions', -1), self.sidebar.get('actionBankSize', None))

    def update_cards(self):
        r = self.__api_get('opportunity')
        self.cards = r.json()

    def get_deck(self):
        return (self.cards['eligibleForCardsCount'], self.cards['maxDeckSize'])

    def get_cards(self):
        return self.cards['displayCards']

    def draw(self):
        if len(self.get_cards()) < self.cards['maxHandSize'] and self.cards['eligibleForCardsCount'] > 0:
            r = self.__api_post('opportunity/draw')
            self.cards = r.json()

    def discard(self, cid):
        assert any(card['eventId'] == cid for card in self.get_cards())
        r = self.__api_post('opportunity/discard/{}'.format(cid))
        return True

    def update_status(self):
        r = self.__api_post('storylet')
        self.status = r.json()

    def get_status(self):
        return self.status

    def get_phase(self):
        return self.status['phase']

    # TODO not all fields are always present; depends on phase

    def get_storylets(self):
        return self.status['storylets']

    def get_storylet(self):
        return self.status['storylet']

    def begin_storylet(self, sid):
        self.update_status()
        if 'In' in self.get_phase():
            return False
        r = self.__api_post('storylet/begin', data={'eventId': sid})
        self.status = r.json()
        return True

    bs = begin_storylet

    def go_back(self):
        self.update_status()
        if 'In' not in self.get_phase():
            return True
        if not self.status['storylet']['canGoBack']:
            return False
        r = self.__api_post('storylet/goback')
        self.status = r.json()
        return True

    def get_branches(self):
        if 'In' not in self.get_phase():
            return False
        return self.status['storylet']['childBranches']

    def print_branches(self):
        if 'In' not in self.get_phase():
            return False
        for branch in self.status['storylet']['childBranches']:
            print("{}{}: {}".format('!' if branch['isLocked'] else ' ', branch['id'], branch['name']))

    pb = print_branches

    def choose_branch(self, bid): # TODO check autofire cards
        self.update_status()
        if 'In' not in self.get_phase():
            return False
        assert any([branch['id'] == bid for branch in self.status['storylet']['childBranches']])
        r = self.__api_post('storylet/choosebranch', data={'branchId': bid})
        self.status = r.json()
        return True

    cb = choose_branch

    def print_result(self):
        if self.get_phase() != 'End':
            return False
        print("Name: {}".format(self.status['endStorylet']['event']['name']))
        print("Desc: {}".format(self.status['endStorylet']['event']['description']))

        for message in self.status['messages']['defaultMessages']:
            print(message['message'])

    pr = print_result

    def print_cards(self):
        for card in self.get_cards():
            print("{card['eventId']}: {card['name']}".format(card=card))

    pc = print_cards

    def print_storylets(self):
        for storylet in self.get_storylets():
            print("{storylet['id']}: {storylet['name']}".format(storylet=storylet))

    ps = print_storylets
