#!/usr/bin/env python
from time import *
from datetime import datetime
import cv2, os
from cv2 import cv
import pytesseract

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
		self.CID=0
		self.BETTY=5
		self.NATALIA=10
		self.MIDAS=15
		self.AMEN=19
		self.SHINO=23
		self.FROST=25

	def loadheroes(self):
		with open('heroes.txt', 'r') as f:
			for l in f.read().split('\n'):
				if len(l) == 0:
					continue
				tok = l.split(',')
				h = Hero(tok[0], float(tok[1]), float(tok[2]))
				self.heroes.append(h)

	def getbutlastvisiblehero(self):
		w.scrollbottom()
		onefound = False
		for i in reversed(range(25)):
			h = w.findvisiblehero(h.heroes[i])
			if h.x != None:
				if onefound:
					return h
				else:
					onefound = True

	def upgradeall200(self):
		for i in range(25):
			visibleHero = w.findhero(self.heroes[i])
			w.levelup100(visibleHero)
			w.levelup100(visibleHero)
			if i != self.AMEN:
				for j in range(7):
					w.upgrade(visibleHero, j)
			else:
				for j in range(3):
					w.upgrade(visibleHero, j)
