#!/usr/bin/env python

from clickerheroes import *
from gamewindow import *
from gamestatewatch import *
from display import *

from time import *
from enum import Enum

sleep(1)

hh = SuspendHelper()
w = GameWindow(hh.process)
h = Heroes(hh.process, w)
watch = GameStateWatcher(w)

#wait for game state to update
sleep(1)
cid = w.findhero(h.heroes[h.CID])
print str(cid.x)

# h.upgradeall200()

# while True:
# 	state = watch.readState()
# 	if state.level == 1:
# 		cid = w.findhero(h.heroes[h.CID])
# 		w.levelup100(cid)
# 		w.levelup100(cid)
# 		for i in range(7):
# 			w.upgrade(cid, i)
# 		w.checkprog()

# 	if state.level >= 1 and state.level < 140:
# 		while state.level < 140:
# 			w.clickmonster(500)
# 			hero = h.getbutlastvisiblehero()
# 			w.levelup100(hero)
# 			state = watch.readState()
# 			w.checkprog()


# 	h.upgradeall200()

# 	# now go with frostleaf
# 	if state.level >= 140:

# 		while state.level < 1001:
# 			w.clickmonster(500)
# 			frost = w.findhero(h.heroes[h.FROST])
# 			w.levelup100(frost)
# 			state = watch.readState()

# 	# ascend
# 	if state.level >= 1001:
# 		amen = w.findhero(h.heroes[h.AMEN])
# 		w.upgrade(amen, 3)
# 		w.ascendConfirm()
