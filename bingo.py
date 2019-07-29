#! /usr/bin/python3

from loop import Loop
from win_type import WinType

class Bingo(Loop):
	def __init__(self):
		Loop.__init__(self)
	def loop(self):
		pass





#! /usr/bin/python3

from random import shuffle

class WinType:
	ROW       = 1 << 0
	COL       = 1 << 1
	DIAGY     = 1 << 2
	DIAGX     = 1 << 3
	DIAG1     = DIAGY  | DIAGX
	DIAGY2    = 1 << 4
	DIAGX2    = 1 << 5
	DIAG2     = DIAGY2 | DIAGX2
	DIAG      = DIAG1  | DIAG2
	BORDER    = 1 << 6
	TEXAS_T   = 1 << 7
	ST_ANDREW = 1 << 8
	BLACKOUT  = 1 << 9

class Game:
	def isSelected(self, x): return x in self.history
	def gDisplay(self, x): return 'X' if self.isSelected(x) else x
	# TODO expected number of turns till win
	# TODO free cells
	def check_row_win(self, board, width, height):
		for row in board:
			if sum([self.isSelected(x) for x in row]) is len(row): return True
		return False
	def check_col_win(self, board, width, height): return self.check_row_win(zip(*board), width, height)
	def check_diagY_win(self, board, width, height):
		K = min(width, height)
		for Y in range(K - 1, height):
			if sum([self.isSelected(board[y][y]) for y in range(min(Y+1, width))]) is K: return True
		return False
	def check_diagX_win(self, board, width, height): return self.check_diagY_win(list(zip(*board)), width, height)
	def check_diag_win(self, board, width, height): return self.check_diagY_win(board, width, height) or self.check_diagX_win(board, width, height)
	def check_diagY2_win(self, board, width, height): return self.check_diagY_win([row[::-1] for row in board], width, height)
	def check_diagX2_win(self, board, width, height): return self.check_diagY2_win(list(zip(*board)), width, height)
	def check_diag2_win(self, board, width, height): return self.check_diagY2_win(board, width, height) or self.check_diagX2_win(board, width, height)
	def check_t_win(self, board, width, height): return self.check_row_win(board, width, height) and self.check_col_win(board, width, height)
	def check_x_win(self, board, width, height): return self.check_diag_win(board, width, height) and self.check_diag2_win(board, width, height)
	def check_blackout_win(self, board, width, height): return sum([self.isSelected(x) for row in board for x in row]) is width * height

	def __init__(self):
		self.cws = {
			WinType.ROW       : self.check_row_win,
			WinType.COL       : self.check_col_win,
			WinType.DIAGY     : self.check_diagY_win,
			WinType.DIAGX     : self.check_diagX_win,
			WinType.DIAGY2    : self.check_diagY2_win,
			WinType.DIAGX2    : self.check_diagX2_win,
			WinType.TEXAS_T   : self.check_t_win,
			WinType.ST_ANDREW : self.check_x_win,
			WinType.BLACKOUT  : self.check_blackout_win
		}
		width, height = 10, 20
		max = width * height + 30

		self.boards = [Board(width, height, max, self.cws, WinType.COL | WinType.ROW | WinType.DIAG, self.gDisplay) for _ in range(3)]
		#b1 = Board(width, height, max, WinType.ROW & WinType.COL & WinType.DIAG)
		#self.b1 = Board(width, height, max, self.cws, WinType.ROW, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.COL, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.DIAGY, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.DIAGX, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.DIAGY2, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.DIAGX2, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.TEXAS_T, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.ST_ANDREW, self.gDisplay)
		#self.b1 = Board(width, height, max, self.cws, WinType.BLACKOUT, self.gDisplay)
		#print(b1.isValid())
		#b1.display()

		self.history = []
		self.future  = list(range(max))
		shuffle(self.future)
	def checkWin(self):
		for board in self.boards:
			if board.checkWin(): return True
		return False
	def checkWin2(self): return [i for i, board in enumerate(self.boards, start=1) if board.checkWin()]
	def display(self):
		for i, p in enumerate(self.boards, start=1):
			print("Player %s" % i)
			p.display()
			print()
	def gameLoop(self):
		#print("valid=%s" % self.b1.isValid())
		turns = 0
		self.display()
		while not self.checkWin():
			#self.b1.display()
			move = self.future[-1]
			self.future = self.future[:-1]
			self.history.append(move)
			turns = turns + 1
			print("Turn %s; Calling cell: %s" % (turns, move))
			#broadcastMove(move)
			#print()
			self.display()
		#self.b1.display()
		#self.display()
		#print("victory in %s turns" % turns)
		print("Victory in %s turns for player(s): %s" % (turns, self.checkWin2()))

class Board:
	def __init__(self, width, height, max, cws, win, gd):
		self.width  = width
		self.height = height
		self.max    = max
		self.board  = self.randomBoard()
		self.cws    = cws
		self.win    = win
		self.gDisplay = gd
	def randomBoard(self):
		l = list(range(self.max))
		shuffle(l)
		return [[l[y * self.width + x] for x in range(self.width)] for y in range(self.height)]
	def isValid(self):
		history = []
		for row in self.board:
			for k in row:
				if k in history: return False
				history.append(k)
		return True
	def display(self):
		K = len(str(self.max))
		for row in self.board:
			for k in row: print("%*s " % (K, self.gDisplay(k)), end='')
			print()
	def checkWin(self):
		for cw in self.cws:
			if self.win & cw and self.cws[cw](self.board, self.width, self.height): return True
		return False

if __name__ == "__main__":
	#width, height = 10, 20
	#max = width * height + 30
	##b1 = Board(width, height, max, WinType.ROW & WinType.COL & WinType.DIAG)
	#b1 = Board(width, height, max, WinType.ROW)
	#print(b1.isValid())
	#b1.display()
	g = Game()
	g.gameLoop()



