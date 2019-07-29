#! /usr/bin/python3

class Player(object):
	def __init__(self, name, sock):
		self.name = name
		self.sock = sock
	def __repr__(self): return "Player(name=%s, sock=%s)" % (self.name, self.sock)

if __name__ == "__main__": print(Player(name="Frank", sock=12))
