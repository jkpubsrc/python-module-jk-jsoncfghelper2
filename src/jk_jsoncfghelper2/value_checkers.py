

import re

from jk_testing import Assert




class IStructureCheckerManager(object):

	def get(self, name:str) -> "AbstractValueChecker":
		raise NotImplementedError()
	#

	def getE(self, name:str) -> "AbstractValueChecker":
		raise NotImplementedError()
	#

	def __in__(self, key:str) -> bool:
		raise NotImplementedError()
	#

	def __iter__(self):
		raise NotImplementedError()
	#

	def list(self) -> list:
		raise NotImplementedError()
	#

#





class AbstractCondition(object):

	def check(self, data:dict):
		raise NotImplementedError()
	#

#

class ValueCondition(AbstractCondition):

	def __init__(self, fieldName:str, value):
		self.__fieldName = fieldName
		self.__value = value
	#

	def check(self, data:dict):
		if not isinstance(data, dict):
			return False
		if self.__fieldName in data:
			return data.get(self.__fieldName) == self.__value
		else:
			return False
	#

#






class AbstractValueChecker(object):

	def __init__(self, scmgr:IStructureCheckerManager):
		assert isinstance(scmgr, IStructureCheckerManager)

		self._scmgr = scmgr
		self._bCompiled = False
	#

	def dump(self, prefix:str = "", printFunc = None):
		raise NotImplementedError()
	#

	def parseValueFromStr(self, s:str):
		raise NotImplementedError()
	#

	def _compile(self, scmgr, path:list):
		self._bCompiled = True
		return
		yield
	#

	def _matchType(self, value):
		raise NotImplementedError()
	#

	def _check(self, scmgr, path:list, value):
		raise NotImplementedError()
	#

	def _isinstance(self, v, typeOrTypes):
		if isinstance(typeOrTypes, (tuple, list)):
			for t in typeOrTypes:
				if v.__class__ == t:
					return True
			return False
		else:
			return v.__class__ == typeOrTypes
	#

	def check(self, value):
		ret = [ (".".join(a), b) for a, b in list(self._compile(self._scmgr, [])) ]
		yield from ret
		if not ret:
			ret = [ (".".join(a), b) for a, b in list(self._check(self._scmgr, [], value)) ]
			yield from ret
	#

	def checkB(self, value, printFunc = None) -> bool:
		bSuccess = True

		if not self._bCompiled:
			for path, msg in self._compile(self._scmgr, []):
				bSuccess = False
				if printFunc:
					printFunc(repr(".".join(path)) + ": " + msg)
				else:
					print(repr(".".join(path)) + ": " + msg)

		if bSuccess:
			for path, msg in self._check(self._scmgr, [], value):
				bSuccess = False
				if printFunc:
					printFunc(repr(".".join(path)) + ": " + msg)
				else:
					print(repr(".".join(path)) + ": " + msg)

		return bSuccess
	#

	def checkE(self, value):
		if not self._bCompiled:
			for path, msg in self._compile(self._scmgr, []):
				raise Exception(repr(".".join(path)) + ": " + msg)

		for path, msg in self._check(self._scmgr, [], value):
			raise Exception(repr(".".join(path)) + ": " + msg)
	#

#

class AbstractNumericValueChecker(AbstractValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager, pythonTypeOrTypes, humanReadableTypeNames, minValue = None, maxValue = None, allowedValues:list = None,
		required:bool = True, nullable:bool = False):

		super().__init__(scmgr)

		self.required = required
		self.nullable = nullable
		self.pythonTypeOrTypes = pythonTypeOrTypes
		self.humanReadableTypeNames = humanReadableTypeNames
		self.minValue = minValue
		self.maxValue = maxValue
		self.allowedValues = allowedValues
	#

	def dump(self, prefix:str = "", printFunc = None):
		if printFunc is None:
			printFunc = print

		printFunc(prefix + ">> " + self.humanReadableTypeNames + " >> "
			+ " minValue=" + str(self.minValue)
			+ " maxValue=" + str(self.maxValue)
			+ " allowedValues=" + str(self.allowedValues)
			+ " required=" + str(self.required)
			+ " nullable=" + str(self.nullable))
	#

	def _matchType(self, value):
		if value is None:
			if self.nullable:
				return True
			else:
				return False
		else:
			return self._isinstance(value, self.pythonTypeOrTypes)
	#

	def _check(self, scmgr, path:list, value):
		if value is None:
			if not self.nullable:
				yield path, "must not be null"
				return
		else:
			if not self._isinstance(value, self.pythonTypeOrTypes):
				yield path, repr(value) + " is not of type " + self.humanReadableTypeNames
				return

			if self.minValue is not None:
				if value < self.minValue:
					yield path, str(value) + " is lower than " + str(self.minValue)
					return
			if self.maxValue is not None:
				if value > self.maxValue:
					yield path, str(value) + " is greater than " + str(self.maxValue)
					return
			if self.allowedValues is not None:
				if not value in self.allowedValues:
					yield path, str(value) + " is not in " + str(self.allowedValues)
	#

#

class IntValueChecker(AbstractNumericValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager, minValue:int = None, maxValue:int = None, allowedValues:list = None,
		required:bool = True, nullable:bool = False):

		super().__init__(scmgr, int, "integer", minValue, maxValue, allowedValues, required, nullable)
	#

	def parseValueFromStr(self, s:str):
		return int(s)
	#

#

class FloatValueChecker(AbstractNumericValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager, minValue:float = None, maxValue:float = None, allowedValues:list = None,
		required:bool = True, nullable:bool = False):

		super().__init__(scmgr, (float, int), "float", minValue, maxValue, allowedValues, required, nullable)
	#

	def parseValueFromStr(self, s:str):
		return float(s)
	#

#

class StringValueChecker(AbstractValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager, minLength:int = None, maxLength:int = None, allowedValues:list = None,
		required:bool = True, nullable:bool = False):

		super().__init__(scmgr)

		self.required = required
		self.nullable = nullable
		self.minLength = minLength
		self.maxLength = maxLength
		self.allowedValues = allowedValues
	#

	def dump(self, prefix:str = "", printFunc = None):
		if printFunc is None:
			printFunc = print

		printFunc(prefix + ">> string >>"
			+ " minLength=" + str(self.minLength)
			+ " maxLength=" + str(self.maxLength)
			+ " allowedValues=" + str(self.allowedValues)
			+ " required=" + str(self.required)
			+ " nullable=" + str(self.nullable))
	#

	def parseValueFromStr(self, s:str):
		return s
	#

	def _matchType(self, value):
		if value is None:
			if self.nullable:
				return True
			else:
				return False
		else:
			return self._isinstance(value, str)
	#

	def _check(self, scmgr, path:list, value):
		if value is None:
			if not self.nullable:
				yield path, "must not be null"
				return
		else:
			if not self._isinstance(value, str):
				yield path, repr(value) + " is not of type string"
				return

			if self.minLength is not None:
				if len(value) < self.minLength:
					yield path, repr(value) + " is shorter than " + str(self.minLength)
					return
			if self.maxLength is not None:
				if len(value) > self.maxLength:
					yield path, repr(value) + " is longer than " + str(self.maxLength)
					return
			if self.allowedValues is not None:
				if not value in self.allowedValues:
					yield path, repr(value) + " is not in " + str(self.allowedValues)
	#

#

class BooleanValueChecker(AbstractValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager,
		required:bool = True, nullable:bool = False):

		super().__init__(scmgr)

		self.required = required
		self.nullable = nullable
	#

	def dump(self, prefix:str = "", printFunc = None):
		if printFunc is None:
			printFunc = print

		printFunc(prefix + ">> boolean >>"
			+ " required=" + str(self.required)
			+ " nullable=" + str(self.nullable))
	#

	def parseValueFromStr(self, s:str):
		if (s == "true") or (s == "1") or (s == "yes"):
			return True
		if (s == "false") or (s == "0") or (s == "no"):
			return False
		raise Exception("Not a boolean value: " + repr(s))
	#

	def _matchType(self, value):
		if value is None:
			if self.nullable:
				return True
			else:
				return False
		else:
			return self._isinstance(value, bool)
	#

	def _check(self, scmgr, path:list, value):
		if value is None:
			if not self.nullable:
				yield path, "must not be null"
				return
		else:
			if not self._isinstance(value, bool):
				yield path, repr(value) + " is not of type boolean"
	#

#

class NullValueChecker(AbstractValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager,
		required:bool = True, nullable:bool = False):

		super().__init__(scmgr)

		self.required = required
		self.nullable = nullable
	#

	def dump(self, prefix:str = "", printFunc = None):
		if printFunc is None:
			printFunc = print

		printFunc(prefix + ">> null >>"
			+ " required=" + str(self.required)
			+ " nullable=" + str(self.nullable))
	#

	def parseValueFromStr(self, s:str):
		if s is not None:
			raise Exception("Not a boolean value: " + repr(s))
	#

	def _matchType(self, value):
		return value is None
	#

	def _check(self, scmgr, path:list, value):
		if value is not None:
			yield path, repr(value) + " is not null"
	#

#

class ListValueChecker(AbstractValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager, minLength:int = None, maxLength:int = None, allowedElementTypes:list = None,
		required:bool = True, nullable:bool = False):

		super().__init__(scmgr)

		self.required = required
		self.nullable = nullable
		self.minLength = minLength
		self.maxLength = maxLength
		self.allowedElementTypes = allowedElementTypes
		self.__allowedElementTypes = None
	#

	def dump(self, prefix:str = "", printFunc = None):
		if printFunc is None:
			printFunc = print

		printFunc(prefix + ">> list >>"
			+ " minLength=" + str(self.minLength)
			+ " maxLength=" + str(self.maxLength)
			+ " allowedElementTypes=" + str(self.allowedElementTypes)
			+ " required=" + str(self.required)
			+ " nullable=" + str(self.nullable))
	#

	def parseValueFromStr(self, s:str):
		raise Exception("Lists can not be represented as strings")
	#

	def _compile(self, scmgr, path:list):
		types = []		# receives compiled list of types

		bHasError = False
		if self.allowedElementTypes is not None:
			for typeName in self.allowedElementTypes:
				t = scmgr.get(typeName)
				if t is None:
					yield path, "Unknown type: " + repr(typeName)
					bHasError = True
				else:
					types.append(t)

		if not bHasError:
			self.__allowedElementTypes = types if types else None
			for t in types:
				for path, msg in t._compile(scmgr, path):
					yield path, msg
					bHasError = True

		if not bHasError:
			self._bCompiled = True
	#

	def _matchType(self, value):
		if value is None:
			if self.nullable:
				return True
			else:
				return False
		else:
			return self._isinstance(value, (list, tuple))
	#

	def _check(self, scmgr, path:list, value):
		if value is None:
			if not self.nullable:
				yield path, "must not be null"
				return
		else:
			if not self._isinstance(value, (tuple, list)):
				yield path, "value is not of type list"
				return

			if self.minLength is not None:
				if len(value) < self.minLength:
					yield path, "list is shorter than " + str(self.minLength)
					return

			if self.maxLength is not None:
				if len(value) > self.maxLength:
					yield path, "list is longer than " + str(self.maxLength)
					return

			if self.__allowedElementTypes is not None:
				for i, v in enumerate(value):
					if v is None:
						yield self.__modifyPath(path, i), "must not be null"
						continue
					bFound = False
					for t in self.__allowedElementTypes:
						if t._matchType(v):
							yield from t._check(scmgr, self.__modifyPath(path, i), v)
							bFound = True
							break
					if not bFound:
						yield self.__modifyPath(path, i), "item is of invalid type"
	#

	def __modifyPath(self, path:list, i:int):
		ret = list(path)
		ret[-1] = ret[-1] + "[" + str(i) + "]"
		return ret
	#

#

class AnyDictionaryValueChecker(AbstractValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager, required:bool = True, allowedElementTypes:list = None,
		nullable:bool = False):
	
		super().__init__(scmgr)

		self.required = required
		self.nullable = nullable
		self.allowedElementTypes = allowedElementTypes
		self.__allowedElementTypes = None
	#

	def dump(self, prefix:str = "", printFunc = None):
		if printFunc is None:
			printFunc = print

		printFunc(prefix + ">> dictionary >>"
			+ " allowedElementTypes=" + str(self.allowedElementTypes)
			+ " required=" + str(self.required)
			+ " nullable=" + str(self.nullable))
	#

	def parseValueFromStr(self, s:str):
		raise Exception("Dictionaries can not be represented as strings")
	#

	def _compile(self, scmgr, path:list):
		types = []		# receives compiled list of types

		bHasError = False
		if self.allowedElementTypes is not None:
			for typeName in self.allowedElementTypes:
				t = scmgr.get(typeName)
				if t is None:
					yield path, "Unknown type: " + repr(typeName)
					bHasError = True
				else:
					types.append(t)

		if not bHasError:
			self.__allowedElementTypes = types if types else None
			for t in types:
				for path, msg in t._compile(scmgr, path):
					yield path, msg
					bHasError = True

		if not bHasError:
			self._bCompiled = True
	#

	def _matchType(self, value):
		if value is None:
			if self.nullable:
				return True
			else:
				return False
		else:
			return self._isinstance(value, dict)
	#

	def _check(self, scmgr, path:list, value):
		if value is None:
			if not self.nullable:
				yield path, "must not be null"
				return
		else:
			if not self._isinstance(value, dict):
				yield path, "value is not of type dictionary"
				return

			if self.__allowedElementTypes is not None:
				for k, v in value.items():
					if not isinstance(k, str):
						yield self.__modifyPath(path, k), "key must be string"
						continue
					if v is None:
						yield self.__modifyPath(path, k), "must not be null"
						continue
					bFound = False
					for t in self.__allowedElementTypes:
						if t._matchType(v):
							yield from t._check(scmgr, self.__modifyPath(path, k), v)
							bFound = True
							break
					if not bFound:
						yield self.__modifyPath(path, k), "item is of invalid type"
	#

	def __modifyPath(self, path:list, k:str):
		ret = list(path)
		ret[-1] = ret[-1] + "[" + repr(k) + "]"
		return ret
	#

#

class SpecificDictionaryValueChecker(AbstractValueChecker):

	def __init__(self, scmgr:IStructureCheckerManager, children:dict = None, required:bool = True, structType:str = None,
		nullable:bool = False):

		super().__init__(scmgr)

		if children is not None:
			assert isinstance(children, dict)
		assert isinstance(required, bool)
		if structType is not None:
			assert isinstance(structType, str)

		self.required = required
		self.nullable = nullable
		self.children = children
		self.conditions = None
		self.structType = structType
	#

	def dump(self, prefix:str = "", printFunc = None):
		if printFunc is None:
			printFunc = print

		printFunc(prefix + ">> struct " + self.structType + " >>"
			+ " required=" + str(self.required)
			+ " nullable=" + str(self.nullable)
			+ " {")
		for k, v in self.children.items():
			printFunc(prefix + "\t" + repr(k) + ":")
			v.dump(prefix + "\t\t", printFunc)
		printFunc(prefix + "}")
	#

	def parseValueFromStr(self, s:str):
		raise Exception("Lists can not be represented as strings")
	#

	def cloneObject(self):
		ret = SpecificDictionaryValueChecker(self._scmgr, self.children, self.required, self.structType)
		if self.conditions is not None:
			ret.conditions = list(self.conditions)
		return ret
	#

	def _compile(self, scmgr, path:list):
		ret = []
		for k, c in self.children.items():
			for r in c._compile(scmgr, path + [ k ]):
				ret.append(r)
		if ret:
			yield from ret
		else:
			self._bCompiled = True
	#

	def _matchType(self, value):
		if value is None:
			if self.nullable:
				return True
			else:
				return False
		else:
			if self._isinstance(value, dict):
				if self.conditions:
					for c in self.conditions:
						if not c.check(value):
							return False
				return True
			else:
				return False
	#

	def _check(self, scmgr, path:list, value):
		if value is None:
			if not self.nullable:
				yield path, "must not be null"
				return
		else:
			if not self._isinstance(value, dict):
				yield path, "value is not of type dictionary"
				return

			remainingChildren = dict(self.children)
			for k, v in value.items():
				checker = remainingChildren.get(k)
				if checker is None:
					yield path + [ k ], "excessive element"
					continue

				yield from checker._check(scmgr, path + [ k ], v)
				del remainingChildren[k]

			for k in sorted(remainingChildren.keys()):
				c = remainingChildren[k]
				if c.required:
					yield path + [ k ], "required"
	#

#




class StructureCheckerManager(IStructureCheckerManager):

	def __init__(self):
		self.__types = {
			"int": IntValueChecker(self),
			"float": FloatValueChecker(self),
			"str": StringValueChecker(self),
			"bool": BooleanValueChecker(self),
		}
	#

	def register(self, name:str, checker:AbstractValueChecker):
		Assert.isInstance(name, str)
		#assert isinstance(name, str)
		Assert.isInstance(checker, AbstractValueChecker)
		#assert isinstance(checker, AbstractValueChecker)

		self.__types[name] = checker

		return checker
	#

	def get(self, name:str) -> AbstractValueChecker:
		Assert.isInstance(name, str)
		#assert isinstance(name, str)

		return self.__types.get(name)
	#

	def getE(self, name:str) -> AbstractValueChecker:
		Assert.isInstance(name, str)
		#assert isinstance(name, str)

		return self.__types[name]
	#

	def __in__(self, key:str) -> bool:
		assert isinstance(key, str)

		return key in self.__types
	#

	def __iter__(self):
		return sorted(self.__types.keys()).__iter__()
	#

	def list(self) -> list:
		return sorted(self.__types.keys())
	#

#








