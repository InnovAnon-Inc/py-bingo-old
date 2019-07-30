#! /usr/bin/python3

from client.game_client import GameClient
from common.loop        import Loop

class Client(GameClient):
	def __init__(self, port=9617):
		GameClient.__init__(self, serverport=port)
	def display(self, msg):
		# TODO
		print(msg)

if __name__ == "__main__":
	c = Client()
	c.start()
	c.join()
