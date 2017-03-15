import pyscreenshot as ImageGrab
import pytesseract
import cv2
# from cv2 import cv
from multiprocessing import Pool, Manager
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import numpy as np
from time import sleep
from timeit import timing
import logging
import savereader
from display import SuspendHelper
from exceptions import HeroNotFoundError

scrollPages = 10
pageScrollClicks = 5


class VisibleHero:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def hire_location(self):
        return 96, self.y + 230

    def upgrade_location(self, i):
        return 195 + 37 * i, self.y + 66


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
logger.info(f'Window found at {winx}; {winy}')
# hwinx = winx + 11
# hwiny = winy + 171


# @timing
def grab_ocr(x, y, w, h):
    """ Translate picture to text """
    x = winx + x
    y = winy + y
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


def click(location, times):
    x, y = location
    for i in range(times):
        mouse.click(winx + x, winy + y)
        sleep(0.02)


def slow_click(x, y):
    sleep(0.15)
    # grab_screen(x - 50, y - 50, 100, 100)  # helps debug, look at: tests/big.bmp
    click((x, y), 1)
    sleep(0.15)


def click_monster(times):
    logger.info('clicking monster ...')
    for i in range(times):
        sleep(0.025)
        click(700, 250)
        # suspendCallback()


def scroll_top():
    click(herosScrollUpLocation, pageScrollClicks * scrollPages)
    sleep(0.4)


def scroll_bottom():
    click(herosScrollDownLocation, pageScrollClicks * scrollPages)
    sleep(0.4)


def scroll_page_up():
    click(herosScrollUpLocation, pageScrollClicks)
    sleep(0.4)


def scroll_page_down():
    click(herosScrollDownLocation, pageScrollClicks)
    sleep(0.4)


def grab_screen(x, y, w, h):
    """ Take screenshot of the specified region of screen (knows winx + winy)
    Save a bmp into disk for debuging perpose. I wasn't able to copile
    cv2 with GTK support. Hint, you can open this .bmp in Sublime Text
    it will refresh automatically when file change.
    """
    im = ImageGrab.grab(bbox=(winx + x, winy + y, winx + x + w, winy + y + h))
    big = np.array(im)

    # Debug output
    # logger.debug('big shape: {}'.format(big.shape))
    try:
        big_correct_color = cv2.cvtColor(big, cv2.COLOR_RGB2BGR)
    except Exception as e:
        big_correct_color = big
        logger.error(f'Error while trying to convert color: {e}')

    cv2.imwrite('tests/big.bmp', big_correct_color)

    big = big[:, :, ::-1].copy()  # <- IndexError: too many indices for array
    return big


def grab_screen_visible_hero():
    """ capture heroes window from top to almost bottom """
    leftmargin = 160
    topmargin = 175
    return grab_screen(leftmargin, topmargin, 272, 350)


# @timing
def find_img_location(small, big):
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
        return x, y
    else:
        return 0, 0


def find_visible_hero_name_mp(hero, big, event):
    """ multiprocessing version
    if found, return hero and his position in the screenshot
    """
    if event.is_set():
        return

    x, y = find_img_location(hero.img, big)

    if x == 0 and y == 0:
        x, y = find_img_location(hero.goldimg, big)

    event.set()
    logger.debug(f'{hero.name}: {x},{y}')
    return (hero, x, y)


def find_hero(hero, scrolldownfirst=False):
    """ Find a specific hero """
    logger.info('searching for %s ...' % hero.name)
    x, y = find_hero_name(hero, scrolldownfirst)
    logger.debug(f'Found {hero.name} at {x}; {y}')
    return VisibleHero(x, y)


def find_hero_name(hero, scrolldownfirst=False):
    """ From a screenshot of the portion of screen where
    you can scroll heroes, scroll until it found the hero
    and return his position in the screenshot
    """

    # Zone to capture
    left = 160
    top = 175
    width = 272
    height = 350

    def get_hero_location():
        big = grab_screen(left, top, width, height)
        logger.debug(f'Took a capture at {left}, {top} and {width}px wide, {height}px high')
        x, y = find_visible_hero_name(hero, big)
        return x, y

    x, y = get_hero_location()
    if x != 0 and y != 0:
        logger.debug('Found hero at 1st try')
        return x, y

    if not scrolldownfirst:
        scroll_top()

    for i in range(scrollPages):
        x, y = get_hero_location()
        if x != 0 and y != 0:
            logger.debug('Found hero at 2nd try')
            return x, y
        scroll_page_down()

    # make another pass from the top...
    if scrolldownfirst:
        scroll_top()

        for i in range(scrollPages):
            x, y = get_hero_location()
            if x != 0:
                logger.debug('Found hero at 3rd try')
                return x, y
            scroll_page_down()

    logger.error('Hero not found')
    return 0, 0


def find_visible_hero_name(hero, big):
    """ if found, return hero and his position in the screenshot """
    x, y = find_img_location(hero.img, big)

    if x == 0:
        x, y = find_img_location(hero.goldimg, big)

    logger.debug(f'Visible Hero Name: {hero.name}: {x},{y}')
    return x, y


def find_visible_hero(heroes, herorange):
    """ From a screenshot of the lower portion of the windows
    where you can scroll heroes, ask a worker to find any
    heroes sent to it """
    big = grab_screen_visible_hero()
    try:
        hero, x, y = find_visible_hero_worker(heroes, herorange, big)
    except TypeError:
        return
    except HeroNotFoundError:
        return
    else:
        return (hero, VisibleHero(x, y))


def find_visible_hero_worker(heroes, herorange, big):
    """ worker that return all found hero into a screenshot """
    pool = Pool()
    m = Manager()
    event = m.Event()
    results = list()
    for i in reversed(range(herorange)):
        results.append(pool.apply_async(find_visible_hero_name_mp, args=(heroes[i], big, event)))
    logger.debug(f'Searching for hero number {i} to {herorange}')
    pool.close()
    event.wait(timeout=6)
    pool.terminate()

    try:
        results_extracted = next(r.get() for r in results if r.get() is not None)
    except StopIteration as s:
        logger.error('Hero not found')
        raise HeroNotFoundError
    else:
        return results_extracted


def level_up_100(visibleHero):
    """ click into a hero location with CTRL key pressed """
    x, y = visibleHero.hire_location()
    keyboard.press_key(keyboard.control_key)
    slow_click(x, y)
    logger.debug(f'level_up_100: clicking at {x} px, {y} px')
    keyboard.release_key(keyboard.control_key)


def upgrade(visibleHero, index):
    """ Buy a unique hero upgrade """
    x, y = visibleHero.upgrade_location(index)
    slow_click(x, y)


def check_prog():
    big = grab_screen(1090, 227, 46, 55)
    x, y = find_img_location(progimg, big, 1090, 227, 46, 55)
    if x is 0 and y is 0:
        logger.debug('check_prog not seen OFF auto-progress indicator. Do nothing.')
        return
    else:
        logger.debug('check_prog clicked to activate auto-progression')
        slow_click(1115, 252)


def ascend_confirm():
    slow_click(490, 420)


def use_skills():
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
    slow_click(1116, 26)  # Click on wrench
    slow_click(278, 78)   # Click on Save
    sleep(0.2)
    keyboard.press_key(keyboard.escape_key)
    sleep(0.2)
    slow_click(945, 29)  # Click on close
    sleep(0.2)
    slow_click(945, 29)  # Click on close again in case windows wasn't active
    sr = savereader.SaveReader()
    return sr
