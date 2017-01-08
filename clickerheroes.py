#!/usr/bin/env python
# from time import *
# from datetime import datetime
# import os
import cv2
# from cv2 import cv
# import pytesseract


class Hero:
    def __init__(self, name, price, dps):
        self.name = name
        self.img = cv2.imread('img/%s/%s.png' % (name, name))
        self.goldimg = cv2.imread('img/%s/%sgold.png' % (name, name))
        self.price = price
        self.dps = dps


class Heroes:
    def __init__(self, suspendCallback, window):
        self.suspendCallback = suspendCallback
        self.window = window
        self.heroes = []
        self.loadheroes()
        self.CID = 0
        self.BETTY = 5
        self.SAMURAI = 6
        self.NATALIA = 10
        self.MIDAS = 15
        self.AMEN = 19
        self.SHINO = 23
        self.FROST = 25

    def loadheroes(self):
        with open('heroes.txt', 'r') as f:
            for l in f.read().split('\n'):
                if len(l) == 0:
                    continue
                tok = l.split(',')
                h = Hero(tok[0], float(tok[1]), float(tok[2]))
                self.heroes.append(h)

    def getbutlastvisiblehero(self):
        print('searching for last visible hero...')
        self.window.scrollbottom()
        onefound = False
        for i in reversed(range(27)):
            h = self.window.findvisiblehero(self.heroes[i])
            if h.x is not None:
                if onefound:
                    print(self.heroes[i].name + ' is last available... ')
                    return h
                else:
                    print(self.heroes[i].name + ' visible. searching for next... ')
                    onefound = True
            else:
                print(self.heroes[i].name + ' not visible ')

    def upgradeall200(self):
        for i in range(26):
            visibleHero = self.window.findhero(self.heroes[i], scrolldownfirst=True)
            self.window.levelup100(visibleHero)
            self.window.levelup100(visibleHero)
            if i != self.AMEN:
                for j in range(7):
                    self.window.upgrade(visibleHero, j)
            else:
                for j in range(3):
                    self.window.upgrade(visibleHero, j)
