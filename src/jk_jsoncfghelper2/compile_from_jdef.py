

from jk_testing import Assert
from jk_simplexml import *
from .value_checkers import *
from .jdef import *





def _compile_null(scmgr:StructureCheckerManager, x:JDef):
	Assert.isEqual(x.dataType, "null")
	#assert x.dataType == "null"

	return NullValueChecker(scmgr, required=x.required)
#



def _compile_int(scmgr:StructureCheckerManager, x:JDef):
	Assert.isIn(x.dataType, [ "int", "integer" ])
	#assert x.dataType in [ "int", "integer" ]

	return IntValueChecker(scmgr, minValue=x.minValue, maxValue=x.maxValue, required=x.required, nullable=x.nullable)
#



def _compile_float(scmgr:StructureCheckerManager, x:JDef):
	Assert.isEqual(x.dataType, "float")
	#assert x.dataType == "float"

	return FloatValueChecker(scmgr, minValue=x.minValue, maxValue=x.maxValue, required=x.required, nullable=x.nullable)
#



def _compile_bool(scmgr:StructureCheckerManager, x:JDef):
	Assert.isIn(x.dataType, [ "bool", "boolean" ])
	#assert x.dataType in [ "bool", "boolean" ]

	return BooleanValueChecker(scmgr, required=x.required, nullable=x.nullable)
#



def _compile_str(scmgr:StructureCheckerManager, x:JDef):
	Assert.isIn(x.dataType, [ "str", "string" ])
	#assert x.dataType in [ "str", "string" ]

	return StringValueChecker(scmgr, minLength=x.minLength, maxLength=x.maxLength, allowedValues=x.allowedValues, required=x.required, nullable=x.nullable)
#



def __compile_allowedElements(scmgr:StructureCheckerManager, allowedElementTypes:list):
	if allowedElementTypes is None:
		return None

	ret = []
	for et in allowedElementTypes:
		if isinstance(et, str):
			ret.append(et)
		elif isinstance(et, JDefStructure):
			if et.name not in scmgr:
				t = _compileDefStructure(scmgr, et)
				scmgr.register(et.name, t)
			ret.append(et.name)
		else:
			raise Exception("Allowed element specified is of unknown type: " + repr(et.__class__.__name__))

	return ret
#


def _compile_list(scmgr:StructureCheckerManager, x:JDef):
	Assert.isEqual(x.dataType, "list")
	#assert x.dataType == "list"

	return ListValueChecker(scmgr, minLength=x.minLength, maxLength=x.maxLength, allowedElementTypes=__compile_allowedElements(scmgr, x.elementTypes), required=x.required, nullable=x.nullable)
#



def _compile_anydict(scmgr:StructureCheckerManager, x:JDef):
	Assert.isIn(x.dataType, [ "dict", "dictionary" ])
	#assert x.dataType in [ "dict", "dictionary" ]

	return AnyDictionaryValueChecker(scmgr, required=x.required, allowedElementTypes=__compile_allowedElements(scmgr, x.elementTypes), nullable=x.nullable)
#



def _compile_specificdict(scmgr:StructureCheckerManager, t:AbstractValueChecker, x:JDef):
	t = t.cloneObject()

	t.required = x.required
	t.nullable = x.nullable

	return t
#



def compileFromDef(x:JDef):
	scmgr = StructureCheckerManager()

	if isinstance(x.dataType, JDefStructure):
		raise Exception()
	elif x.dataType in [ "null" ]:
		return _compile_null(scmgr, x)
	elif x.dataType in [ "int", "integer" ]:
		return _compile_int(scmgr, x)
	elif x.dataType == "float":
		return _compile_float(scmgr, x)
	elif x.dataType in [ "bool", "boolean" ]:
		return _compile_bool(scmgr, x)
	elif x.dataType in [ "str", "string" ]:
		return _compile_str(scmgr, x)
	elif x.dataType in [ "list" ]:
		return _compile_list(scmgr, x)
	elif x.dataType in [ "dict", "dictionary", "obj", "object" ]:
		return _compile_anydict(scmgr, x)
	else:
		raise Exception()
#



def _compileDefStructure(scmgr:StructureCheckerManager, x:JDefStructure):
	#print("Compiling structure: " + x.name)

	children = {}

	for xChild in x.structure:
		if not isinstance(xChild, JDef):
			continue

		name = xChild.name
		dataType = xChild.dataType
		if dataType is None:
			raise Exception("No data type specified for " + x.name + ":" + name)

		#print("\t> field ", repr(name), ":", dataType)

		if isinstance(dataType, JDefStructure):
			# if we encounter a JDefStructure: compile it if it has not yet been compiled
			t = scmgr.get(dataType.name)
			if t is None:
				t = _compileDefStructure(scmgr, dataType)
				scmgr.register(dataType.name, t)
			children[name] = _compile_specificdict(scmgr, t, xChild)
		elif dataType in [ "null" ]:
			children[name] = _compile_null(scmgr, xChild)
		elif dataType in [ "int", "integer" ]:
			children[name] = _compile_int(scmgr, xChild)
		elif dataType == "float":
			children[name] = _compile_float(scmgr, xChild)
		elif dataType in [ "bool", "boolean" ]:
			children[name] = _compile_bool(scmgr, xChild)
		elif dataType in [ "str", "string" ]:
			children[name] = _compile_str(scmgr, xChild)
		elif dataType in [ "list" ]:
			children[name] = _compile_list(scmgr, xChild)
		elif dataType in [ "dict", "dictionary", "obj", "object" ]:
			children[name] = _compile_anydict(scmgr, xChild)
		else:
			t = scmgr.get(dataType)
			if t is None:
				raise Exception("Unknown data type: " + repr(dataType))
			else:
				children[name] = _compile_specificdict(scmgr, t, xChild)

	checker = SpecificDictionaryValueChecker(scmgr, children, structType=x.name)

	return checker
#



def compileFromDefs(defOrDefs, scmgr:StructureCheckerManager = None) -> StructureCheckerManager:
	if isinstance(defOrDefs, (list, tuple)):
		pass
	else:
		defOrDefs = [ defOrDefs ]

	if scmgr is None:
		scmgr = StructureCheckerManager()

	for x in defOrDefs:
		if isinstance(x, JDefStructure):
			# print("Registering: " + x.name)
			scmgr.register(x.name, _compileDefStructure(scmgr, x))
		else:
			raise Exception("Unknown type: " + str(x.__class__.__name__))

	return scmgr
#










