from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..games.game import Game
from ..engine.solid import Solid
from ..common.event import EventDispatcher
from ..common.events import InputEvent
from ..renderer.renderer import Renderer

class TestGame(Game):
	DELTA = 10
	def __init__(self, event_dispatcher):
		super(TestGame, self).__init__(event_dispatcher, "TestGame")
		self._engine = GameEngine()

	def setup(self):
		event_dispatcher = EventDispatcher()
		event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)

		resolution = Renderer().getGameResolution()

		self._p1 = self._engine.createRectangle(Vector(25, 200))
		self._p1.position = Vector(-300, 0)
		self._p2 = self._engine.createRectangle(Vector(25, 200))
		self._p2.position = Vector(300, 0)

		self._ball = self._engine.createCircle(50)
		self._ball.getComponent(Solid).velocity = Vector(400,100)

		thickness = 50
		self._engine.createRectangle(Vector(resolution.x, thickness)).position = Vector(0, -resolution.y / 2)
		self._engine.createRectangle(Vector(resolution.x, thickness)).position = Vector(0, resolution.y / 2)
		self._engine.createRectangle(Vector(thickness, resolution.y)).position = Vector(-resolution.x / 2, 0)
		self._engine.createRectangle(Vector(thickness, resolution.y)).position = Vector(resolution.x / 2, 0)

	def update(self):
		return

	def processInputEvent(self, event):
		if event == InputEvent.W:
			self._p1.position.y -= self.DELTA
			return
		elif event == InputEvent.A:
			return
		elif event == InputEvent.S:
			self._p1.position.y += self.DELTA
			return
		elif event == InputEvent.D:
			return
		elif event == InputEvent.I:
			self._p2.position.y -= self.DELTA
			return
		elif event == InputEvent.J:
			return
		elif event == InputEvent.K:
			self._p2.position.y += self.DELTA
			return
		elif event == InputEvent.L:
			return
		return