#! /usr/bin/python3

from random import shuffle

class Lotto(object):
	def __init__(self, n):
		self.history = []
		self.future  = list(range(n))
		shuffle(self.future)
	def doTurn(self):
		move = self.future[-1]
		self.future = self.future[:-1]
		self.history.append(move)
		return move
	@staticmethod
	def getLotto(width, height, extra): return Lotto(width * height + extra)
	def __len__(self): return len(self.future)

if __name__ == "__main__":
	l = Lotto(10)
	while l: print(l.doTurn())
