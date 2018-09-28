from .common import config
from .common.event import EventDispatcher
from .common.events import *
from .engine.game_engine import GameEngine
from .games.game_manager import GameManager
from .input.input_manager import InputManager
from .renderer.renderer import Renderer
from .sync.period_sync import PeriodSync

import os
import pygame
import signal
import time

class Main(object):
    def setFullScreen(self, enable):
        config.FULL_SCREEN = enable

    def run(self):
        pygame.mixer.pre_init(44100, -16, 2, 1)
        pygame.mixer.init()
        pygame.init()

        EventDispatcher().add_event_listener(KeyDownEvent.TYPE, self.onKeyDownEvent)

        managers = [
            InputManager(),
            GameManager(),
            GameEngine(),
            Renderer(),
        ]

        for manager in managers:
            manager.setup()

        self._running = True
        period_sync = PeriodSync()
        while self._running:
            period_sync.Start()
            for manager in managers:
                manager.update()
            period_sync.End()
            period_sync.Sync()

        for manager in managers:
            manager.stop()

        pygame.quit()
    
    def onKeyDownEvent(self, event):
        if event.data() == Key.Q:
            self._running = False
