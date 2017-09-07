from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING,UINT32,BOOL

class RequestIDProblem(PacketType):
	DEFINITION_IDENTIFIER ="lab1b.Qianrui.MyPacket1"
	DEFINITION_VERSION="1.0"
	FIELDS = []

class IDQuestion(PacketType):
	DEFINITION_IDENTIFIER ="lab1b.Qianrui.MyPacket2"
	DEFINITION_VERSION="1.0"
	FIELDS=[("ID",UINT32),("question",STRING)]

class IDSolution(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.Qianrui.MyPacket3"
	DEFINITION_VERSION="1.0"
	FIELDS=[("ID",UINT32),("IDnumber",STRING)]

class Result(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.Qianrui.MyPacket4"
	DEFINITION_VERSION="1.0"
	FIELDS=[("ID",UINT32),("result",BOOL)]

def basicUnitTest():
	packet1=RequestIDProblem()
	packet1Bytes=packet1.__serialize__()
	packet1a=RequestIDProblem.Deserialize(packet1Bytes)
	assert packet1 ==packet1a
	print ("These two packets1 are the same")

	packet2=IDQuestion()
	packet2.question="What's your member ID?"
	packet2.ID=1
	packet2Bytes=packet2.__serialize__()
	packet2a=IDQuestion.Deserialize(packet2Bytes)
	if packet2a==packet2:
		print("These two packets2 are the same")

	packet3=IDSolution()
	packet3.IDnumber="qqiu3"
	packet3.ID=2
	packet3Bytes=packet3.__serialize__()
	packet3a=IDSolution.Deserialize(packet3Bytes)
	if packet3a ==packet3:
		print("These two packets3 are the same")

	packet4=Result()
	packet4.result=True
	packet4.ID=3
	packet4Bytes=packet4.__serialize__()
	packet4a=Result.Deserialize(packet4Bytes)
	assert packet4==packet4a
	print("These two packets4 are the same")

	pktBytes = packet1.__serialize__()+packet2.__serialize__()+packet3.__serialize__()+packet4.__serialize__()
	deserializer =PacketType.Deserializer()
	deserializer.update(pktBytes)
	for packet in deserializer.nextPackets():
		print("got a packet!")
		if packet ==packet1:print("It's packet 1!")
		elif packet ==packet2:print("It's packet 2!")
		elif packet ==packet3:print("It's packet 3!")
		elif packet ==packet4:print("It's packet 4!")

	
if __name__=="__main__":
	basicUnitTest()

	
