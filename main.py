from common.camera import Camera
from common.debug import Debugger
from common.debug import PerformanceLogger
from threading import Thread
from logicThread import LogicThread
from common.event import EventDispatcher
from common.inputEvent import InputEvent
from common.drawEvent import DrawEvent
from common.periodSync import PeriodSync
import numpy as np 
import pygame
import picamera
import sys

class Birthday29():
    def run(self):
        pygame.init()
        #screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screenAttributes = 0
        screen = pygame.display.set_mode(Camera.RESOLUTION_HI, screenAttributes)
        debugger = Debugger()
        displayLogger = PerformanceLogger('Display')
        
        self._running = True

        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)
        event_dispatcher.add_event_listener(DrawEvent.TYPE, self.processDrawEvent)
        
        logicThread = LogicThread(event_dispatcher)
        logicThread.setDaemon(True)
        logicThread.start()

        self.surface = None
        period_sync = PeriodSync()
        while(self._running):
            period_sync.Start()

            displayLogger.startLog()
            if not self.surface == None:
                screen.blit(self.surface, (0,0), (0,0,self.surface.get_width(),self.surface.get_height()))
            debugger.clear()
            pygame.display.update()
            displayLogger.endLog()
            debugger.append(displayLogger.getLog() + ' ')

            period_sync.End()
            period_sync.Sync()

        logicThread.stop()
        logicThread.join()
        pygame.quit()

    def processDrawEvent(self, event):
        self.surface = pygame.image.frombuffer(event.data(), Camera.RESOLUTION_LO, 'RGB')

    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            self._running = False
            pygame.quit()
            sys.exit()
        if event == InputEvent.Q:
            self._running = False

if (__name__ == "__main__"):
    Birthday29().run()
