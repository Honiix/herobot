import threading
# import Queue
import copy
import logging

from time import *
# from timeit import timing


class GameState:
    pass


class GameStateWatcher:
    def __init__(self, window):
        self.window = window
        self.lock = threading.Lock()
        self.state = GameState()
        t = threading.Thread(target=self.watchThread)
        t.daemon = True
        t.start()
        self.logger = logging.getLogger('herobot.gamestatewatch')

    def watchThread(self):
        while True:
            self.lock.acquire()
            self.state.level = self.getlevel()
            # self.state.money = self.getmoney()
            # self.state.soulscurrent = self.getsoulscurrent()
            # self.state.soulsnext = self.getsoulsnext()
            self.lock.release()
            sleep(2)

    def getlevel(self):
        raw = self.window.grabocr(882, 81, 134, 27)
        self.logger.debug('getlevel read: "{}"'.format(raw))
        num = ''.join(ch for ch in raw if ch.isdigit())
        try:
            return int(num)
        except:
            return 0

    def getmoney(self):
        raw = self.window.grabocr(100, 18, 400, 42)
        self.logger.debug('getmoney read: "{}"'.format(raw))
        raw = raw.replace(' ', '')
        try:
            val = float(raw)
            return val
        except:
            return 0

    def getsoulscurrent(self):
        raw = self.window.grabocr(363, 130, 190, 20)
        self.logger.debug('getsoulscurrent read: "{}"'.format(raw))
        num = ''.join(ch for ch in raw if ch.isdigit())
        try:
            return int(num)
        except:
            return 0

    def getsoulsnext(self):
        raw = self.window.grabocr(363, 150, 190, 20)
        self.logger.debug('getsoulsnext read: "{}"'.format(raw))
        num = ''.join(ch for ch in raw if ch.isdigit())
        try:
            return int(num)
        except:
            return 0

    def readState(self):
        self.lock.acquire()
        o = copy.deepcopy(self.state)
        self.lock.release()
        return o
