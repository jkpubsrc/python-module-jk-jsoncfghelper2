

import jk_xmlparser
from jk_simplexml import *
from .value_checkers import *




def __xml_getBooleanAttribute(x:HElement, attrName:str, defaultValue:bool) -> bool:
	if x.hasAttribute(attrName):
		s = x.getAttributeValue(attrName)
		if (s == "true") or (s == "1") or (s == "yes"):
			return True
		elif (s == "false") or (s == "0") or (s == "no"):
			return False
		else:
			raise Exception("Invalid value specified for " + repr(attrName) + ": " + repr(s))
	else:
		return defaultValue
#




def _compile_null(scmgr:StructureCheckerManager, x:HElement):
	required = __xml_getBooleanAttribute(x, "required", True)

	return NullValueChecker(scmgr, required=required, nullable=True)
#



def _compile_int(scmgr:StructureCheckerManager, x:HElement):
	minValue = None
	if x.hasAttribute("minValue"):
		minValue = int(x.getAttributeValue("minValue"))

	maxValue = None
	if x.hasAttribute("maxValue"):
		maxValue = int(x.getAttributeValue("maxValue"))

	allowedValues = None
	if x.hasAttribute("allowedValues"):
		allowedValues = [ int(i.strip()) for i in x.getAttributeValue("allowedValues").split(",") ]

	required = __xml_getBooleanAttribute(x, "required", True)

	nullable = __xml_getBooleanAttribute(x, "nullable", False)

	return IntValueChecker(scmgr, minValue=minValue, maxValue=maxValue, required=required, nullable=nullable)
#



def _compile_float(scmgr:StructureCheckerManager, x:HElement):
	minValue = None
	if x.hasAttribute("minValue"):
		minValue = float(x.getAttributeValue("minValue"))

	maxValue = None
	if x.hasAttribute("maxValue"):
		maxValue = float(x.getAttributeValue("maxValue"))

	allowedValues = None
	if x.hasAttribute("allowedValues"):
		allowedValues = [ float(i.strip()) for i in x.getAttributeValue("allowedValues").split(",") ]

	required = __xml_getBooleanAttribute(x, "required", True)

	nullable = __xml_getBooleanAttribute(x, "nullable", False)

	return FloatValueChecker(scmgr, minValue=minValue, maxValue=maxValue, required=required, nullable=nullable)
#



def _compile_bool(scmgr:StructureCheckerManager, x:HElement):
	required = __xml_getBooleanAttribute(x, "required", True)

	nullable = __xml_getBooleanAttribute(x, "nullable", False)

	return BooleanValueChecker(scmgr, required=required, nullable=nullable)
#



def _compile_str(scmgr:StructureCheckerManager, x:HElement):
	minLength = None
	if x.hasAttribute("minLength"):
		minLength = int(x.getAttributeValue("minLength"))

	maxLength = None
	if x.hasAttribute("maxLength"):
		maxLength = int(x.getAttributeValue("maxLength"))

	allowedValues = None
	if x.hasAttribute("allowedValues"):
		allowedValues = [ s.strip() for s in x.getAttributeValue("allowedValues").split(",") ]

	required = __xml_getBooleanAttribute(x, "required", True)

	nullable = __xml_getBooleanAttribute(x, "nullable", False)

	return StringValueChecker(scmgr, minLength=minLength, maxLength=maxLength, allowedValues=allowedValues, required=required, nullable=nullable)
#



def _compile_list(scmgr:StructureCheckerManager, x:HElement):
	minLength = None
	if x.hasAttribute("minLength"):
		minLength = int(x.getAttributeValue("minLength"))

	maxLength = None
	if x.hasAttribute("maxLength"):
		maxLength = int(x.getAttributeValue("maxLength"))

	allowedElementTypes = None
	if x.hasAttribute("elementTypes"):
		allowedElementTypes = [ s.strip() for s in x.getAttributeValue("elementTypes").split(",") ]

	required = __xml_getBooleanAttribute(x, "required", True)

	nullable = __xml_getBooleanAttribute(x, "nullable", False)

	return ListValueChecker(scmgr, minLength=minLength, maxLength=maxLength, allowedElementTypes=allowedElementTypes, required=required, nullable=nullable)
#



def _compile_anydict(scmgr:StructureCheckerManager, x:HElement):
	required = __xml_getBooleanAttribute(x, "required", True)

	nullable = __xml_getBooleanAttribute(x, "nullable", False)

	allowedElementTypes = None
	if x.hasAttribute("elementTypes"):
		allowedElementTypes = [ s.strip() for s in x.getAttributeValue("elementTypes").split(",") ]

	return AnyDictionaryValueChecker(scmgr, required=required, allowedElementTypes=allowedElementTypes, nullable=nullable)
#



def _compile_specificdict(scmgr:StructureCheckerManager, t:AbstractValueChecker, x:HElement):
	t = t.cloneObject()

	t.required = __xml_getBooleanAttribute(x, "required", True)
	t.nullable = __xml_getBooleanAttribute(x, "nullable", False)

	return t
#



def _compile_eq(structureName:str, checker:SpecificDictionaryValueChecker, x:HElement):
	fieldName = x.getAttributeValue("field")
	sFieldValue = x.getAllText().strip()

	if fieldName in checker.children:
		field = checker.children[fieldName]
		v = field.parseValueFromStr(sFieldValue)
		return ValueCondition(fieldName, v)
	else:
		raise Exception("No such field in structure " + structureName + ": " + repr(fieldName))
#



def _compileDef(scmgr:StructureCheckerManager, x:HElement):
	#print("Compiling structure: " + x.name)

	xStructure = x.getChildElement("STRUCTURE")
	xCondition = x.getChildElement("CONDITION")
	children = {}

	for xChild in xStructure.children:
		if not isinstance(xChild, HElement):
			continue

		name = xChild.name
		dataType = xChild.getAttributeValue("dataType")
		if dataType is None:
			raise Exception("No data type specified for " + x.name + ":" + name)

		#print("\t> field ", repr(name), ":", dataType)

		if dataType in [ "null" ]:
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

	if xCondition is not None:
		conditions = []
		for xChild in xCondition.children:
			if not isinstance(xChild, HElement):
				continue

			name = xChild.name
			#print("\t> condition ", repr(name))

			if name == "eq":
				conditions.append(_compile_eq(x.name, checker, xChild))
			else:
				raise Exception("Unknown condition: " + repr(name))

		checker.conditions = conditions

	return checker
#



_xmlParser = jk_xmlparser.XMLDOMParser()

def loadFromXMLFile(filePath:str, scmgr:StructureCheckerManager = None) -> StructureCheckerManager:
	assert isinstance(filePath, str)

	if scmgr is None:
		scmgr = StructureCheckerManager()

	with open(filePath, "r") as f:
		rawText = f.read()
	rawText = rawText.strip()
	xRoot = _xmlParser.parseText(rawText)
	#xRoot = _xmlParser.parseFile(filePath)
	assert isinstance(xRoot, HElement)

	for x in xRoot.children:
		if isinstance(x, HElement):
			# print("Registering: " + x.name)
			scmgr.register(x.name, _compileDef(scmgr, x))

	return scmgr
#

def loadFromXMLStr(rawText:str, scmgr:StructureCheckerManager = None) -> StructureCheckerManager:
	assert isinstance(rawText, str)

	if scmgr is None:
		scmgr = StructureCheckerManager()

	rawText = rawText.strip()
	xRoot = _xmlParser.parseText(rawText)
	assert isinstance(xRoot, HElement)

	for x in xRoot.children:
		if isinstance(x, HElement):
			# print("Registering: " + x.name)
			scmgr.register(x.name, _compileDef(scmgr, x))

	return scmgr
#









