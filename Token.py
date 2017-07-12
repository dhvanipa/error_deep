
class Token():


# __slots__ = 'start', 'end'

	def __init__(self, type, value, srow, scol, erow, ecol, line):
	        self.type = type
		self.value = value
		self.srow = srow
		self.scol = scol
		self.erow = erow
		self.ecol = ecol
		self.line = line
