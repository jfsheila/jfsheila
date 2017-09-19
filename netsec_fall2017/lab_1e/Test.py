import asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING,UINT32,BOOL
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from Packet import RequestIDProblem, IDQuestion, IDSolution, Result 
from Client import EchoClientProtocol
from Server import EchoServerProtocol


def basicUnitTest():
	asyncio.set_event_loop(TestLoopEx())
	client=EchoClientProtocol()
	server=EchoServerProtocol()

	transportToServer=MockTransportToProtocol(server)
	transportToClient=MockTransportToProtocol(client)

	server.connection_made(trnasportToClient)
	client.connection_made(transportToServer)

	assert client.status==2
	assert server.status==2


if __name__=="__main__":
	basicUnitTest()
	print ("Test Successful.")



