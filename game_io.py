#! /usr/bin/python3

from server_io import ServerIO

class GameIO(ServerIO):
	def __init__(self, lobby, port=9009, timeout=None):
		ServerIO.__init__(self, port=port, timeout=timeout)
		self.lobby = lobby
	def onInit(self, PORT):
		ServerIO.onInit(self, PORT)
	def onClientConnect(self, sock, addr):
		ServerIO.onInit(self, sock, addr)
		self.lobby.addPlayer(sock, Player(sock))
	def onClientMessage(self, sock, data):
		if data.startsWith("/msg "):
			data = data[len("/msg "):]
			ServerIO.onClientMessage(self, sock, data)
			return
		# TODO lobby-related commands
	def onClientDisconnect(self, sock):
		ServerIO.onClientDisconnect(self, sock)
		self.lobby.removePlayer(sock)
		
if __name__ == "__main__":
	from loop_test import LoopTest
	from lobby import Lobby

	lobby = Lobby()
	def consGameIO(timeout=None): return GameIO(lobby, timeout=timeout)
	lt = LoopTest(consGameIO, polling_timeout=3, sleep_time=10)
	lt.start()
	lt.join()
