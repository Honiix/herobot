import pyscreenshot as ImageGrab
import pytesseract
import cv2
# from cv2 import cv
from multiprocessing import Pool
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import numpy as np
from time import sleep
from timeit import timing
import logging
from savereader import extract_save_from_clipboard

scrollPages = 10
pageScrollClicks = 5


class VisibleHero:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def hire_location(self, winx, winy):
        return (winx + 74, winy + self.y + 45)

    def upgrade_location(self, winx, winy, i):
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
    def grab_ocr(self, x, y, w, h):
        x = self.winx + x
        y = self.winy + y
        im = ImageGrab.grab(bbox=(x, y, x + w, y + h)).convert('RGB')

        # debug output
        # imcolor = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        # cv2.imwrite('tests/grab_ocr.bmp', imcolor)

        pix = im.load()
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                if pix[x, y] != (254, 254, 254):
                    pix[x, y] = 0
        return pytesseract.image_to_string(im, lang='eng')

    def grab_screen(self, x, y, w, h):
        """ Take screenshot of the specified region of gamewindow
        Save a bmp into disk for debuging perpose. I wasn't able to copile
        cv2 with GTK support. Hint, you can open this .bmp in Sublime Text
        it will refresh automatically when file change.
        """
        im = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        big = np.array(im)

        # Debug output
        # logger.debug('big shape: {}'.format(big.shape))
        cv2.imwrite('tests/big.bmp', cv2.cvtColor(big, cv2.COLOR_RGB2BGR))

        big = big[:, :, ::-1].copy()  # <- IndexError: too many indices for array
        return big

    def grab_screenlastvisiblehero(self):
        """ capture heroes window lower region where last available hero will be """
        leftmargin = 160
        topmargin = 383
        return self.grab_screen(self.winx + leftmargin, self.winy + topmargin, 272, 210)

    def grab_screen_visible_hero(self):
        """ capture heroes window from top to almost bottom """
        leftmargin = 160
        topmargin = 175
        return self.grab_screen(self.winx + leftmargin, self.winy + topmargin, 272, 350)

    def click(self, location, times):
        x, y = location
        for i in range(times):
            self.mouse.click(self.winx + x, self.winy + y)
            sleep(0.02)

    def scroll_top(self):
        self.click(self.herosScrollUpLocation, pageScrollClicks * scrollPages)
        sleep(0.4)

    def scroll_bottom(self):
        self.click(self.herosScrollDownLocation, pageScrollClicks * scrollPages)
        sleep(0.4)

    def scroll_page_up(self):
        self.click(self.herosScrollUpLocation, pageScrollClicks)
        sleep(0.4)

    def scroll_page_down(self):
        self.click(self.herosScrollDownLocation, pageScrollClicks)
        sleep(0.4)

    # @timing
    def find_img_location(self, small, x, y, w, h):
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

    def find_img_location(self, small):
        leftmargin = 160
        topmargin = 383
        (x, y) = self.find_img_location(small, self.winx + leftmargin, self.winy + topmargin, 272, 210)
        if x is not None:
            return (x + leftmargin, y + topmargin)
        return (None, None)

    def findvisibleheroname(self, hero):
        x, y = self.find_img_location(hero.img)
        if x is None:
            x, y = self.find_img_location(hero.goldimg)
        return (x, y)

    def find_hero_name(self, hero, scrolldownfirst=False):
        x, y = self.findvisibleheroname(hero)
        if x is not None:
            return (x, y)

        if not scrolldownfirst:
            self.scroll_top()

        for i in range(scrollPages):
            x, y = self.findvisibleheroname(hero)
            if x is not None:
                return (x, y)
                break
            self.scroll_page_down()

        # make another pass from the top...
        if scrolldownfirst:
            self.scroll_top()

            for i in range(scrollPages):
                x, y = self.findvisibleheroname(hero)
                if x is not None:
                    return (x, y)
                    break
                self.scroll_page_down()

        return (None, None)

    def find_herolevel(self, y):
        raw = self.grab_ocr(312, y + 20, 121, 25)
        self.logger.debug('find_herolevel read: "{}"'.format(raw))
        num = ''.join(ch for ch in raw if ch.isdigit())
        try:
            return int(num)
        except:
            return 0

    def findvisiblehero(self, herorange: int):
        # x, y = self.findvisibleheroname(hero)
        # result = self.findvisibleheroworker(herorange)
        # if result:
        #     x, y = result
        # return VisibleHero(x, y)

        big = self.grab_screenlastvisiblehero()
        try:
            hero, x, y = self.findvisibleheroworker(herorange, big)
        except TypeError:
            return (None, VisibleHero(None, None))
        else:
            if x is not None and y is not None:
                return (hero, VisibleHero(x, y))
            else:
                return (None, VisibleHero(None, None))

    def callback(self, result):
        if result:
            self.logger.info('Hero found, stop other process')
            self.pool.terminate()

    def findvisibleheroworker(self, herorange: int):
        pool = Pool()
        for i in reversed(range(herorange)):
            result = pool.apply_async(
                self.findvisibleheroname,
                args=self.heroes[i],
                callback=self.callback)
            self.logger.info('Searching for hero number {}'.format(i))
        pool.close()
        pool.join()
        return result.get(timeout=10)

    def find_hero(self, hero, scrolldownfirst=False):
        self.logger.info('searching for %s ...' % hero.name)
        x, y = self.find_hero_name(hero, scrolldownfirst)
        self.logger.debug('Found {} at {}; {}'.format(hero.name, str(x), str(y)))
        if x is not None:
            return (VisibleHero(x, y), self.find_herolevel(y))
        else:
            return (None, None)

    def level_up_100(self, visibleHero):
        x, y = visibleHero.hire_location()
        self.keyboard.press_key(self.keyboard.control_key)
        self.slow_click(x, y)
        self.logger.debug(f'level_up_100: clicking at {x} px, {y} px')
        self.keyboard.release_key(self.keyboard.control_key)

    def upgrade(self, visibleHero, index):
        x, y = visibleHero.upgrade_location(index)
        self.slow_click(x, y)

    def check_prog(self):
        x, y = self.find_img_location(self.progimg, self.winx + 1090, self.winy + 227, 46, 55)
        if x is None and y is None:
            self.logger.debug('check_prog not seen OFF auto-progress indicator. Do nothing.')
            return
        else:
            self.logger.debug('check_prog clicked to activate auto-progression')
            self.slow_click(self.winx + 1115, self.winy + 252)

    def ascend_confirm(self):
        self.slow_click(self.winx + 490, self.winy + 420)

    def slow_click(self, x, y):
        sleep(0.15)
        self.mouse.click(x, y)
        sleep(0.15)

    def click_monster(self, times):
        self.logger.info('clicking monster ...')
        for i in range(times):
            sleep(0.025)
            self.mouse.click(self.winx + 700, self.winy + 250)
            self.suspendCallback()

    def use_skills(self):
        self.keyboard.tap_key('1')
        self.keyboard.tap_key('2')
        self.keyboard.tap_key('8')
        self.keyboard.tap_key('3')
        self.keyboard.tap_key('9')
        self.keyboard.tap_key('4')
        self.keyboard.tap_key('5')
        self.keyboard.tap_key('6')
        self.keyboard.tap_key('7')

    def grabsave(self) -> dict:
        self.slow_click(self.winx + 1116, self.winy + 26)  # Click on wrench
        self.slow_click(self.winx + 278, self.winy + 78)   # Click on Save
        sleep(0.2)
        self.keyboard.press_key(self.keyboard.escape_key)
        sleep(0.2)
        self.slow_click(self.winx + 945, self.winy + 29)  # Click on close
        sleep(0.2)
        self.slow_click(self.winx + 945, self.winy + 29)  # Click on close again in case windows wasn't active
        return extract_save_from_clipboard()
