import playground
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING,UINT32,BOOL
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from Packet import RequestIDProblem, IDQuestion, IDSolution, Result
import asyncio

class EchoClientProtocol(asyncio.Protocol):
	def __init__(self):
		self.transport=None

	def connection_made(self,transport):
		self.transport=transport
		self.status=0
		self._deserializer=PacketType.Deserializer()
		packet1=RequestIDProblem()
		packet1.ID=1
		self.transport.write(packet1.__serialize__())

	def data_received(self,data):
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

loop1=asyncio.get_event_loop()
#loop1a=loop1.create_connection(lambda:EchoClientProtocol(),host="127.0.0.1",port=8004)
loop1a=playground.getConnector().create_playground_connection(lambda:EchoClientProtocol(), "20174.1.1.4", 8004)
loop1.run_until_complete(loop1a)
loop1.run_forever()
loop1.close()
