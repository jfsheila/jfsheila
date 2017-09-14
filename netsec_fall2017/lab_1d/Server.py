import asyncio
import playground
from playground.network.packet import PacketType
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from Packet import RequestIDProblem, IDQuestion, IDSolution, Result

class EchoServerProtocol(asyncio.Protocol):

	def connection_made(self,transport):
		print("Echo Server Connected to Client")
		self.transport =transport  
		self.status=0
		self._deserializer=PacketType.Deserializer()
	
	def data_received(self,data):
		self._deserializer.update(data)
		for pkt in self._deserializer.nextPackets():
			print (pkt)
			if isinstance(pkt,RequestIDProblem):
				packet2=IDQuestion()
				packet2.ID=pkt.ID
				packet2.question="What is your ID number"
				self.status+=1
				self.transport.write(packet2.__serialize__())

			elif isinstance(pkt,IDSolution):
				packet4=Result()
				packet4.ID=pkt.ID
				if pkt.solution=="qqiu3":
					packet4.result=True
				else: 
					packet4.result=False
					
				self.transport.write(packet4.__serialize__())
				self.status+=1

			else:
				print("Connection Lost")

	def connection_lost(self,exc):
		self.transport=None
		print("Echo Server Connection Lost because{}".format(exc))
		
loop2=asyncio.get_event_loop()
#loop2x=loop2.create_server(lambda:EchoServerProtocol(),port=8004)
loop2x=playground.getConnector().create_playground_server(lambda:EchoServerProtocol(),8004)
loop2.run_until_complete(loop2x)
loop2.run_forever()
loop2.close()
