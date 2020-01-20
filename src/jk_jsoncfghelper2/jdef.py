


from typing import Union




class JDefStructure(object):

	def __init__(self, name:str, structure:Union[list,tuple]):
		assert isinstance(name, str)
		assert isinstance(structure, (list, tuple))

		self.name = name
		self.structure = structure
	#

	#def cloneObject(self):
	#	return JDefStructure(self.name, list(self.structure))
	##

#


class JDef(object):

	def __init__(self, name:str, dataType:Union[str,JDefStructure], required:bool = True,
		minValue = None, maxValue = None, allowedValues:Union[list,tuple] = None,
		minLength:int = None, maxLength:int = None, elementTypes:Union[list,tuple] = None,
		nullable:bool = False):

		assert isinstance(name, str)
		assert isinstance(dataType, (str, JDefStructure))
		assert isinstance(required, bool)
		assert isinstance(nullable, bool)

		if minValue is not None:
			assert isinstance(minValue, (float, int))
		if maxValue is not None:
			assert isinstance(maxValue, (float, int))
		if allowedValues is not None:
			assert isinstance(allowedValues, (tuple, list))
		if minLength is not None:
			assert isinstance(minLength, int)
		if maxLength is not None:
			assert isinstance(maxLength, int)
		if elementTypes is not None:
			assert isinstance(elementTypes, (tuple, list))
			for item in elementTypes:
				assert isinstance(item, (str, JDefStructure))

		self.name = name
		self.dataType = dataType
		self.required = required
		self.minValue = minValue
		self.maxValue = maxValue
		self.allowedValues = allowedValues
		self.minLength = minLength
		self.maxLength = maxLength
		self.elementTypes = elementTypes
		self.nullable = nullable
	#

	def __str__(self):
		return self.name + ":" + self.dataType
	#

	def __repr__(self):
		return self.name + ":" + self.dataType
	#

	#def cloneObject(self):
	#	return JDef(self.name,
	#		dataType,
	#		minValue,
	#		maxValue,
	#		list(allowedValues) if allowedValues is not None else None,
	#		minLength,
	#		maxLength,
	#		list(elementTypes) if elementTypes is not None else None
	#	)
	##

#













