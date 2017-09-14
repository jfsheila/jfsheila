import asyncio
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.packet import PacketType
from playground.network.testing import MockTransportToProtocol
from playground.network.packet.fieldtypes import STRING,UINT32,BOOL

class RequestIDProblem(PacketType):
	DEFINITION_IDENTIFIER ="lab1b.Qianrui.MyPacket1"
	DEFINITION_VERSION="1.0"
	FIELDS = [("ID",UINT32)]

class IDQuestion(PacketType):
	DEFINITION_IDENTIFIER ="lab1b.Qianrui.MyPacket2"
	DEFINITION_VERSION="1.0"
	FIELDS=[("ID",UINT32),("question",STRING)]

class IDSolution(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.Qianrui.MyPacket3"
	DEFINITION_VERSION="1.0"
	FIELDS=[("ID",UINT32),("solution",STRING)]

class Result(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.Qianrui.MyPacket4"
	DEFINITION_VERSION="1.0"
	FIELDS=[("ID",UINT32),("result",BOOL)]


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
				self.status+=1

			else:
				print("Connection Lost")


	def connection_lost(self,exc):
		self.transport=None
		print ("Echo Client Connection Lostbecase{}.".format(exc))



class EchoServerProtocol(asyncio.Protocol):
	def __init__(self):
		self.transport=None


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


def basicUnitTest():
	asyncio.set_event_loop(TestLoopEx())
	client=EchoClientProtocol()
	server=EchoServerProtocol()

	transportToServer=MockTransportToProtocol(server)
	transportToClient=MockTransportToProtocol(client)

	server.connection_made(transportToClient)
	client.connection_made(transportToServer)
	
#	packet1=RequestIDProblem()
#	packet1.ID=1
#	client.transport.write(packet1.__serizalize__())

	assert client.status==2
	assert server.status==2


if __name__=="__main__":
	basicUnitTest()
	print ("Test Successful.")


