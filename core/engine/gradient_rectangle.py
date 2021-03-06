from ..engine.component import Component
from ..engine.primitive import Rectangle
from ..renderer.color import Color
from ..engine.vector import Vector

class GradientRectangle(Component):
	def __init__(self, game_object):
		super(GradientRectangle, self).__init__(game_object)
		self.start_color = Color.WHITE
		self.end_color = Color.BLACK
		self.step = 100
		self.dimensions = Vector()
