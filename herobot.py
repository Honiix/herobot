#!/usr/bin/env python

from clickerheroes import Heroes
from gamewindow import GameWindow
from gamestatewatch import GameStateWatcher
from display import SuspendHelper
from savereader import grabsave

from time import *
# from enum import Enum
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('herobot')

sleep(1)

hh = SuspendHelper()
w = GameWindow(hh.process)
h = Heroes(hh.process, w)
watch = GameStateWatcher(w)

# wait for game state to update
sleep(1)

# cid, _ = w.findhero(h.heroes[h.CID])
# print(str(cid.x))
# h.upgradeall200(2)
# w.useskills()

w.clicksave()
savegame = grabsave()

while True:
    state = watch.readState()
    logger.debug('readState level: %s' % state.level)
    if state.level == 1:
        cid, level = w.findhero(h.heroes[h.CID])
        if cid is not None and level < 200:
            w.levelup100(cid)
            w.levelup100(cid)
            for i in range(7):
                w.upgrade(cid, i)
            w.checkprog()
        else:
            logger.info('Could not find Cid')

    if state.level >= 1 and state.level < 100:
        while state.level < 100:
            w.clickmonster(500)
            hero = h.getbutlastvisiblehero()
            if hero is not None:
                w.levelup100(hero)
                state = watch.readState()
                w.useskills()
                w.checkprog()
            else:
                logger.info('Could not find before last hero')

    if state.level >= 100 and state.level < 200:
        h.upgradeall200(19)

        while state.level < 200:
            w.clickmonster(500)
            hero = h.getbutlastvisiblehero()
            if hero is not None:
                w.levelup100(hero)
                state = watch.readState()
                w.useskills()
                w.checkprog()
            else:
                logger.info('Could not find before last hero')

    # now go with samurai
    if state.level >= 200 and state.level < 1401:
        h.upgradeall200(25)

        while state.level < 1401:
            w.clickmonster(1000)
            samurai, _ = w.findhero(h.heroes[h.SAMURAI])
            if samurai is not None:
                w.levelup100(samurai)
                state = watch.readState()
                w.useskills()
                w.checkprog()
            else:
                logger.info('Could not find Samurai')

    # ascend
    if state.level >= 1401:
        amen, _ = w.findhero(h.heroes[h.AMEN])
        if amen is not None:
            w.upgrade(amen, 3)
            w.ascendConfirm()

            # wait for state update
            sleep(5)
        else:
            logger.info('Could not find Amen')
