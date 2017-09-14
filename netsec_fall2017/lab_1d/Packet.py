from playground.network.packet import PacketType
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
