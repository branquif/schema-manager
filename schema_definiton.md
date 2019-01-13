# General schema definitions

This project provides a unification of data schemas, being a superset of the
most common data schemas definitions.

Originally it is amied to encompass:
Schemas:
 - json schemas
 - ProtocolBuffers
 - AVRO
 - Cassandra
 - MySQL
 - Postgres
RPCs:
 - gRPC
 - OpenAPI
EventBased
 - Kafka

# Primitive types
The set of primitive type names is:

- null: no value
- boolean: a binary value
- int: 32-bit signed integer
- long: 64-bit signed integer
- float: single precision (32-bit) IEEE 754 floating-point number
- double: double precision (64-bit) IEEE 754 floating-point number
- bytes: sequence of 8-bit unsigned bytes (support size)
- string: unicode character sequence (support size)
- decimal: arbitrary-precision signed decimal number (scale, precision)
- date: 32-bit unsigned integer representing the number of days since epoch 
	(January 1, 1970) with no corresponding time value. Values are integer (days
	since epoch) or string format 'yyyy-mm-dd'
- time-millis: a time of day, with no reference to a particular calendar, time
	zone or date, with a precision of milliseconds. It is represented internally
	as an int. Values are integer (milliseconds from midnight) or string format
	as 'hh:mm:ss[.fff]', where miliseconds (f) are optional.
- time-micros: a time of day, with no reference to a particular calendar, time
	zone or date, with a precision of microseconds. It is represented internally
	as a long. Values are integer (microseconds from midnight) or string format
	as 'hh:mm:ss[.fff]', where miliseconds (f) are optional.
- timestamp: 



# Complex types
There are six kinds of complex types: records, enums, arrays, maps, unions and
fixed.

## Records
Records support three attributes:
- name: name of the record (required)
- doc: documentation to the user of this schema (optional)
- aliases: array providing alternate names for this record (optional)
- fields: list of fields (required). Each field has the following attributes, in
	this order:
	- name: the name of the field (required)
	- aliases: array of strings, providing alternate names for this field (optional)
	- type: the type of the field primitive or complex (required)
	- size: a max size - always in parentheses (optional)
	- null and default: define a field as null, and an optional default value in
		case of nullable value between parentheses
	- order: specifies how this field impacts sort ordering of this record
		(optional). Valid values are asc (the default), desc, or ignore.
	- doc: description of the field for users, between double quotes (optional)

Example:
```
namespace example.schema
	record User
		name string(256) "Full name of the user"
		favorite_number int null(7) "User's favorite number"
		favorite_color string null("blue") "User's favorite color"
		mother_name(mother, mom_name) string(256) asc "the mothers full name"
```

## Enums
Enums support the following attributes:
- name: the name of the enum (required)
- aliases: array of strings providing alternate names for this enum (optional(
- symbols: list of symbols, as strings. All symbols in an enum must be unique;
	duplicates are prohibited. Every symbol must match the regular expression
	[A-Za-z_] [A-Za-z_]*

Example:
```
enum Suit("suit", "deck_suit")  (SPADES, DIAMONDS, CLUBS, HEARTS)
```

## Arrays
Arrays support a single attribute, defining the type of the items of the array:
- items: the schema of the array type.

Example:
```
namespace example.schema
	record Invoice
		header string "the invoice header"
		items array(
			record item
				name string
				value Decimal(19,4)
		)
		total Decimal(19,4)

	record OrderItem
		name string
		value Decimal(19,4)
	
	record Order
		customerId string "the customer id"
		items array(OrderItem)

```

## Maps
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
		teams map(int, string)

```

Key is assumed as string when not informed.
Example:
```
teams map(int) // teams key will be a string, with int values
```

## Unions (Oneof)
A union or a OneOf is used to indicate that a field may have more than one type. They are
represented as arrays.
In case of a nullable field, the default value is related to the first type of
the union.

For example, suppose you had a field that could be either a string or an int.
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

# Preprocessing
Some minor preprocessing capabilites are included in the processing of schema
definitions, and are similar to a C language preprocessor, except that instead
of using the # symbol we will use !

## Including files

Use the !include directive to include schema files.

For example:
```
!include Address.schm

record Person
	name string
	address Address # address record type defined at the Address.schm file

```

## Constant definition

You can define constat using the !define directive. As in C language, a constant
name can only use alphanumeric and underscore character, and cannot start with
a digit.

```
!define MONEY decimal(19,4)
!include Acconut.schm

record Transfer
	fromAccount Account
	toAccount Account
	value MONEY
```

Of course, you can use the !include directove to define all your constants in
a single file that you include in your schema definition.

Constant can be undefined with the !undef XXX directive.

