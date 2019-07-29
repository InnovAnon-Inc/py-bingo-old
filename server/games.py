#! /usr/bin/python3

from threading import Lock

class Games(object):
	def __init__(self, lobby):
		self.data  = []
		self.lock  = Lock()
		self.lobby = lobby
	def __repr__(self):
		try:
			self.lock.acquire()
			return "Games(data=%s)" % (self.data,)
		finally: self.lock.release()
	def addGame(self, game):
		try:
			self.lock.acquire()
			self.data.append(game)
		finally: self.lock.release()
		game.games = self
		game.start()
	def removeGame(self, game):
		try:
			self.lock.acquire()
			self.data.remove(game)
		finally: self.lock.release()
		self.lobby.addPlayers(game.players)
	def __iter__(self): return iter(self.data)

if __name__ == "__main__":
	from random import choice
	from threading import Thread
	from time import sleep, strftime, gmtime

	from lobby  import Lobby
	from loop   import Loop
	from player import Player

	lobby = Lobby()
	games = Games(lobby)

	#class Player(object):
	#	def __init__(self, name, sock):
	#		self.name = name
	#		self.sock = sock
	#	def __repr__(self): return "Player(name=%s, sock=%s)" % (self.name, self.sock)
	class Thread1(Loop):
		def __init__(self):
			Loop.__init__(self)
			self.sock = 3
		def loop(self):
			player = Player("abc", self.sock)
			print("[%s] Adding player: %s" % (strftime("%8s", gmtime()), player))
			lobby.addPlayer(self.sock, player)
			self.sock = self.sock + 1
			sleep(5)
	class Game(Thread):
		def __init__(self, players):
			Thread.__init__(self)
			self.players = players
		def run(self):
			sleep(10)
			self.games.removeGame(self)
			winner = choice(self.players)
			print("[%s] game over; winner: %s" % (strftime("%8s", gmtime()), winner))
		def __repr__(self): return "Game(players=%s)" % (self.players,)
	def target2():
		for k in range(10):
			players = lobby.getPlayers(min_n=3, max_n=5, timeout=3, max_timeout=7)
			game = Game(players)
			games.addGame(game)

			print("[%s] #%s %s" % (strftime("%8s", gmtime()), k, game))
			print("[%s] %s %s" % (strftime("%8s", gmtime()), len(lobby), lobby))
			#game.start()
			#game.join()
			#lobby.addPlayers(players)

	t1 = Thread1()
	t2 = Thread(target=target2)

	t1.start()
	t2.start()

	t2.join()
	t1.stop()
	t1.join()
