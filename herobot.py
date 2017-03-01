# Python3.6 minimum

import logging.config
from time import sleep
import gamewindowwithoutclass as w
# from gamewindow import GameWindow
from clickerheroes import Heroes
from display import SuspendHelper

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('herobot')

sleep(0.5)

hh = SuspendHelper()
# w = GameWindow(hh.process)
h = Heroes(hh.process)
# watch = GameStateWatcher(w)

# wait for game state to update
sleep(1)

# cid, _ = w.findhero(h.heroes[h.CID])
# print(str(cid.x))
# h.upgradeall200(2)
# w.useskills()

# h.lastavailablehero()
# exit()

while True:
    savegame = w.grabsave()
    logger.debug('Current level: %s' % savegame['currentZoneHeight'])

    if savegame['currentZoneHeight'] == 1:
        cid, level = w.findhero(h.heroes[h.CID])
        if cid is not None and level < 200:
            w.levelup100(cid)
            w.levelup100(cid)
            for i in range(7):
                w.upgrade(cid, i)
            w.checkprog()
        else:
            logger.info('Could not find Cid')

    if savegame['currentZoneHeight'] >= 1 and savegame['currentZoneHeight'] < 100:
        lastlevel = savegame['currentZoneHeight']
        waitloop = 3
        while savegame['currentZoneHeight'] < 100:
            logger.debug('lastlevel: {}, currentlevel: {}'.format(lastlevel, savegame['currentZoneHeight']))
            hero = h.lastavailablehero(savegame)
            w.levelup100(hero)
            savegame = w.grabsave()
            lastlevel = savegame['currentZoneHeight']
            logger.debug('Current level: %s' % savegame['currentZoneHeight'])

            if lastlevel >= savegame['currentZoneHeight'] and waitloop == 0:
                w.useskills()
                w.checkprog()
                waitloop = 4
            waitloop -= 1
            # w.clickmonster(1500)

    if savegame['currentZoneHeight'] >= 100 and savegame['currentZoneHeight'] < 200:
        h.upgradeall200(savegame, 19)

        while savegame['currentZoneHeight'] < 200:
            # w.clickmonster(1500)
            hero = h.lastavailablehero(savegame)
            w.levelup100(hero)
            savegame = w.grabsave()
            logger.debug('Current level: %s' % savegame['currentZoneHeight'])
            sleep(10)


    # now go with samurai
    if savegame['currentZoneHeight'] >= 200 and savegame['currentZoneHeight'] < 1401:
        h.upgradeall200(savegame, 25)

        while savegame['currentZoneHeight'] < 1401:
            # w.clickmonster(1000)
            samurai, _ = w.findhero(h.heroes[h.SAMURAI])
            if samurai is not None:
                w.levelup100(samurai)
                savegame = w.grabsave()
                logger.debug('Current level: %s' % savegame['currentZoneHeight'])
                w.useskills()
                w.checkprog()
            else:
                logger.info('Could not find Samurai')

    # ascend
    if savegame['currentZoneHeight'] >= 1401:
        amen, _ = w.findhero(h.heroes[h.AMEN])
        if amen is not None:
            w.upgrade(amen, 3)
            w.ascendConfirm()

            # wait for state update
            sleep(5)
        else:
            logger.info('Could not find Amen')
