#!/usr/local/bin/python3

from datetime import datetime
import os
import random
import sys
import time

from character import Character

print('current time {}'.format(datetime.now()))

delay = random.randint(0, 30*60)

print('sleeping for {} secs...'.format(delay))

sys.stdout.flush()

#time.sleep(delay)

c = Character()

assert c.get_phase() == 'In' and c.status['storylet']['id'] == 284781

actions = c.get_actions()

print('actions: {}/{}'.format(actions[0], actions[1]))

for x in range(actions[0] // 4):
    c.cb(211145)
    c.pr()

print('done')
