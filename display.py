#!/usr/bin/env python
from enum import Enum

from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

import threading
import Queue
from time import *

class SuspendState(Enum):
    Suspend = 0
    Running = 1

class SuspendHelper:
    def __init__(self):
        self.disp = Display()
        self.root = self.disp.screen().root
        self.state = SuspendState.Running

        print 'starting event listen thread...'
        t = threading.Thread(target=self.listenThread)
        t.daemon = True
        t.start()

        self.suspendQueue = Queue.Queue()


    def listenThread(self):
        self.ctx = self.disp.record_create_context(
                    0,
                    [record.AllClients],
                    [{
                            'core_requests': (0, 0),
                            'core_replies': (0, 0),
                            'ext_requests': (0, 0, 0, 0),
                            'ext_replies': (0, 0, 0, 0),
                            'delivered_events': (0, 0),
                            'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
                            'errors': (0, 0),
                            'client_started': False,
                            'client_died': False,
                    }])
        self.disp.record_enable_context(self.ctx, self.handler)
        self.disp.record_free_context(self.ctx)


    def handler(self, reply):
        """ This function is called when a xlib event is fired """
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.disp.display, None, None)

            # KEYCODE IS FOUND USERING event.detail
            if event.type == X.KeyPress and event.detail == 33:
                self.suspendQueue.put(event)

    def handle_event(self, event):
        print event.detail

    def process(self):

        while not self.suspendQueue.empty():
            self.suspendQueue.get()
            if self.state == SuspendState.Suspend:
                self.state = SuspendState.Running
                print 'resuming...'
            else:
                self.state = SuspendState.Suspend
                print 'suspended...'


        if self.state == SuspendState.Suspend:
            # wait until resumed
            while True:
                if not self.suspendQueue.empty():
                    break
                sleep(0.1)
