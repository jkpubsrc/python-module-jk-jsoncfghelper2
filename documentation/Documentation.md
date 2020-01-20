General Information
===================

* A **boolean value** is a value either of `true` or `false`.
* An **integer value** is either zero or a positive or negative numeric value of any size without fractional part.
* A **float value** is either an integer or a decimal value of any size.
* A **string value** is a sequence of characters.
* A **list** is a sequence of values.
* A **dictionary** is a set of key-value pairs.
	* Keys are always strings as this constraint system targets JSON (and other data that can be represented as JSON).
	* Values can be of either booleans, integers, floats, strings or lists or other dictionaries, either non-constrained ones or constrained ones (= structures).
* A **structure** is a dictionary that has specific attribute constraints. Typically such a structure has a name in order to simply referring to speicifc structure types.

Type constraints for structure definitions
==========================================

Type constraints define the type of a field in a structure.

Type: Boolean
-------------

Type identifier(s): "bool", "boolean"

Attributes:

* `bool required`: Indicates that this data field must be present.
	* In XML notation: Specify one of the following values: `true`, `false`, `yes`, `no`, `1`, `0`

Example:

```xml
<aBooleanField dataType="boolean" required="true" />
```

Type: Integer
-------------

Type identifier(s): "int", "integer"

Attributes:

* `bool required`: Indicates that this data field must be present.
	* In XML notation: Specify one of the following values: `true`, `false`, `yes`, `no`, `1`, `0`
* `int minValue`: If present defines the minimum value allowed.
	* In XML notation: Specify a single integer value.
* `int maxValue`: If present defines the maximum value allowed.
	* In XML notation: Specify a single integer value.
* `int[] allowedValues`: If present defines the values allowed.
	* In XML notation: Specify a list of integer values separated by comma.

Example:

```xml
<anIntegerField dataType="integer" required="true" minValue="1" maxValue="1000" allowedValues="1, 10, 100, 1000" />
```

Type: Float
-----------

Type identifier(s): "float"

Attributes:

* `bool required`: Indicates that this data field must be present.
	* In XML notation: Specify one of the following values: `true`, `false`, `yes`, `no`, `1`, `0`
* `float minValue`: If present defines the minimum value allowed.
	* In XML notation: Specify a single float value in standard IEEE notation.
* `float maxValue`: If present defines the maximum value allowed.
	* In XML notation: Specify a single float value in standard IEEE notation.
* `float[] allowedValues`: If present defines the values allowed.
	* In XML notation: Specify a list of float values separated by comma.

Example:

```xml
<aFloatField dataType="float" required="true" minValue="1" maxValue="1000" allowedValues="1.23, 2.34, 3.45, 4.56" />
```

Type: String
------------

Type identifier(s): "str", "string"

Attributes:

* `bool required`: Indicates that this data field must be present.
	* In XML notation: Specify one of the following values: `true`, `false`, `yes`, `no`, `1`, `0`
* `int minLength`: If present defines the minimum length allowed.
	* In XML notation: Specify a single int value.
* `int maxLength`: If present defines the maximum length allowed.
	* In XML notation: Specify a single int value.
* `str[] allowedValues`: If present defines the values allowed.
	* In XML notation: Specify a list of character sequences values separated by comma.

Example:

```xml
<aStringField dataType="string" required="true" minLength="1" maxLength="1000" allowedValues="foo, bar, some string value, another string value" />
```

Type: List
----------

Type identifier(s): "list"

Attributes:

* `bool required`: Indicates that this data field must be present.
	* In XML notation: Specify one of the following values: `true`, `false`, `yes`, `no`, `1`, `0`
* `int minLength`: If present defines the minimum length allowed.
	* In XML notation: Specify a single int value.
* `int maxLength`: If present defines the maximum length allowed.
	* In XML notation: Specify a single int value.
* `str[] elementTypes`: If present defines of which types values of the list are allowed to be of.
	* In XML notation: Specify a list of type names separated by comma.

Example:

```xml
<aListField dataType="list" required="true" minLength="1" maxLength="1000" elementTypes="int, str, someStructure" />
```

Type: Dictionary
----------------

Type identifier(s): "dict", "dictionary", "obj", "object"

Attributes:

* `bool required`: Indicates that this data field must be present.
	* In XML notation: Specify one of the following values: `true`, `false`, `yes`, `no`, `1`, `0`
* `str[] elementTypes`: If present defines of which types values of the dictionary are allowed to be of.
	* In XML notation: Specify a list of type names separated by comma.

Example:

```xml
<aDictionaryField dataType="dictionary" required="true" elementTypes="int, str, someStructure" />
```

Type: Structure
---------------

Type identifier: The name of a previously defined structure.

Attributes:

* `bool required`: Indicates that this data field must be present.
	* In XML notation: Specify one of the following values: `true`, `false`, `yes`, `no`, `1`, `0`

Example:

```xml
<aStringField dataType="someStructure" required="true" />
```

Conditional constraints for structure definitions
-------------------------------------------------

By definition structures are specializations of dictionaries. That means: There can exist multiple structures that are all basically nothing else but dictionaries with key-value pairs.

In this type constraint system we can define types for the values in key-value pairs. As we might want to define multiple structures a specific value can be of, we need a way to distinguish between specific structures. An easy way for doing this is to define value constraints for a structure. That means: If for an instance of a structure that the type checker encounteres a certain value constraint holds this structure is identified as being of the specific type as defined by this constraint.

Example: We can define structure *sx* to require a "`type`" attribute with value "`sx`". Additionally we can define structure *sy* to require a "`type`" attribute with value "`sy`". Depending on the value specified for "`type`" either constraints for structure *sx* or *sy* must be applied, depending on the value specified. So value specidied in attribute "`type`" determines which specific structure the data encountered must be of.

Cnstraint: Equals
-----------------

The constraint `eq` defines that a value must be equal to a specific value to recognize a dictionary encountered as being of a specific structure type.

Attributes:

* `str field`: The name of the field that must match the specified value.
	* In XML notation: Specify a character sequence.
* `(text)`: The value of the field.
	* In XML notation: Specify an arbitrary value as text within the XML element.

Example:

```xml
<eq field="aStrField">hard drive</eq>
```



