#! /usr/bin/python3

from server.game     import Game
from server.lotto    import Lotto
from server.win_type import WinType

class Bingo(Game):
	def __init__(self, players, width=5, height=5, extra=50, wc=WinType.ROW | WinType.COL | WinType.DIAG):
		Game.__init__(self, players)

		self.lotto = Lotto.getLotto(width, height, extra)

		for player in self.players:
			player.createBoard(width, height, extra)
			player.wc = wc
	def doTurn(self):
		move = self.lotto.doTurn()
		for player in self.players: player.doMove(move)
	def isEnd(self):
		for player in self.players:
			if player.checkWin(self.lotto.history): return True
		return False
	def endSequence(self):
		Game.endSequence(self)
		for player in self.players:
			if player.checkWin(self.lotto.history): print("Winner: %s" % player)

if __name__ == "__main__":
	from time import sleep
	from random import randint

	from player import Player

	from games import Games
	from lobby import Lobby
	lobby = Lobby()
	games = Games(lobby)

	G = []

	for _ in range(5):
		players = [Player(name=None, sock=randint(3, 100)) for _ in range(3)]
		g = Bingo(players)
		g.games = games
		G.append(g)

	for g in G:
		print(g)
		games.addGame(g)

