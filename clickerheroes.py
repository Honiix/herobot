#!/usr/bin/env python
# from time import *
# from datetime import datetime
# import os
import cv2
# from cv2 import cv
# import pytesseract
# from multiprocessing import Pool
import logging
import gamewindowwithoutclass as window
# from gamewindow import GameWindow as window
# import savereader as sr
# from exceptions import HeroNotFoundError


class Hero:
    def __init__(self, name, price, dps):
        self.name = name
        self.img = cv2.imread(f'img/{name}/{name}.png')
        self.goldimg = cv2.imread(f'img/{name}/{name}gold.png')
        self.price = price
        self.dps = dps


class Heroes:
    def __init__(self, suspendCallback):
        self.suspendCallback = suspendCallback
        self.window = window
        self.heroes = []
        self.load_heroes()
        self.CID = 0 + 1
        self.BETTY = 5 + 1
        self.SAMURAI = 6 + 1
        self.NATALIA = 10 + 1
        self.MIDAS = 15 + 1
        self.AMEN = 19 + 1
        self.SHINO = 23 + 1
        self.FROST = 25 + 1
        self.logger = logging.getLogger('herobot.clickerheroes')

    def load_heroes(self):
        with open('heroes.txt', 'r') as f:
            for l in f.read().split('\n'):
                if len(l) == 0:
                    continue
                tok = l.split(',')
                h = Hero(tok[0], float(tok[1]), float(tok[2]))
                self.heroes.append(h)

    def last_available_hero(self, savereader):
        self.logger.info('searching for last visible hero...')
        # window.scroll_bottom()

        # w = Worker(self.window, self.heroes)
        # h = w.searchhero()
        # self.logger.info('h in multi process: {}'.format(h))

        # for i in reversed(range(27)):
        #     h = findvisiblehero(self.heroes[i])
        #     if h.x is not None:
        #         h = findvisiblehero(self.heroes[i - 1 ])
        #         self.logger.info('{} is last available... '.format(self.heroes[i - 1].name))
        #         return h
        #     else:
        #         self.logger.info('%s not visible' % self.heroes[i].name)
        # hero, visible_hero = window.findvisiblehero(self.heroes, 27)
        last_id = savereader.last_available_hero_id
        last_available_hero = self.heroes[last_id - 1]

        visible_hero = window.find_hero(last_available_hero, True)

        self.logger.info(f'{last_available_hero.name} is last available... ')
        return last_available_hero, visible_hero

    def upgrade_all_200(self, savereader, upto):
        hc = savereader.hero_collection
        for i in range(upto):

            currenthero = hc.get(str(i))
            if currenthero is None:
                self.logger.info('Hero not found in the savegame {}'.format(currenthero))
                break

            if currenthero.get('level') < 200:
                visibleHero = window.find_hero(self.heroes[i], scrolldownfirst=True)
                if visibleHero is not None:
                    window.level_up_100(visibleHero)
                    window.level_up_100(visibleHero)
                    if i != self.AMEN:
                        for j in range(7):
                            window.upgrade(visibleHero, j)
                    else:
                        for j in range(3):
                            window.upgrade(visibleHero, j)
                else:
                    self.logger.info('Couldn\'t upgrade hero number {}'.format(i))
            else:
                self.logger.debug('hero {} was already level 200+'.format(i))


# class Worker():
#     def __init__(self, window, heroes, cores=None):
#         self.pool = Pool(processes=cores)
#         self.window = window
#         self.heroes = heroes
#         self.logger = logging.getLogger('herobot.clickerheroes.Worker')

#     def callback(self, result):
#         if result:
#             self.logger.info('Hero found, stop other process')
#             self.pool.terminate()

#     def searchhero(self):
#         for i in reversed(range(27)):
#             result = self.pool.apply_async(
#                 findvisiblehero,
#                 args=self.heroes[i],
#                 callback=self.callback)
#             self.logger.info('Searching for {}'.format(self.heroes[i].name))
#         self.pool.close()
#         self.pool.join()
#         return result.get(timeout=10)
