#! /usr/bin/python3

import pygame
import pygame.locals

from abc    import ABCMeta
from abc    import abstractmethod
#from random import randrange
from select import select
from socket import socket
from socket import AF_INET, SOCK_STREAM

from common.loop import Loop

class GameClient(Loop, metaclass=ABCMeta):
	def __init__(self, addr="localhost", serverport=4321):
		Loop.__init__(self)

		#self.clientport = randrange(8000, 8999)
		self.conn = socket(AF_INET, SOCK_STREAM)
		# Bind to localhost - set to external ip to connect from other computers
		self.conn.connect((addr, serverport))
		self.addr       = addr
		self.serverport = serverport

		self.read_list  = [self.conn]
		self.write_list = []

		self.setup_pygame()
		self.clock = pygame.time.Clock()
		self.tickspeed = 30

		# Initialize connection to server
		print("init connection to server")
		self.conn.send("/msg c".encode())
	def setup_pygame(self, width=400, height=300):
		self.screen = pygame.display.set_mode((width, height))
		self.bg_surface = pygame.image.load("bg.jpg").convert()

		#self.image = pygame.image.load("sprite.png").convert_alpha()

		pygame.event.set_allowed(None)
		pygame.event.set_allowed([pygame.locals.QUIT,
		                          pygame.locals.KEYDOWN])
		pygame.key.set_repeat(50, 50)
	def loop(self):
		self.conn.send(b"/msg c")

		self.clock.tick(self.tickspeed)

		# select on specified file descriptors
		# TODO timeout
		readable, writable, exceptional = (
			select(self.read_list, self.write_list, [], 0)
		)
		#print("readable.length: %s" % len(readable))
		for f in readable:
			if f is self.conn:
				msg, addr = f.recvfrom(32)
				self.screen.blit(self.bg_surface, (0, 0)) # Draw the background

				print("msg: " + msg)
				self.display(msg)

				#for position in msg.split('|'):
				#	x, sep, y = position.partition(',')
					#try: self.screen.blit(self.image, (int(x), int(y)))
					#except: pass # If something goes wrong, don't draw anything.

		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.locals.QUIT:
				self.stop()
				break
			elif event.type == pygame.locals.KEYDOWN:
				#if event.key == pygame.local.K_UP
				# TODO
				pygame.event.clear(pygame.locals.KEYDOWN)

		pygame.display.update()
	@abstractmethod
	def display(self, msg): raise Exception()
	def stop(self):
		Loop.stop(self)
		self.conn.send(b"/msg d")

if __name__ == "__main__":
	g = GameClient()
	g.start()
	g.join()
