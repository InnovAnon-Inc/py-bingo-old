#! /usr/bin/python3

from client import Client
from server import Server

if __name__ == "__main__":
	s = Server()
	s.start()

	c = Client()
	c.start()

	c.join()
	s.stop()
