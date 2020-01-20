#!/usr/bin/python3


from jk_jsoncfghelper2 import *




MAIN_DEF = JDefStructure("authData", structure=[
	JDef("authMethod", dataType="str", required=True),
	JDef("authLogin", dataType="str", required=True),
	JDef("authToken", dataType="str", required=True),
	JDef("info", dataType=JDefStructure("authDataClientInfo", structure=[
		JDef("uid", dataType="int", required=True),
		JDef("uname", dataType="str", required=True),
		JDef("gid", dataType="int", required=True),
		JDef("gname", dataType="str", required=True),
		JDef("pid", dataType="int", required=True),
		JDef("subsystem", dataType="str", required=True),
		JDef("version", dataType="str", required=True),
		JDef("commands", dataType="list", elementTypes=[
			JDefStructure("cmdDef", structure=[
				JDef("description", dataType="str", required=True),
				JDef("cmd", dataType="str", required=True),
				JDef("msgType", dataType="str", required=True),
				JDef("dataResponses", dataType="list", required=False),
				JDef("errorResponses", dataType="list", required=False),
				JDef("errID", dataType="str", required=False),
				JDef("forwardSubsystem", dataType="str", required=False),
				JDef("isForward", dataType="bool", required=False),
			])
		], required=True),
	]), required=True)
])




scmgr = compileFromDefs(MAIN_DEF)
print("Elements:")
for name in scmgr:
	print("\t" + name)

print()



checker = scmgr.get("authData")

print("Errors:")
n = 0
for path, message in checker.check({
	"authMethod": "plaintext",
	"authLogin": "somebody",
	"authToken": "abc123ghj789",
	"info": {
		"uid": 0,
		"uname": "root",
		"gid": 0,
		"gname": "root",
		"pid": 12345,
		"subsystem": "abc",
		"version": "0.2019.11.1",
		"commands": [
		]
	}
}):
	print("\t" + path + ": " + message)
	n += 1

if n == 0:
	print("\t(no errors)")




