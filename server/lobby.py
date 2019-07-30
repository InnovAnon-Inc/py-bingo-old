#! /usr/bin/python3

from threading import Lock
from time      import sleep

class Lobby(object):
	def __init__(self):
		self.data  = {}
		self.lock  = Lock()
		self.alive = True
	def addPlayer(self, sock, player):
		print("lobby.addPlayer(%s, %s)" % (sock, player))
		try:
			self.lock.acquire()
			self.data[sock] = player
		finally: self.lock.release()
	def removePlayer(self, sock):
		print("lobby.removePlayer(%s)" % (sock,))
		try:
			self.lock.acquire()
			p = self.data[sock]
			del self.data[sock]
		finally: self.lock.release()
		return p
	def getPlayers(self, min_n=2, max_n=10, timeout=1, max_timeout=None):
		print("lobby.getPlayers()")
		total_timeout = 0
		players       = []
		timeout_flag  = False

		def isEnoughPlayers(): return len(players) >= min_n
		def isMaxTimeout():    return not max_timeout or total_timeout >= max_timeout
		def isTimeOut():       return timeout_flag

		while self.alive and not isEnoughPlayers() or (not isTimeOut() and not isMaxTimeout()):
			timeout_flag = True
			try:
				self.lock.acquire()
				i = iter(self.data)
				m = min(max_n - len(players), len(self.data))
				socks = [next(i) for _ in range(m)]
				players = players + [self.data[sock] for sock in socks]
				for sock in socks: del self.data[sock]
				if m: timeout_flag = False
			finally: self.lock.release()

			print("done polling; players: %s" % (players,))
			if isEnoughPlayers(): break

			if max_timeout:
				t = max(0, max_timeout - total_timeout)
				t = min(t, timeout)
			else: t = timeout
			sleep(t)
			total_timeout = total_timeout + t
		return players
	def addPlayers(self, players):
		try:
			self.lock.acquire()
			for player in players: self.data[player.sock] = player
		finally: self.lock.release()
	def __repr__(self):
		try:
			self.lock.acquire()
			return "Lobby(data=%s)" % (self.data,)
		finally: self.lock.release()
	def __len__(self):
		try:
			self.lock.acquire()
			return len(self.data)
		finally: self.lock.release()
	def stop(self): self.alive = False
		
if __name__ == "__main__":
	from threading import Thread
	from time import strftime, gmtime

	from loop   import Loop
	from player import Player

	lobby = Lobby()

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
		def run(self): sleep(10)
		def __repr__(self): return "Game(players=%s)" % (self.players,)
	def target2():
		for k in range(10):
			players = lobby.getPlayers(min_n=3, max_n=5, timeout=3, max_timeout=7)
			game = Game(players)
			print("[%s] #%s %s" % (strftime("%8s", gmtime()), k + 1, game))
			print("[%s] %s %s" % (strftime("%8s", gmtime()), len(lobby), lobby))
			game.start()
			game.join()
			lobby.addPlayers(players)

	t1 = Thread1()
	t2 = Thread(target=target2)

	t1.start()
	t2.start()

	t2.join()
	t1.stop()
	t1.join()
