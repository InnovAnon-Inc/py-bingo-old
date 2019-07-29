#! /usr/bin/python3

from time import gmtime, sleep, strftime

from game    import Game
from games   import Games
from game_io import GameIO
from lobby   import Lobby
from loop    import Loop

class GameServer(Loop):
	def __init__(self, MyGame, min_n=1, max_n=100, polling_timeout=5, max_timeout=60, port=4321, timeout=None):
		Loop.__init__(self)

		self.lobby  = Lobby()
		self.games  = Games(self.lobby)
		self.io     = GameIO(self.lobby, port=port, timeout=timeout)

		self.MyGame = MyGame
		self.ngame  = 0

		self.min_n  = min_n
		self.max_n  = max_n
		self.polling_timeout = polling_timeout
		self.max_timeout     = max_timeout
	def loop(self):
		players = self.lobby.getPlayers(min_n=self.min_n, max_n=self.max_n, timeout=self.polling_timeout, max_timeout=self.max_timeout)
		if len(players) < self.min_n:
			print("%s players => no games" % len(players))
			return
		game    = self.MyGame(players)
		self.games.addGame(game)
		self.ngame = self.ngame + 1

		print("[%s] #%s %s" % (strftime("%8s", gmtime()), self.ngame, game))
		print("[%s] %s %s" % (strftime("%8s", gmtime()), len(self.lobby), self.lobby))
	def stop(self):
		Loop.stop(self)
		self.io.stop()
		for game in self.games: game.stop()
		self.lobby.stop()

if __name__ == "__main__":
	from loop_test import LoopTest

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

	def consServer(timeout=None): return GameServer(MyGame=MyGame, min_n=1, max_n=5, polling_timeout=1, max_timeout=10, timeout=timeout)
	lt = LoopTest(consServer, polling_timeout=3, sleep_time=10)
	lt.start()
	lt.join()
