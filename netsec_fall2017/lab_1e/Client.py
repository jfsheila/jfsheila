import playground
import asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING,UINT32,BOOL
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from Packet import RequestIDProblem, IDQuestion, IDSolution, Result
from playground.network.common import StackingProtocol,StackingTransport,StackingProtocolFactory


class EchoClientProtocol(asyncio.Protocol):
	def __init__(self):
		self.transport=None

	def connection_made(self,transport):
		print("connection made!")
		self.transport=transport
		self.status=0
		self._deserializer=PacketType.Deserializer()
		packet1=RequestIDProblem()
		packet1.ID=1
		self.transport.write(packet1.__serialize__())

	def data_received(self,data):
		print("data received!")
		self.data=data
		self._deserializer.update(data)
		for pkt in self._deserializer.nextPackets():
			print (pkt)
			if isinstance(pkt,IDQuestion):
				packet3=IDSolution()
				packet3.ID=pkt.ID
				packet3.solution="qqiu3"
				self.status+=1
				self.transport.write(packet3.__serialize__())

			elif isinstance(pkt,Result):
				print(pkt.result)
				print("Successful")
				self.status+=1

			else:
				print("Connection Lost")


	def connection_lost(self,exc):
		self.transport=None
		print ("Echo Client Connection Lostbecase{}.".format(exc))


class Passthroughlayer1(StackingProtocol):
	def __init__(self):
		super().__init__()

	def connection_made(self,transport):
		self.transport=transport
		higherTransport = StackingTransport(self.transport)		
		self.higherProtocol().connection_made(higherTransport)
		print("passthroughlayer1 connection_made success")
	
	def data_received(self,data):
		self.data=data
		self.higherProtocol().data_received(self.data)
		print("passthroughlayer1 data_receive success")
	
	def connection_lost(self,exc):
		self.higherProtocol().connection_lost(exc)
		print("Passthroughlayer1 connection_lost success")

class Passthroughlayer2(StackingProtocol):
	def __init__(self):
		super().__init__()

	def connection_made(self,transport):
		self.transport=transport
		higherTransport = StackingTransport(self.transport)	
		self.higherProtocol().connection_made(higherTransport)
		print("passthroughlayer2 connection_made success")
	
	def data_received(self,data):
		self.data=data
		self.higherProtocol().data_received(data)
		print("passthroughlayer2 data_received success")
	
	def connection_lost(self,exc):
		self.higherProtocol().connection_lost(exc)
		print("Passthroughlayer2 connection_lost success")
'''
import logging, sys
logging.getLogger().setLevel(logging.NOTSET)
logging.getLogger().addHandler(logging.StreamHandler())
print("here")
logging.getLogger().critical("test")
'''
loop1=asyncio.get_event_loop()
loop1.set_debug(enabled=True)
f=StackingProtocolFactory(lambda:Passthroughlayer1(),lambda:Passthroughlayer2())
ptConnector=playground.Connector(protocolStack=f)
playground.setConnector("passthrough",ptConnector)
coro1=playground.getConnector("passthrough").create_playground_connection(lambda:EchoClientProtocol(), "20174.1.1.1", 8009)
loop1.run_until_complete(coro1)
loop1.run_forever()
loop1.close()
