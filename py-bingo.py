#! /usr/bin/python3

from time import sleep

from py_client import Client
from py_server import Server

if __name__ == "__main__":
	s = Server()
	s.start()

	sleep(3)
	c = Client()
	c.start()

	c.join()
	s.stop()
