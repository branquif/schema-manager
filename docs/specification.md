# Specification

## Introduction

This document defines the schema-manager specification, and the implementation
of schema-manager must adhere to this specification.

The data representation will follow in part the concepts of Domain Driven
Design, using Aggregates, Entities and Value Objects as schema representation,
and it is recommended that it is used as an overall guideline for the schema
modeling, although not strictly necessary.

Whenever a relevant point needs to be made on how a target schema styles or target physical schema definitions will be dealt, it will appear in a compatibility list session in this document - examples being how to map enums to relational databases and common denimators between AVRO schemas and OpenAPI schemas.

## Basic Structure

A schema is represented in a simplified DSL, built to simplify human readability
and version control using VCS, like GIT or SVN.  
It is heavely inspired by the Python programming language inheriting it's  readability (flat element definitions, forced identification, long documentation strings).






## Namespaces

TBD

## Comments

**Comments** are single-line only, and starts with a #.
Ex:
```
#this is a line comment example

type Money Decimal(19,4) "Money user defined type" # this is a comment
```
There is no multiline comments at schema-manager. If needed to comment several
lines, use several single-line commented lines.

## Element declaration

An element is a type or attribute being defined.
It is always declared in the following form:
```
<element_definition_type> <element_name> [<specific_type_definitions>][[<inline
documentation>] | :
	<multiline_documentation>]

	[<element_definition_attributes>]
```

where:  
**element_definition_type**: one of the possible type definitions (type, record,
enum )  
**element_name**: the element name, following the name formation rule  
**specific_type_definitions**: the other definitions needed by the element
definition type, like the datatype for user defined types.  
**inline_documentation**: inline documentation of the element. Note that it is
not possible to have an inline_documentation with a line break extension(:) element. If
the description requires a lengthly description, it is better to use
a multiline_documentation.  
**multiline_documentation**: a multiline documentation for the element. Note
that, as a clarification rule, we insert a separated line between the comment
and the initial declaration of attributes.  
**element_definition_attributes**: all needed attributes for this element, if
needed  

Examples:
```
# User defined type declaration
type Code String(12) "Short string to represent a code" 

# Record element type declaration
record Person:
	"""Represents a person in the system"""

	*id Integer "Unique id for the person"
	name String(255) "full name of person"
	email String(255) "email of persion"
```

## Elements documentation

**Documentation** are used to describe the concept of various elements within
schema-manager. It is always optional, and can be used inline or multiline.

**Inline** comments are always the last part of a declaration (comments are not
considered), and are always between double quotes (").
Example:
```

type Money Decimal(19,4) "Money user defined type" # this is a comment
						 ^^^^^^^^^^^^^^^^^^^^^^^^^
						 This is an inline comment
```

**Multiline** comments are always used to provide lengthly descriptions of
elements, and are represented by triple double quotes (""").

End of lines are automatically included in the string, but its possible to 
prevent this by adding a \ at the end of the line.


```
type Code String(12):
	"""short string, usually a mnemonic, used as alternate key or primary \
	key of referencial static data
	"""

[<other_element_declaration>]
```

Note that in the example above, the following string represents the
documentation:
```
short string, usually a mnemonic, used as alterative key of primary key of referencial static data\n
```

## Primitive Types

Primitive types are all capitalized and have no attributes.


The set of primitive type names is:

**Bool**: a binary value
**Int**: 32-bit signed integer
**Long**: 64-bit signed integer
**Float**: single precision (32-bit) IEEE 754 floating-point number
**Double**: double precision (64-bit) IEEE 754 floating-point number
**Bytes**: sequence of 8-bit unsigned bytes (support size)
**Uuid**: Universal unique identication
**String**: unicode character sequence (support size)
**Decimal**: arbitrary-precision signed decimal number (support scale and precision)
**Date**: 32-bit unsigned integer representing the number of days since epoch 
	(January 1, 1970) with no corresponding time value.
**Time**: a time of day, with no reference to a particular calendar, time
**Timestanp**: Date and Time representation
**Timetz**: time represented with it's time zone
**Timestamptz**: timestamp with it's timezone
**Blob**: arbitrary binary sized object

This is a superset of primitive types, and some of them are not primitives in
their physical schemas, and a translation mechanism to that specific
implementation will be necessary (sometimes to other primitive type, sometimes
with a complex type).

### User Defined Types
It is possible to define user defined simple types that act as aliases of simple
types.

Declaration of types:
```
type <type_name> <simple_type> [<inline documentation>]:
	[<multiline documentation>]
```

Where:
type_name: the name that will be used as alias of this type.
simple_type: one of the simple types described above.

Example:
```
type Code String(12):
	"""short string, usually a mnemonic, used as alternate key or primary \
	key of referencial static data
	"""
```

## Complex types

The complex types are represented by the following concepts:
- **Records**: represents a data entity in the model.
- **Enums**: list of possible values.
- **Map**: a dictionary with key and values
- **List**: A list of a specific value
- **Set**: a list of unique values
- **Unions**: a union or a OneOf is used to indicate that an attribute may have
  more than one type.


### Enums
Enums are a list of possible values, known as symbols.  
Declaration of enums:
```
enum <enum_name>:
	<multiline documentation>

	<symbol 1> <inline_documentation>
	<symbol 2> <inline_documentation>
```

Where:
<enum_name>: the name of the enum (required)
<symbol #>: any name that represent the symbol. Cannot have duplicate values.

Example:
```
enum Suit:
	"""The french deck suits"""

	SPADES "Spades suit"
	DIAMONDS "diamonds suit"
	CLUBS "Clubs suit"
	HEARTS "Hearts suit"
```
Compatibility list:
- AVRO: values are list of strings.
- ProtoBuf: values are symbols, translated into int32, and allow aliasses.
- OpenAPI: Values are list of strings, no aliases.
- DB: values are a list of arbitrary types, no aliases. Usually specified as
	check constraints in regular datrabases. Postgres can nominate an enum
	datatype, just like schema-manager. Mysql can generate inline enum
	attributes. As a rule of thumb, we will not use either. The decision will
	always be between a check constraint vs a dedicated domain table when
	instantiating the model in a database.

**Decision for schema-manager**:  
We will use list of strings, without AVRO concept of aliases, since it is a common ground for
all the available schemas in use.


### Records
Represents a data entity. Each instance of an entity can have many attributes
of different types (primary or complex).


Record declaration:

```
record <record_name>:
	[<multiline_documentation>]

	[<list_of_attributes>]

	# attribute definition
	<primary_key_attribute> | <record_attribute> [<"inline_documentation">][:
		<multiline_documentation>]

	#<primary_key_attribute>
	*<attribute_name> <simple_type>

	#<record_attribute>
	<attribute_name> <regular_attribute> | <array_attribute> | <reference_attribute>

	#<regular_attribute>
	<simple_type | complex_type> [null] default <default_value>

	#<array_attribute>
	*[(#)]<simple_type | complex_type>

	#<reference_attribute>
	!<complex_type>

```

where:  
**record_name**: name of the record element (required)  
**multiline_documentation**: documentation to the user of this schema (optional)  
**attribute_name**: name of this attribute (required)  
**simple_type**: one of the simple types supported or a user defined type  
**complex_type**: another complex type
**null**: define if the attribute can accept null values. If not specified, the
	attrubute will not accept null values.  
**default_value**: the default value. Applicable only for simple_types (optional)  
**inline_documentation**: inline documentation to the user of this schema
(optional)  
**multiline_documentation**: multiline documentation to the user of this schema
(optional)  

```
namespace example.schema:

	record Address:
		"""Address type"""

		street_name String(255)
		neighborhood String(255)
		zip_code String(16)


	record PhoneNumber:
		"""phone number type"""

		type enum PhoneType: # even nested type definition must have a name

			Mobile
			Work
			Home


	record User:
		"""person that represents a system user"""

		*id Long "User unique indetifier"
		name String(256) "Full name of the user"
		spouse_id !User null "user's Spouse"
		phone_numbers *PhoneNumber
		favorite_number Int null(7) "User's favorite number"
		favorite_color String null("blue") "User's favorite color"
		mail_address Address null "user mail address"
		billing_address Address null "user billing address"


	record UserFriends:

		user !User
		friend !User
```

####Schema Style Type important considerations

Following the Domain Driven Design principles, we can use the record elements to
represent entities, which must have a primary key, and value objects, that are
complex types that are used within an entity, which don't need a primary key,
since they cannot exist without their "parent" entity.

**Inline type declaration**  
At the example, note that the PhoneNumber type was defined inline in a nested way.
It is possible to nest as many inline types as needed.

Whenever a record without a primary key needs to be inserted in a database,
a default unique identification for value objects will be created automatically
(an "invisible" id field will be created to allow referential integrity).

A record can have composite **primary keys** (more than one attribute with a * in
front of their attribute_name. Note that primary keys can only be simple_types.

**Default values** are only allowed for simple types,  and must follow the same
data type of the attribute being declared.

**Array Atrributes** are nested data, and is one of the characteristics of
nestable schema styles like json, xml and yaml, when a list of types are nested
for an attribute.


An example of an array attribute:
```
User : { id : 345,
		name : "William Bonner",
		spouse_id : 123
		phone_numbers : [ #an array of objects
			{ type : "Mobile", phone_number : "11 99434 2234"},
			{ type : "Work", phone_number : "11 3434 1234" }
		]}

```

Array attributes have different ways to be implemented in a relational database,
and this problem is known as 
[object relational impedance mismatch](https://en.wikipedia.org/wiki/Object-relational_impe$)

When represented as relational database, they will be converted into a table,
and will have a foreign key assigned to the entity that references it. If it
has no defined primary key in the model (which can be common practice for value
objects), an id attribute will be added and set as primary key, along with the
entity key.

Examples:
```
table User (
	id Long is PK, 
	name Varchar(255), 
	spouse_id Long, 
	mail_address_id Long,
	billing_address_id Long)

#Note that a _id suffix was created for the mail_address and billing_address
attributes.

table Address (
	id Long is PK, 
	street_name varchar(255) ...)
	
#Note that an id attribute was created as a primary key for Address
```

**Reference attribute** references other complex types by their primary keys.
It is not possible to reference a record that don't have a defined primary key.
When the primary key is a single attribute, a representation in
a hierarchical format would look like this:

```
User : { 
	id : 345,
	name : "William Bonner",
	spouse_id : 123 }
```

When the primary key is composed of more than one attribute, a representation
in a hierarchical format would look like this:

```
User : { 
	id : 345, 
	name : "William Bonner", 
	spouse : { 
		id : 123, 
		parent_id : 2 }
# Where it is id and parent_id are the primary key of the referenced record
```

#### Compatibility list
- AVRO: it has the concept of
  [aliases](http://avro.apache.org/docs/current/spec.html#Aliases). We will use
  mapping concept to cope with aliases for AVRO  
- ProtoBuf: compatible as nestable schema.
- OpenAPI: compatible as nestable schema.
- Relational DB: check all schema style 

### Maps
Maps support two attribute:
- key: the schema of the map's key
- values: the schema of the map's value

Example:
```
namespace example.schema
	record cycling_teams
		id uuid
		lastname string
		firstname string
		teams map(Int, String(20)) # teams attribute is a map
```


#### Compatibility list
- AVRO: it allow only string keys. 
  [maps](http://avro.apache.org/docs/current/spec.html#Maps).
  If the map defined has a key that is not a string, it will be converted into a string 
	(#todo: specify the casting function to converto to string)
- ProtoBuf: requires the enum to have a name, and works with symbols. 
- OpenAPI: compatible as nestable schema.
- Relational DB: check all schema style 

### Unions (Oneof)
A union or a OneOf is used to indicate that an attribute may have more than one
type. They are represented as arrays.

For example, suppose you had an attribute that could be either a string or an int.
Then the union is represented as: 
```
string|int
```

You might use it in the following way:

```
namespace example.schema
	record Address
		street string
		number int

	record FullName
		first string|null
		last string
		address string|Address null("Sesame Street") 

```


## Importing definitions

Use the _import_ directive to include schema files.

For example:
```
import Address.schm

record Person
	name string
	address Address # address record type defined at the Address.schm file

```

## Constant definition



### Names
Record, enums and fixed are named types. Each has a fullname that is composed of
two parts; a name and a namespace. Equality of names is defined on the fullname.

The name portion of a fullname, record field names, and enum symbols must:

start with [A-Za-z_] subsequently contain only [A-Za-z0-9_] A namespace is
a dot-separated sequence of such names. The empty string may also be used as
a namespace to indicate the null namespace. Equality of names (including field
names and enum symbols) as well as fullnames is case-sensitive.

In record, enum and fixed definitions, the fullname is determined in one of the
following ways:

A name and namespace are both specified. For example, one might use "name": "X",
"namespace": "org.foo" to indicate the fullname org.foo.X.  A fullname is
specified. If the name specified contains a dot, then it is assumed to be
a fullname, and any namespace also specified is ignored. For example, use
"name": "org.foo.X" to indicate the fullname org.foo.X.  A name only is
specified, i.e., a name that contains no dots. In this case the namespace is
taken from the most tightly enclosing schema or protocol. For example, if
"name": "X" is specified, and this occurs within a field of the record
definition of org.foo.Y, then the fullname is org.foo.X. If there is no
enclosing namespace then the null namespace is used.  References to previously
defined names are as in the latter two cases above: if they contain a dot they
are a fullname, if they do not contain a dot, the namespace is the namespace of
the enclosing definition.

Primitive type names have no namespace and their names may not be defined in any
namespace.

A schema or protocol may not contain multiple definitions of a fullname.
Further, a name must be defined before it is used ("before" in the depth-first,
left-to-right traversal of the JSON parse tree, where the types attribute of
a
