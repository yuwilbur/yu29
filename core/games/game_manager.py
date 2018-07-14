from ..common.event import EventDispatcher
from ..common.events import InputEvent
from ..games.test_game import TestGame
from ..sync.manager import Manager

class GameManager(Manager):
	def __init__(self):
		super(GameManager, self).__init__()
		self._event_dispatcher = EventDispatcher()
		self._event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)
		self._game = None

	def setup(self):
		self.startGame(TestGame(self._event_dispatcher))

	def stop(self):
		self.stopGame()

	def stopGame(self):
		if not self._game == None:
			self._game.stop()
			self._game.join()

	def startGame(self, game):
		self.stopGame()
		self._game = game
		self._game.setDaemon(True)
		self._game.start()

	def processInputEvent(self, event):
		if event == InputEvent.ONE:
			self.startGame(TestGame(self._event_dispatcher))