#! /usr/bin/python3

from threading import Thread
from time      import sleep

class LoopTest(Thread):
	def __init__(self, S, polling_timeout=1, sleep_time=3):
		Thread.__init__(self)
		
		self.s = S(timeout=polling_timeout)
		self.t = Thread(target=lambda: sleep(sleep_time))

	def start(self):
		print("starting threads")
		self.s.start()
		self.t.start()

	def join(self):
		print("waiting...")
		self.t.join()

		print("time is up")
		self.s.stop()

		print("joining server thread")
		self.s.join()

		print("done")

if __name__ == "__main__":
	from server_io import ServerIO

	lt = LoopTest(ServerIO)
	lt.start()
	lt.join()
