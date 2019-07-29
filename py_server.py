#! /usr/bin/python3

from server.bingo       import Bingo
from server.game_server import GameServer

class Server(GameServer):
	def __init__(self, port=9617, timeout=None):
		GameServer.__init__(self, MyGame=Bingo, port=port, timeout=timeout)

if __name__ == "__main__":
	s = Server()
	try:     s.start()
	finally: s.join()
