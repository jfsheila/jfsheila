import playground
import asyncio
from playground.network.common import StackingProtocol,StackingTransport,StackingProtocolFactory
from playground.network.packet import PacketType
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from Packet import RequestIDProblem, IDQuestion, IDSolution, Result
from playground.network.common import StackingProtocol,StackingTransport,StackingProtocolFactory

class EchoServerProtocol(asyncio.Protocol):

	def connection_made(self,transport):
		print("Echo Server Connected to Client")
		self.transport =transport  
		self.status=0
		self._deserializer=PacketType.Deserializer()
	
	def data_received(self,data):
		print("data received")
		self.data=data
		self._deserializer.update(data)
		for pkt in self._deserializer.nextPackets():
			print (pkt)
			if isinstance(pkt,RequestIDProblem):
				packet2=IDQuestion()
				packet2.ID=pkt.ID
				packet2.question="What is your ID number"
				self.status+=1
				self.transport.write(packet2.__serialize__())
				print ("This is the second packet: What is your ID number?")

			elif isinstance(pkt,IDSolution):
				packet4=Result()
				packet4.ID=pkt.ID
				if pkt.solution=="qqiu3":
					packet4.result=True
					print("This is the last packet: Identification Success")
				else: 
					packet4.result=False
				print("This is the last packet: Identifaction Failed")
				self.transport.write(packet4.__serialize__())
				self.status+=1

			else:
				print("Connection Lost")

	def connection_lost(self,exc):
		self.transport=None
		print("Echo Server Connection Lost because{}".format(exc))


class Passthroughlayer1(StackingProtocol):
	def __init__(self):
		super().__init__

	def connection_made(self,transport):
		#print("c_m")
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
		super().__init__

	def connection_made(self,transport):
		#print("c_m2")
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
loop2=asyncio.get_event_loop()
loop2.set_debug(enabled=True)
print("here")
'''
loop2=asyncio.get_event_loop()
f=StackingProtocolFactory(lambda:Passthroughlayer1(),lambda:Passthroughlayer2())
ptConnector=playground.Connector(protocolStack=f)
playground.setConnector("passthrough",ptConnector)
coro2=playground.getConnector('passthrough').create_playground_server(lambda:EchoServerProtocol(),8009)
loop2.run_until_complete(coro2)
loop2.run_forever()
loop2.close()

