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

# cid = w.find_hero(h.heroes[h.CID])
# print(str(cid.x))
# h.upgrade_all_200(2)
# w.use_skills()

# h.last_available_hero()
# exit()


while True:
    savereader = w.grabsave()
    logger.debug('Current level: %s' % savereader.savegame['currentZoneHeight'])

    if savereader.savegame['currentZoneHeight'] == 1:
        heroes = savereader.hero_collection
        cid = heroes.get(h.CID)
        cid_obj = w.find_hero(h.heroes[h.CID])
        if cid.get('level') < 200:
            w.level_up_100(cid_obj)
            w.level_up_100(cid_obj)
            for i in range(7):
                w.upgrade(cid_obj, i)
            w.check_prog()
        else:
            logger.info('Could not find Cid')

    if savereader.savegame['currentZoneHeight'] >= 1 and savereader.savegame['currentZoneHeight'] < 100:
        lastlevel = savereader.savegame['currentZoneHeight']
        waitloop = 3
        while savereader.savegame['currentZoneHeight'] < 100:
            logger.debug('lastlevel: {}, currentlevel: {}'.format(lastlevel, savereader.savegame['currentZoneHeight']))
            hero, visible_hero = h.last_available_hero(savereader)
            logger.debug(f'Leveling up {hero.name} by 100')
            w.level_up_100(visible_hero)

            logger.info('waiting 1 minute...')
            sleep(60)

            savereader = w.grabsave()

            if lastlevel >= savereader.savegame['currentZoneHeight'] and waitloop == 0:
                w.use_skills()
                w.check_prog()
                waitloop = 4
            waitloop -= 1
            # w.click_monster(1500)

    if savereader.savegame['currentZoneHeight'] >= 100 and savereader.savegame['currentZoneHeight'] < 200:
        h.upgrade_all_200(savereader, 19)

        while savereader.savegame['currentZoneHeight'] < 200:
            # w.click_monster(1500)
            hero, visible_hero = h.last_available_hero(savereader)
            w.level_up_100(visible_hero)
            savereader = w.grabsave()
            logger.debug('Current level: %s' % savereader.savegame['currentZoneHeight'])
            sleep(20)

    # now go with samurai
    if savereader.savegame['currentZoneHeight'] >= 200 and savereader.savegame['currentZoneHeight'] < 1401:
        h.upgrade_all_200(savereader, 25)

        while savereader.savegame['currentZoneHeight'] < 1401:
            # w.click_monster(1000)
            samurai = w.find_hero(h.heroes[h.SAMURAI])
            if samurai is not None:
                w.level_up_100(samurai)
                savereader = w.grabsave()
                logger.debug('Current level: %s' % savereader.savegame['currentZoneHeight'])
                w.use_skills()
                w.check_prog()
            else:
                logger.info('Could not find Samurai')

    # ascend
    if savereader.savegame['currentZoneHeight'] >= 1401:
        amen = w.find_hero(h.heroes[h.AMEN])
        if amen is not None:
            w.upgrade(amen, 3)
            w.ascend_confirm()

            # wait for state update
            sleep(5)
        else:
            logger.info('Could not find Amen')
