#! /usr/bin/python3

from py_client import Client
from py_server import Server

if __name__ == "__main__":
	s = Server()
	s.start()

	c = Client()
	c.start()

	c.join()
	s.stop()
