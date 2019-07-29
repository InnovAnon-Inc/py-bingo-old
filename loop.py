#! /usr/bin/python3

from abc       import ABCMeta
from abc       import abstractmethod
from threading import Thread

class Loop(Thread, metaclass=ABCMeta):
	def __init__(self):
		Thread.__init__(self)
		self.running = True
	def run(self):
		while self.running: self.loop()
	def stop(self): self.running = False
	@abstractmethod
	def loop(self): raise Error()

if __name__ == "__main__":
	from loop_test import LoopTest
	from server_io import ServerIO

	lt = LoopTest(ServerIO, polling_timeout=2, sleep_time=5)
	lt.start()
	lt.join()
