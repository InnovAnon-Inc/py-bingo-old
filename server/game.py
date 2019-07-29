#! /usr/bin/python3

from abc import ABCMeta
from abc import abstractmethod
from time import gmtime, strftime

from common.loop import Loop

class Game(Loop, metaclass=ABCMeta):
	def __init__(self, players):
		Loop.__init__(self)
		self.players = players
		self.turns = 0
	def loop(self):
		if self.isEnd():
			self.endSequence()
			self.stop()
			return
		self.turns = self.turns + 1
		self.doTurn()
	def stop(self):
		Loop.stop(self)
		self.games.removeGame(self)
	def __repr__(self): return "Game(players=%s)" % (self.players,)
	@abstractmethod
	def doTurn(self): raise Error()
	@abstractmethod
	def isEnd(self): raise Error()
	def endSequence(self): print("[%s] game over" % (strftime("%8s", gmtime()),))
		

if __name__ == "__main__":
	#class Player(object):
	#	def __init__(self, sock): self.sock = sock
	#	def __repr__(self): return "Player(sock=%s)" % (self.sock,)
	from time import sleep
	from random import randint

	from player import Player

	from games import Games
	from lobby import Lobby
	lobby = Lobby()
	games = Games(lobby)

	class MyGame(Game):
		def __init__(self, players, max_score=19, max_turns=5):
			Game.__init__(self, players)
			self.max_turns = max_turns
			self.max_score = max_score
			for player in self.players: player.score = 0
		def doTurn(self):
			for player in self.players: player.score = player.score + randint(-10, 10)
			sleep(1)
		def isEnd(self):
			if self.turns == self.max_turns: return True
			for player in self.players:
				if player.score > self.max_score: return True
			return False
		def endSequence(self):
			Game.endSequence(self)
			print("%s turns / %s max turns" % (self.turns, self.max_turns))
			for player in self.players:
				if player.score > self.max_score:
					print("score: %s %s" % (player.score, player))

			

	G = []

	for _ in range(5):
		players = [Player(name=None, sock=randint(3, 100)) for _ in range(3)]
		g = MyGame(players, max_turns=randint(5, 10))
		g.games = games
		G.append(g)

	for g in G:
		print(g)
		games.addGame(g)

