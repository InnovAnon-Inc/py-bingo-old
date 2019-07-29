#! /usr/bin/python3

# Socket server in python using select function

#from abc    import ABCMeta
#from abc    import abstractmethod
from select import select
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from socket import socket

from common.loop import Loop

#class ServerIO(Loop, metaclass=ABCMeta):
class ServerIO(Loop):
	def __init__(self, recv_buffer=4096, listen="0.0.0.0", port=5000, timeout=None):
		Loop.__init__(self)

		CONNECTION_LIST = []	# list of socket clients
		#RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
		#PORT = 5000
		PORT = port
		
		server_socket = socket(AF_INET, SOCK_STREAM)
		# this has no effect, why ?
		server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		server_socket.bind((listen, PORT))
		server_socket.listen(10)

		# Add server socket to the list of readable connections
		CONNECTION_LIST.append(server_socket)

		self.connection_list = CONNECTION_LIST
		self.recv_buffer     = recv_buffer
		self.server_socket   = server_socket
		self.timeout         = timeout
		self.onInit(PORT)
	#@abstractmethod
	def onInit(self, PORT):
		print("Chat server started on port " + str(PORT))

		self.addrs = {}
	#@abstractmethod
	def onClientConnect(self, sock, addr):
		print("Client (%s, %s) connected" % addr)
		self.addrs[sock] = addr
	#@abstractmethod
	def onClientMessage(self, sock, data):
		sock.send(b'OK ... ' + data)
	#@abstractmethod
	def onClientDisconnect(self, sock):
		addr = self.addrs[sock]
		del self.addrs[sock]
		# TODO
		broadcast_data(sock, "Client (%s, %s) is offline" % addr)
		print("Client (%s, %s) is offline" % addr)
		
	def loop(self):
		CONNECTION_LIST = self.connection_list
		RECV_BUFFER     = self.recv_buffer
		server_socket   = self.server_socket

		# Get the list sockets which are ready to be read through select
		select_args = (CONNECTION_LIST, [], [])
		if self.timeout: select_args = (*select_args, self.timeout)
		#read_sockets,write_sockets,error_sockets = select(CONNECTION_LIST, [], [], self.timeout)
		read_sockets,write_sockets,error_sockets = select(*select_args)

		for sock in read_sockets:
			#if not self.running: break
			
			#New connection
			if sock == server_socket:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				self.onClientConnect(sockfd, addr)
				
			#Some incoming message from a client
			else:
				# Data recieved from client, process it
				try:
					#In Windows, sometimes when a TCP program closes abruptly,
					# a "Connection reset by peer" exception will be thrown
					data = sock.recv(RECV_BUFFER)
					# echo back the client message
					if data: self.onClientMessage(sock, data)
				
				# client disconnected, so remove from socket list
				except:
					self.onClientDisconnect(sock)
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue
	def stop(self):
		Loop.stop(self)
		self.server_socket.close()

if __name__ == "__main__":
	from loop_test import LoopTest

	lt = LoopTest(ServerIO, polling_timeout=3, sleep_time=10)
	lt.start()
	lt.join()
