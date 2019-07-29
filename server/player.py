#! /usr/bin/python3

from server.lotto    import Lotto
from server.win_type import WinType

class Player(object):
	def __init__(self, name, sock):
		self.name    = name
		self.sock    = sock
		self.history = []
	def toStringI(self, history, x): return "%3s" % ("X" if WinType.isSelected(x, history) else x,)
	def toString(self, history): return "\n".join([" ".join([self.toStringI(history, x) for x in row]) for row in self.board])
	def __repr__(self): return "Player(name=%s, sock=%s); board=\n%s\n" % (self.name, self.sock, self.toString(self.history))
	def createBoard(self, width, height, extra):
		lotto = Lotto.getLotto(width, height, extra)
		self.board  = [[lotto.doTurn() for x in range(width)] for y in range(height)]
		self.width  = width
		self.height = height
		# TODO free space
	def doMove(self, move):
		self.history.append(move)
		# TODO
		self.sock.send(str(self))
		pass
	def checkWin(self, history): return WinType.isWin(self.wc, history, self.board, self.width, self.height)

if __name__ == "__main__": print(Player(name="Frank", sock=12))
