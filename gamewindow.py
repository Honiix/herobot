import pyscreenshot as ImageGrab
import pytesseract
import cv2, os
from cv2 import cv
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import numpy as np
from time import *

scrollPages = 10

class VisibleHero:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def gethirelocation(self, winx, winy):
		return (winx + 74, winy + self.y + 45)

	def getupgradelocation(self, winx, winy, i):
		return (winx + 186 + 37*i, winy + self.y + 66)


class GameWindow:
	def __init__(self, suspendCallback):
		self.suspendCallback = suspendCallback
		self.wniy = 0
		self.winx = 0
		self.mouse = PyMouse()
		self.keyboard = PyKeyboard()
		self.cvmethod = cv2.TM_CCOEFF_NORMED
		self.startpointer = cv2.imread('img/start.png')
		self.progimg = cv2.imread('img/prog.png')
		self.getwindow()
		self.herosScrollUpLocation = (549, 190)
		self.herosScrollDownLocation = (549, 623)

	def getwindow(self):
		im = ImageGrab.grab().convert('RGB')
		big=np.array(im)
		big=big[:, :, ::-1].copy()
		r = cv2.matchTemplate(self.startpointer, big, self.cvmethod)
		y, x = np.unravel_index(r.argmax(), r.shape)
		self.winx = x - 14
		self.winy = y - 86
		print 'window found at ' + str(self.winx) + '; ' + str(self.winy)
		# self.hwinx = self.winx + 11
		# self.hwiny = self.winy + 171

	def grabocr(self, x, y, w, h):
		x = self.winx + x
		y = self.winy + y
		im = ImageGrab.grab(bbox=(x, y, x+w, y+h))
		pix = im.load()
		for x in range(im.size[0]):
			for y in range(im.size[1]):
				if pix[x, y] != (254, 254, 254):
					pix[x, y] = 0;
		return pytesseract.image_to_string(im)

	def click(self, location, times):
		x, y = location
		for i in range(times):
			self.mouse.click(self.winx + x, self.winy + y)
			sleep(0.02)

	def scrolltop(self):
		self.click(self.herosScrollUpLocation, 6 * scrollPages)
		sleep(0.4)

	def scrollbottom(self):
		self.click(self.herosScrollDownLocation, 6 * scrollPages)
		sleep(0.4)

	def scrollpageup(self):
		self.click(self.herosScrollUpLocation, 6)
		sleep(0.4)

	def scrollpagedown(self):
		self.click(self.herosScrollDownLocation, 6)
		sleep(0.4)


	def findimg(self, small, x, y, w, h):
		im = ImageGrab.grab(bbox=(x, y, x+w, y+h))
		big=np.array(im)
		big=big[:, :, ::-1].copy()

		while True:
			try:
				r = cv2.matchTemplate(small, big, self.cvmethod)
				break
			except:
				print "Warning: failed to grab image"
				continue

		y, x = np.unravel_index(r.argmax(), r.shape)
		loc = np.where(r >= 0.95)
		if loc.count(x) > 0 and loc.count(y) > 0:
			return (x, y)
		else:
			return (None, None)

	def findheroimg(self, small):
		(x, y) = self.findimg(small, self.winx + 5, self.winy + 160, 535, 410)
		if x != None:
			return (x + 5, y + 160)
		return (None, None)

	def findvisibleheroname(self, hero):
		x, y = self.findheroimg(hero.img)
		if x == None:
			x, y = self.findheroimg(hero.goldimg)
		return (x, y)

	def findheroname(self, hero, scrolldownfirst = False):
		x, y = self.findvisibleheroname(hero)
		if x != None:
			print 'found ' + hero.name + ' at ' + str(x) + ' ; ' + str(y)
			return (x, y)
		
		if not scrolldownfirst:
			self.scrolltop()
		
		for i in range(scrollPages):
			x, y = self.findvisibleheroname(hero)
			if x != None:
				print 'found ' + hero.name + ' at ' + str(x) + ' ; ' + str(y)
				return (x, y)
				break
			self.scrollpagedown()

		# make another pass from the top...
		if scrolldownfirst:
			self.scrolltop()
		
			for i in range(scrollPages):
				x, y = self.findvisibleheroname(hero)
				if x != None:
					print 'found ' + hero.name + ' at ' + str(x) + ' ; ' + str(y)
					return (x, y)
					break
				self.scrollpagedown()

		return (None, None)

	def findvisiblehero(self, hero):
		x, y = self.findvisibleheroname(hero)
		return VisibleHero(x, y)


	def findhero(self, hero, scrolldownfirst = False):
		print 'searching for ' + hero.name + '...'
		x, y = self.findheroname(hero, scrolldownfirst)
		print 'found at: ' + str(x) + ' ' + str(y)
		return VisibleHero(x, y)

	def levelup100(self, visibleHero):
		x,y = visibleHero.gethirelocation(self.winx, self.winy)
		self.keyboard.press_key(self.keyboard.control_key)
		self.slowclick(x, y)
		self.keyboard.release_key(self.keyboard.control_key)

	def upgrade(self, visibleHero, index):
		x,y = visibleHero.getupgradelocation(self.winx, self.winy, index)
		self.slowclick(x, y)


	def checkprog(self):
		x, y = self.findimg(self.progimg, self.winx+1090, self.winy+190, 60, 60)
		if x == None and y == None:
			return
		else:
			self.slowclick(self.winx+1111, self.winy+211)

	def ascendConfirm(self):
		self.slowclick(self.winx + 490, self.winy + 420)

	def slowclick(self, x, y):
		sleep(0.15)
		self.mouse.click(x, y)
		sleep(0.15)

	def clickmonster(self, times):
		print 'clicking monster ...'
		for i in range(times):
			sleep(0.018)
			self.mouse.click(self.winx + 580, self.winy + 120)
			self.suspendCallback()

	def useskills(self):
		self.keyboard.tap_key('1')
		self.keyboard.tap_key('2')
		self.keyboard.tap_key('8')
		self.keyboard.tap_key('3')
		self.keyboard.tap_key('9')
		self.keyboard.tap_key('4')
		self.keyboard.tap_key('5')
		self.keyboard.tap_key('6')
		self.keyboard.tap_key('7')

