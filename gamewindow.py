import pyscreenshot as ImageGrab
import pytesseract
import cv2
# from cv2 import cv
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import numpy as np
from time import *
from timeit import timing
import logging

scrollPages = 10
pageScrollClicks = 5


class VisibleHero:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def gethirelocation(self, winx, winy):
        return (winx + 74, winy + self.y + 45)

    def getupgradelocation(self, winx, winy, i):
        return (winx + 186 + 37 * i, winy + self.y + 66)


class GameWindow:
    def __init__(self, suspendCallback):
        self.suspendCallback = suspendCallback
        self.winy = 0
        self.winx = 0
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.cvmethod = cv2.TM_CCOEFF_NORMED
        self.startpointer = cv2.imread('img/start.png')
        self.progimg = cv2.imread('img/prog.png')
        self.logger = logging.getLogger('herobot.gamewindow')
        self.getwindow()
        self.herosScrollUpLocation = (549, 190)
        self.herosScrollDownLocation = (549, 623)

    def getwindow(self):
        im = ImageGrab.grab().convert('RGB')
        big = np.array(im)
        big = big[:, :, ::-1].copy()
        r = cv2.matchTemplate(self.startpointer, big, self.cvmethod)
        y, x = np.unravel_index(r.argmax(), r.shape)
        self.winx = x - 14
        self.winy = y - 92
        self.logger.info('Window found at {}; {}'.format(str(self.winx), str(self.winy)))
        # self.hwinx = self.winx + 11
        # self.hwiny = self.winy + 171

    # @timing
    def grabocr(self, x, y, w, h):
        x = self.winx + x
        y = self.winy + y
        im = ImageGrab.grab(bbox=(x, y, x + w, y + h)).convert('RGB')

        # debug output
        # imcolor = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        # cv2.imwrite('tests/grabocr.bmp', imcolor)

        pix = im.load()
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                if pix[x, y] != (254, 254, 254):
                    pix[x, y] = 0
        return pytesseract.image_to_string(im, lang='eng')

    def click(self, location, times):
        x, y = location
        for i in range(times):
            self.mouse.click(self.winx + x, self.winy + y)
            sleep(0.02)

    def scrolltop(self):
        self.click(self.herosScrollUpLocation, pageScrollClicks * scrollPages)
        sleep(0.4)

    def scrollbottom(self):
        self.click(self.herosScrollDownLocation, pageScrollClicks * scrollPages)
        sleep(0.4)

    def scrollpageup(self):
        self.click(self.herosScrollUpLocation, pageScrollClicks)
        sleep(0.4)

    def scrollpagedown(self):
        self.click(self.herosScrollDownLocation, pageScrollClicks)
        sleep(0.4)

    # @timing
    def findimg(self, small, x, y, w, h):
        im = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        big = np.array(im)

        # Debug output
        # self.logger.debug('big shape: {}'.format(big.shape))
        cv2.imwrite('tests/big.bmp', cv2.cvtColor(big, cv2.COLOR_RGB2BGR))

        big = big[:, :, ::-1].copy()  # <- IndexError: too many indices for array

        while True:
            try:
                r = cv2.matchTemplate(small, big, self.cvmethod)
                break
            except:
                self.log.error("Warning: failed to grab image")
                continue

        y, x = np.unravel_index(r.argmax(), r.shape)
        loc = np.where(r >= 0.95)
        if loc.count(x) > 0 and loc.count(y) > 0:
            return (x, y)
        else:
            return (None, None)

    def findheroimg(self, small):
        leftmargin = 160
        topmargin = 173
        (x, y) = self.findimg(small, self.winx + leftmargin, self.winy + topmargin, 272, 420)
        if x is not None:
            return (x + leftmargin, y + topmargin)
        return (None, None)

    def findvisibleheroname(self, hero):
        x, y = self.findheroimg(hero.img)
        if x is None:
            x, y = self.findheroimg(hero.goldimg)
        return (x, y)

    def findheroname(self, hero, scrolldownfirst=False):
        x, y = self.findvisibleheroname(hero)
        if x is not None:
            return (x, y)

        if not scrolldownfirst:
            self.scrolltop()

        for i in range(scrollPages):
            x, y = self.findvisibleheroname(hero)
            if x is not None:
                return (x, y)
                break
            self.scrollpagedown()

        # make another pass from the top...
        if scrolldownfirst:
            self.scrolltop()

            for i in range(scrollPages):
                x, y = self.findvisibleheroname(hero)
                if x is not None:
                    return (x, y)
                    break
                self.scrollpagedown()

        return (None, None)

    def findherolevel(self, y):
        raw = self.grabocr(312, y + 20, 121, 25)
        self.logger.debug('findherolevel read: "{}"'.format(raw))
        num = ''.join(ch for ch in raw if ch.isdigit())
        try:
            return int(num)
        except:
            return 0

    def findvisiblehero(self, hero):
        x, y = self.findvisibleheroname(hero)
        return VisibleHero(x, y)

    def findhero(self, hero, scrolldownfirst=False):
        self.logger.info('searching for %s ...' % hero.name)
        x, y = self.findheroname(hero, scrolldownfirst)
        self.logger.debug('Found {} at {}; {}'.format(hero.name, str(x), str(y)))
        if x is not None:
            return (VisibleHero(x, y), self.findherolevel(y))
        else:
            return (None, None)

    def levelup100(self, visibleHero):
        x, y = visibleHero.gethirelocation(self.winx, self.winy)
        self.keyboard.press_key(self.keyboard.control_key)
        self.slowclick(x, y)
        self.keyboard.release_key(self.keyboard.control_key)

    def upgrade(self, visibleHero, index):
        x, y = visibleHero.getupgradelocation(self.winx, self.winy, index)
        self.slowclick(x, y)

    def checkprog(self):
        x, y = self.findimg(self.progimg, self.winx + 1090, self.winy + 223, 46, 60)
        if x is None and y is None:
            self.logger.debug('checkprog not seen OFF auto-progress indicator. Do nothing.')
            return
        else:
            self.logger.debug('checkprog clicked to activate auto-progression')
            self.slowclick(self.winx + 1115, self.winy + 252)

    def ascendConfirm(self):
        self.slowclick(self.winx + 490, self.winy + 420)

    def slowclick(self, x, y):
        sleep(0.15)
        self.mouse.click(x, y)
        sleep(0.15)

    def clickmonster(self, times):
        self.logger.info('clicking monster ...')
        for i in range(times):
            sleep(0.025)
            self.mouse.click(self.winx + 700, self.winy + 250)
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
