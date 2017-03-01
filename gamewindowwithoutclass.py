import pyscreenshot as ImageGrab
import pytesseract
import cv2
# from cv2 import cv
from multiprocessing import (Pool, Manager)
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import numpy as np
from time import sleep
from timeit import timing
import logging
from savereader import extract_save_from_clipboard
from display import SuspendHelper

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


logger = logging.getLogger('herobot.gamewindowwithoutclass')
winy = 0
winx = 0
mouse = PyMouse()
keyboard = PyKeyboard()
cvmethod = cv2.TM_CCOEFF_NORMED
startpointer = cv2.imread('img/start.png')
progimg = cv2.imread('img/prog.png')
herosScrollUpLocation = (549, 190)
herosScrollDownLocation = (549, 623)

im = ImageGrab.grab().convert('RGB')
big = np.array(im)
big = big[:, :, ::-1].copy()
r = cv2.matchTemplate(startpointer, big, cvmethod)
y, x = np.unravel_index(r.argmax(), r.shape)
winx = x - 14
winy = y - 92
logger.info('Window found at {}; {}'.format(str(winx), str(winy)))
# hwinx = winx + 11
# hwiny = winy + 171


# @timing
def grabocr(x, y, w, h):
    """ Translate picture to text """
    x = winx + x
    y = winy + y
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


def click(location, times):
    x, y = location
    for i in range(times):
        mouse.click(winx + x, winy + y)
        sleep(0.02)


def scrolltop():
    click(herosScrollUpLocation, pageScrollClicks * scrollPages)
    sleep(0.4)


def scrollbottom():
    click(herosScrollDownLocation, pageScrollClicks * scrollPages)
    sleep(0.4)


def scrollpageup():
    click(herosScrollUpLocation, pageScrollClicks)
    sleep(0.4)


def scrollpagedown():
    click(herosScrollDownLocation, pageScrollClicks)
    sleep(0.4)


def grabscreen(x, y, w, h):
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


def grabscreenlastvisiblehero():
    """ capture heroes window lower region where last available hero will be """
    leftmargin = 160
    topmargin = 383
    return grabscreen(winx + leftmargin, winy + topmargin, 272, 210)


def grabscreenvisiblehero():
    """ capture heroes window from top to almost bottom """
    leftmargin = 160
    topmargin = 175
    return grabscreen(winx + leftmargin, winy + topmargin, 272, 350)


# @timing
def findimg(small, big):
    """ search if small is in big """
    while True:
        try:
            r = cv2.matchTemplate(small, big, cvmethod)
            break
        except:
            logger.error("Warning: failed to grab image")
            continue

    y, x = np.unravel_index(r.argmax(), r.shape)
    loc = np.where(r >= 0.95)
    if loc.count(x) > 0 and loc.count(y) > 0:
        return (x, y)
    else:
        return (None, None)


def findheroimg(small, big):
    """ The hero position in the screenshot """
    (x, y) = findimg(small, big)
    if x is not None:
        return (x, y)
    return (None, None)


def findvisibleheronamemp(hero, big, event):
    """ multiprocessing version
    if found, return hero and his position in the screenshot
    """
    if event.is_set():
        return

    coord = findheroimg(hero.img, big)
    if coord:
        x, y = coord

    if x is None:
        coord = findheroimg(hero.goldimg, big)
        if coord:
            x, y = coord
        else:
            return

    if x is not None:
        event.set()
        logger.debug('{}: {},{}'.format(hero.name, x, y))
        return (hero, x, y)


def findvisibleheroname(hero, big):
    """ if found, return hero and his position in the screenshot """
    x, y = findheroimg(hero.img, big)
    if x is None:
        x, y = findheroimg(hero.goldimg, big)
    if x is not None:
        logger.debug('{}: {},{}'.format(hero.name, x, y))
        return (hero, x, y)


def findheroname(hero, scrolldownfirst=False):
    """ From a screenshot of the portion of screen where
    you can scroll heroes, scroll until it found the hero
    and return his position in the screenshot
    """
    big = grabscreenvisiblehero()
    hero, x, y = findvisibleheroname(hero, big)
    if x is not None:
        return (x, y)

    if not scrolldownfirst:
        scrolltop()

    for i in range(scrollPages):
        hero, x, y = findvisibleheroname(hero, big)
        if x is not None:
            return (x, y)
            break
        scrollpagedown()

    # make another pass from the top...
    if scrolldownfirst:
        scrolltop()

        for i in range(scrollPages):
            hero, x, y = findvisibleheroname(hero, big)
            if x is not None:
                return (x, y)
                break
            scrollpagedown()

    return (None, None)


def findherolevel(y):
    """ can be remove, savegame has this information """
    raw = grabocr(312, y + 20, 121, 25)
    logger.debug('findherolevel read: "{}"'.format(raw))
    num = ''.join(ch for ch in raw if ch.isdigit())
    try:
        return int(num)
    except:
        return 0


def findvisiblehero(heroes, herorange):
    """ From a screenshot of the lower portion of the windows
    where you can scroll heroes, ask a worker to find any
    heroes sent to it """
    big = grabscreenlastvisiblehero()
    try:
        hero, x, y = findvisibleheroworker(heroes, herorange, big)
    except TypeError:
        return
    else:
        if x is not None and y is not None:
            return (hero, VisibleHero(x, y))
        else:
            return


def findvisibleheroworker(heroes, herorange, big):
    """ worker that return all found hero into a screenshot """
    pool = Pool()
    m = Manager()
    event = m.Event()
    results = list()
    for i in reversed(range(herorange)):
        results.append(pool.apply_async(findvisibleheronamemp, args=(heroes[i], big, event)))
    logger.debug('Searching for hero number {} to {}'.format(i, herorange))
    pool.close()
    event.wait(timeout=6)
    pool.terminate()

    try:
        results_extracted = next(r.get() for r in results if r.get() is not None)
    except StopIteration as s:
        logger.error('Hero not found')
        return
    else:
        return results_extracted


def findhero(hero, scrolldownfirst=False):
    """ Find a specific hero """
    logger.info('searching for %s ...' % hero.name)
    x, y = findheroname(hero, scrolldownfirst)
    logger.debug('Found {} at {}; {}'.format(hero.name, str(x), str(y)))
    if x is not None:
        return VisibleHero(x, y)
    else:
        return None


def levelup100(visibleHero):
    """ click into a hero location with CTRL key pressed """
    x, y = visibleHero.gethirelocation(winx, winy)
    keyboard.press_key(keyboard.control_key)
    slowclick(x, y)
    keyboard.release_key(keyboard.control_key)


def upgrade(visibleHero, index):
    """ Buy a unique hero upgrade """
    x, y = visibleHero.getupgradelocation(winx, winy, index)
    slowclick(x, y)


def checkprog():
    big = grabscreen(winx + 1090, winy + 227, 46, 55)
    x, y = findimg(progimg, big, winx + 1090, winy + 227, 46, 55)
    if x is None and y is None:
        logger.debug('checkprog not seen OFF auto-progress indicator. Do nothing.')
        return
    else:
        logger.debug('checkprog clicked to activate auto-progression')
        slowclick(winx + 1115, winy + 252)


def ascendConfirm():
    slowclick(winx + 490, winy + 420)


def slowclick(x, y):
    sleep(0.15)
    mouse.click(x, y)
    sleep(0.15)


def clickmonster(times):
    logger.info('clicking monster ...')
    for i in range(times):
        sleep(0.025)
        mouse.click(winx + 700, winy + 250)
        suspendCallback()


def useskills():
    keyboard.tap_key('1')
    keyboard.tap_key('2')
    keyboard.tap_key('8')
    keyboard.tap_key('3')
    keyboard.tap_key('9')
    keyboard.tap_key('4')
    keyboard.tap_key('5')
    keyboard.tap_key('6')
    keyboard.tap_key('7')


def grabsave():
    slowclick(winx + 1116, winy + 26)  # Click on wrench
    slowclick(winx + 278, winy + 78)   # Click on Save
    sleep(0.2)
    keyboard.press_key(keyboard.escape_key)
    sleep(0.2)
    slowclick(winx + 945, winy + 29)  # Click on close
    sleep(0.2)
    slowclick(winx + 945, winy + 29)  # Click on close again in case windows wasn't active
    return extract_save_from_clipboard()