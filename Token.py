# Copyright 2017 Dhvani Patel

class Token():

	def __init__(self, type, value, srow, scol, erow, ecol, line):
	        self.type = type
		self.value = value
		self.srow = srow
		self.scol = scol
		self.erow = erow
		self.ecol = ecol
		self.line = line
   	def __eq__(self, other) : 
		if self.type == other.type:
			if self.value == other.value:
				if self.srow == other.srow:
					if self.scol == other.scol:
						if self.erow == other.erow:
							if self.ecol == other.ecol:
								if self.line == other.line:
									return True
		else:
			return False	 

