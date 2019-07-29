#! /usr/bin/python3

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
	# TODO box/border win
	BLACKOUT  = 1 << 9

	BLANK_SPACE = -1

	@staticmethod
	def isSelected(x, history): return x is WinType.BLANK_SPACE or x in history

	@staticmethod
	def check_row_win(isSelected, board):
		for row in board:
			if sum([isSelected(x) for x in row]) is len(row): return True
		return False
	@staticmethod
	def check_col_win(isSelected, board): return WinType.check_row_win(isSelected, zip(*board))
	@staticmethod
	def check_diagY_win(isSelected, board, width, height):
		K = min(width, height)
		for Y in range(K - 1, height):
			if sum([isSelected(board[y][y]) for y in range(min(Y+1, width))]) is K: return True
		return False
	@staticmethod
	def check_diagX_win(isSelected, board, width, height): return WinType.check_diagY_win(isSelected, list(zip(*board)), width, height)
	@staticmethod
	def check_diag_win(isSelected, board, width, height): return WinType.check_diagY_win(isSelected, board, width, height) or WinType.check_diagX_win(isSelected, board, width, height)
	@staticmethod
	def check_diagY2_win(isSelected, board, width, height): return WinType.check_diagY_win(isSelected, [row[::-1] for row in board], width, height)
	@staticmethod
	def check_diagX2_win(isSelected, board, width, height): return WinType.check_diagY2_win(isSelected, list(zip(*board)), width, height)
	@staticmethod
	def check_diag2_win(isSelected, board, width, height): return WinType.check_diagY2_win(isSelected, board, width, height) or WinType.check_diagX2_win(isSelected, board, width, height)
	@staticmethod
	def check_diagXX_win(isSelected, board, width, height): return WinType.check_diagX_win(isSelected, board, width, height) or WinType.check_diagX2_win(isSelected, board, width, height)
	@staticmethod
	def check_diagYY_win(isSelected, board, width, height): return WinType.check_diagY_win(isSelected, board, width, height) or WinType.check_diagY2_win(isSelected, board, width, height)
	@staticmethod
	def check_t_win(isSelected, board): return WinType.check_row_win(isSelected, board) and WinType.check_col_win(isSelected, board)
	@staticmethod
	def check_x_win(isSelected, board, width, height): return WinType.check_diag_win(isSelected, board, width, height) and WinType.check_diag2_win(isSelected, board, width, height)
	#def check_x_win(isSelected, board, width, height): return WinType.check_diagXX_win(isSelected, board, width, height) and WinType.check_diagYY_win(isSelected, board, width, height)
	# TODO box/border win
	@staticmethod
	def check_blackout_win(isSelected, board, width, height): return sum([isSelected(x) for row in board for x in row]) is width * height
	@staticmethod
	def getWinTypes(history):
		s = lambda x: WinType.isSelected(x, history)
		return {
			WinType.ROW       : lambda board, width, height: WinType.check_row_win     (s, board),
			WinType.COL       : lambda board, width, height: WinType.check_col_win     (s, board),
			WinType.DIAGY     : lambda board, width, height: WinType.check_diagY_win   (s, board, width, height),
			WinType.DIAGX     : lambda board, width, height: WinType.check_diagX_win   (s, board, width, height),
			WinType.DIAGY2    : lambda board, width, height: WinType.check_diagY2_win  (s, board, width, height),
			WinType.DIAGX2    : lambda board, width, height: WinType.check_diagX2_win  (s, board, width, height),
			WinType.TEXAS_T   : lambda board, width, height: WinType.check_t_win       (s, board),
			WinType.ST_ANDREW : lambda board, width, height: WinType.check_x_win       (s, board, width, height),
			WinType.BLACKOUT  : lambda board, width, height: WinType.check_blackout_win(s, board, width, height)
		}
	@staticmethod
	def isWin(winTypes, history, board, width, height):
		wcs = WinType.getWinTypes(history)
		for flag, wc in wcs.items():
			if winTypes & flag and wc(board, width, height): return True
		return False
	@staticmethod
	def toString(wt):
		wts = {
			WinType.ROW       : "ROW",
			WinType.COL       : "COL",
			WinType.DIAGY     : "DIAG-Y",
			WinType.DIAGX     : "DIAG-X",
			WinType.DIAGY2    : "DIAG-Y2",
			WinType.DIAGX2    : "DIAG-X2",
			WinType.TEXAS_T   : "TEXAS-T",
			WinType.ST_ANDREW : "ST. ANDREW",
			WinType.BLACKOUT  : "BLACKOUT"
		}
		return " ".join([w for f, w in wts.items() if wt & f])

if __name__ == "__main__":
	board = [
		[ 1,  2,  3,  4,  5],
		[ 6,  7,  8,  9, 10],
		[11, 12, 13, 14, 15],
		[16, 17, 18, 19, 20]]
	print("board: %s" % (board,))

	row = [3, 8, 13, 18]
	col = [11, 12, 13, 14, 15]
	d1  = [1, 7, 13, 19]
	d2  = [16, 12, 8, 4]
	d3  = [2, 8, 14, 20]
	d4  = [5, 9, 13, 17]
	
	for history in [row, col, d1, d2, d3, d4, row + col, d1 + d2, d3 + d4, d1 + d4, d2 + d3]:
		print("history: %s" % (history,))
		for wt in [WinType.ROW, WinType.COL, WinType.DIAG, WinType.TEXAS_T, WinType.ST_ANDREW, WinType.BLACKOUT]:
			win = WinType.isWin(wt, history, board, 5, 4)
			print("%s: %s", (WinType.toString(wt), win))

