#!/usr/bin/env python3
import arrow
import netrc
import requests

api = 'https://api.fallenlondon.com/api/{}'

class Character:
    def __login(self):
        if self.s.get(api.format('login/user')).status_code == 200:
            return True
        try:
            login = netrc.netrc().authenticators('fallenlondon')
            email = login[0]
            pw = login[2]
            del login
        except FileNotFoundError:
            from getpass import getpass
            email = input('Email: ')
            pw = getpass('Password: ')

        r = self.s.post(api.format('login'), data={'email': email, 'password': pw})

        del email, pw

        if r.status_code != 200:
            return False
        
        self.s.headers.update({'Authorization': 'Bearer {}'.format(r.json()['Jwt'])})
        return True

    def __init__(self):
        self.s = requests.Session()
        
        self.__login()
        
        r = self.s.get(api.format('login/user'))
        self.user = r.json()
        
        r = self.s.get(api.format('character/myself'))
        self.info = r.json()['Character']
        self.qualities = r.json()['Possessions']
        
        r = self.s.get(api.format('outfit'))
        self.outfit = r.json()
        
        r = self.s.get(api.format('character/possessions'))
        self.items = r.json()['Possessions']
        
        self.update_sidebar()
        self.update_status()

    def time_to_refresh(self):
        self.update_sidebar()
        print(str(arrow.get(self.sidebar['NextActionsAt']) - arrow.now()).split('.')[0])

    def update_sidebar(self):
        r = self.s.get(api.format('character/sidebar'), params={'full': False})
        self.sidebar = r.json()

    def get_actions(self):
        self.update_sidebar()
        return (self.sidebar.get('Actions', -1), self.sidebar.get('ActionBankSize', None))

    def update_cards(self):
        r = self.s.get(api.format('opportunity'))
        self.cards = r.json()

    def get_deck(self):
        self.update_cards()
        return (self.cards['EligibleForCardsCount'], self.cards['MaxDeckSize'])

    def get_cards(self):
        self.update_cards()
        return self.cards['DisplayCards']

    def draw(self):
        if len(self.get_cards()) < self.cards['MaxHandSize'] and self.cards['EligibleForCardsCount'] > 0:
            r = self.s.post(api.format('opportunity/draw'))
            self.cards = r.json()

    def discard(self, cid):
        assert any(card['EventId'] == cid for card in self.get_cards())
        r = self.s.post(api.format(f'opportunity/discard/{cid}'))
        return True

    def update_status(self):
        r = self.s.post(api.format('storylet'))
        self.status = r.json()

    def get_status(self):
        return self.status

    def get_phase(self):
        return self.status['Phase']

    def get_storylets(self):
        self.update_status()
        return self.status['Storylets']

    def begin_storylet(self, sid):
        self.update_status()
        if 'In' not in self.get_phase():
            return False
        r = self.s.post(api.format('storylet/begin'), data={'eventId': sid})
        self.status = r.json()
        return True

    bs = begin_storylet

    def go_back(self):
        self.update_status()
        if 'In' not in self.get_phase():
            return True
        if not self.status['Storylet']['CanGoBack']:
            return False
        r = self.s.post(api.format('storylet/goback'))
        self.status = r.json()
        return True

    def print_branches(self):
        self.update_status()
        if 'In' not in self.get_phase():
            return False
        for branch in self.status['Storylet']['ChildBranches']:
            print(f"{'!' if branch['IsLocked'] else ' '}{branch['Id']}: {branch['Name']}")

    pb = print_branches

    def choose_branch(self, bid): # TODO check autofire cards
        self.update_status()
        if 'In' not in self.get_phase():
            return False
        assert any([branch['Id'] == bid for branch in self.status['Storylet']['ChildBranches']])
        r = self.s.post(api.format('storylet/choosebranch'), data={'branchId': bid})
        self.status = r.json()
        return True

    cb = choose_branch

    def print_result(self):
        if self.get_phase() != 'End':
            return False
        print(f"Name: {self.status['EndStorylet']['Event']['Name']}")
        print(f"Desc: {self.status['EndStorylet']['Event']['Description']}\n")

        for message in self.status['Messages']['DefaultMessages']:
            print(message['Message'])

    pr = print_result

    def print_cards(self):
        for card in self.get_cards():
            print(f"{card['EventId']}: {card['Name']}")

    pc = print_cards

    def print_storylets(self):
        for storylet in self.get_storylets():
            print(f"{storylet['Id']}: {storylet['Name']}")

    ps = print_storylets
