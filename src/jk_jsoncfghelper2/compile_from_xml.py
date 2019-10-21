

import jk_xmlparser
from jk_simplexml import *
from .value_checkers import *






def _compile_int(scmgr:StructureCheckerManager, x:HElement):
	minValue = None
	if x.hasAttribute("minValue"):
		minValue = int(x.getAttributeValue("minValue"))

	maxValue = None
	if x.hasAttribute("maxValue"):
		maxValue = int(x.getAttributeValue("maxValue"))

	allowedValues = None
	if x.hasAttribute("allowedValues"):
		allowedValues = [ int(i) for i in x.getAttributeValue("allowedValues").split(",") ]

	required = True
	if x.hasAttribute("required"):
		s = x.getAttributeValue("required")
		if (s == "true") or (s == "1") or (s == "yes"):
			required = True
		elif (s == "false") or (s == "0") or (s == "no"):
			required = False
		else:
			raise Exception("Invalid value specified for 'required': " + repr(s))

	return IntValueChecker(minValue=minValue, maxValue=maxValue, required=required)
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
		allowedValues = [ float(i) for i in x.getAttributeValue("allowedValues").split(",") ]

	required = True
	if x.hasAttribute("required"):
		s = x.getAttributeValue("required")
		if (s == "true") or (s == "1") or (s == "yes"):
			required = True
		elif (s == "false") or (s == "0") or (s == "no"):
			required = False
		else:
			raise Exception("Invalid value specified for 'required': " + repr(s))

	return FloatValueChecker(minValue=minValue, maxValue=maxValue, required=required)
#



def _compile_bool(scmgr:StructureCheckerManager, x:HElement):
	required = True
	if x.hasAttribute("required"):
		s = x.getAttributeValue("required")
		if (s == "true") or (s == "1") or (s == "yes"):
			required = True
		elif (s == "false") or (s == "0") or (s == "no"):
			required = False
		else:
			raise Exception("Invalid value specified for 'required': " + repr(s))

	return BooleanValueChecker(required=required)
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
		allowedValues = [ s for s in x.getAttributeValue("allowedValues").split(",") ]

	required = True
	if x.hasAttribute("required"):
		s = x.getAttributeValue("required")
		if (s == "true") or (s == "1") or (s == "yes"):
			required = True
		elif (s == "false") or (s == "0") or (s == "no"):
			required = False
		else:
			raise Exception("Invalid value specified for 'required': " + repr(s))

	return StringValueChecker(minLength=minLength, maxLength=maxLength, allowedValues=allowedValues, required=required)
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
		allowedElementTypes = [ s for s in x.getAttributeValue("elementTypes").split(",") ]

	required = True
	if x.hasAttribute("required"):
		s = x.getAttributeValue("required")
		if (s == "true") or (s == "1") or (s == "yes"):
			required = True
		elif (s == "false") or (s == "0") or (s == "no"):
			required = False
		else:
			raise Exception("Invalid value specified for 'required': " + repr(s))

	return ListValueChecker(minLength=minLength, maxLength=maxLength, allowedElementTypes=allowedElementTypes, required=required)
#



def _compile_dict(scmgr:StructureCheckerManager, t:AbstractValueChecker, x:HElement):
	t = t.cloneObject()

	t.required = True
	if x.hasAttribute("required"):
		s = x.getAttributeValue("required")
		if (s == "true") or (s == "1") or (s == "yes"):
			t.required = True
		elif (s == "false") or (s == "0") or (s == "no"):
			t.required = False
		else:
			raise Exception("Invalid value specified for 'required': " + repr(s))

	return t
#



def _compile_eq(structureName:str, checker:DictionaryValueChecker, x:HElement):
	fieldName = x.getAttributeValue("field")
	sFieldValue = x.getAllText()

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

		if dataType in [ "int", "integer" ]:
			children[name] = _compile_int(scmgr, xChild)
		elif dataType == "float":
			children[name] = _compile_float(scmgr, xChild)
		elif dataType in [ "bool", "boolean" ]:
			children[name] = _compile_bool(scmgr, xChild)
		elif dataType in [ "str", "string" ]:
			children[name] = _compile_str(scmgr, xChild)
		elif dataType in [ "list" ]:
			children[name] = _compile_list(scmgr, xChild)
		else:
			t = scmgr.get(dataType)
			if t is None:
				raise Exception("Unknown data type: " + repr(dataType))
			else:
				children[name] = _compile_dict(scmgr, t, xChild)

	checker = DictionaryValueChecker(children, structType=x.name)

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

	xRoot = _xmlParser.parseFile(filePath)
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

	xRoot = _xmlParser.parseText(rawText)
	assert isinstance(xRoot, HElement)

	for x in xRoot.children:
		if isinstance(x, HElement):
			# print("Registering: " + x.name)
			scmgr.register(x.name, _compileDef(scmgr, x))

	return scmgr
#









