# General logic schema governance manager

**This is early alpha proof of concept project**

## Motivation
There is a lot of different ways to define schemas nowadays, being it APIs,
databases, messaging and events, files, etc..

Today, for more complex systems and microservices oriented architectures, 
it is common to have more than one schema definition type involved (API and
Databases being the most common).

This creates the problem of having the same concepts being represented by
different schema definitions, making the data governance harder, since the data
concepts are  spread all over those different schemas.
The suggested solution for this problem is to create a "logical schema model"
that can work as the root to generate all other needed schemas, and this
logical model also be used to validate with domain experts if the concepts
being used are correct.

From that logical schema model, we can derive other schema styles and
instantiate other schema types.


## Goal
The goal of this project is to facilitate data governance in a heterogeneous
environment, where we use several different data schemas, like APIs, Databases
and Messaging.

One of the main goals is to represent different schemas in a domain specific
language that can be used to generate those specific schemas, following this
characteristics:
1. Is a Human Readable Format(HRF): can be read and manipulated in text format
2. Plays well with software version control systems (GIT), being able to use the
   default tools, like diff, and be versioned along with the software being
   built
3. Be the root of all specific schemas, able to automate their generation
4. Be able to represent the selected physical schemas in their respective schema
   style types, adding necessary elements, like:
		- Headers, Partition Keys and Body for Messages and Events
		- Indexes, Foreign Keys and table attributes for relational databases
		- Routes, Request and Response schemas and specific attributes for APIs

Overall, it must work like a logical data model for specific data schemas, but
encompassing more schema types than traditional database logical models

### Future goals
One of the future goals is to implement reverse engineering of physical models
into logical models. This is still under discussion.

## Schema style types
Schema-manager need to support three schema style types:
1. **Nestable** : schemas that can have nested schemas, like json, xml, yaml
   formats;
2. **Relational**: schemas that represent relational databases, with tables,
   attributes and relationships;
3. **Flat**: schemas that have no nested or relationship among entities, like
text files and comma separates files (csv)

Each style can have different ways to be represented, but schema-man uses
a nested schema definition style to represent all other styles.

## Physical schemas

The following schemas are being taken in consideration to be represented by the schema-manager:

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
 - RAML
EventBased
 - Kafka

## Design considerations
The syntax of schema-manager is clearly inspired in the python programming language.

Here goes the zen of schema-manager adapted from [ the zen of python ]( https://en.wikipedia.org/wiki/Zen_of_Python ):  

Beautiful is better than ugly.  
Explicit is better than implicit.  
Simple is better than complex.  
Complex is better than complicated.  
Sparse is better than dense.  
Readability counts.    
Special cases aren't special enough to break the rules.   
Although practicality beats purity.  
Errors should not pass silently.  
In the face of ambiguity, refuse the temptation to guess.  
There should be one—and preferably only one—obvious way to do it.  
If the implementation is hard to explain, it's a bad idea.  
If the implementation is easy to explain, it may be a good idea.  
Namespaces are one honking great idea—let's do more of those!  

## Examples

Some examples of what is possible to define using schema-manager

```
# Separete types using namespaces
namespace com.accenture.common

	#####
	# define simple type aliases
	#####
    type id long "long integer representing a unique id"

    type code string(12):
        "short strig, usually a mnemonic, used as alternate key or primary
        key when referencial static data"

    type Name string(255) "Standard Name"

    type Version string(255) "version of the aggregate"

    type Username string(255) "default username string"

    type Description string(4000) "Description"

	#####
	# Define long documentation, in an arbitrary lenght
	#####
    type Money decimal(19,4):
        """Decimal type, with precision of 19 and 4 decimal to represent monetary
        values
		It is known that 15 digits + 4 decimal digits are a good practice to represent storage.
		Some important articles:
		(four decimal places when using decimal to represent money)[https://stackoverflow.com/questions/34143961/why-are-four-decimal-places-suggested-when-using-decimal-to-represent-money]"""


namespace com.accenture.imat:
	"""The imat namespace"""

	# make the com.accenture.common types accessible without full qualified name
	from com.accenture.common import Name, Username,
			id, Money

    record AuditField:

        created_date Date "date of the record creation"
        created_by Username "username that created the record"
        last_updated_date Date "date that the record were last updated"
		# Username type bein accessed using full qualified name
        last_updated_by com.accenture.common.Username:
			"""username who uptaded the record the last"""


    record KeyValue:
		"""key/value attribute to be used as a name/value set of values by
		other records."""

        key Name
        value String(4000)


    record NameSpace:
        """namespace to focus the domains into specific areas (namespaces)"""

        *code Code
        name Name
        description Description


    record BoundedContext:
        *code Code
        name Name "BC Name"
        description Description "BC Description"
        attributeMap *AttributeMap null "BoundedContext attributeMap"
		# will include the AuditField attributes at this location, 
		# keeping the order of the attributes in the record definition
		# (some schemas, like databases and ProtoBuf requires the correct order)
        !include AuditField     "Expand the record in-line"


    enum SchemaType:
        """the types of schemas - flat, nestable or relational"""

        FLAT
        NESTABLE
        CUSTOM


    record DataTypes
        """The data types used by the models"""

        *code Code
        description Description
		### complex types can be defined in a nested way
		type enum :

			INTEGER
			FLOAT
			DECIMAL
			STRING
			DATE
			DATETIME


    record SchemaType:
        """the data types associated with different technologies"""

        *code Code
        name Name
        type SchemaType
        dataTypes *DataType
        !include AuditField


    record Attribute:
        """Attribute of an entity"""
        name Name
        description Description null
        attributeMap *AttributeMap null
        dataType !DataType
        isNull bool
        isPK bool
        order int
        lenght int null
        precision int null
        scale int null
        defaultValue string(4000) null
        domain string(4000) null
        list_of_values_code !ListOfValues null


    enum EntityType:
        """Following DDD, as Entity, Value Objecs and Aggregates.
        A custom type is also available for other types of entities"""

        VALUE_OBJECT
        ENTITY
        AGGREGATE
        AGGREGATE_ROOT
        CUSTOM


    record Entity:
        """Entity being represented in the logical model"""

        *code Code
        name Name
        description Description null
        type EntityType
        attributeMap *AttributeMap null
        attributes *Attribute null

    record SchemaSource:
        """Identify the source of the schema, as it comes from a pre-defined
        structure, lide a software package (SAP, SalesForce) or pre-existing
        legacy structures"""

        *name Name
        desciption Description
        connectionString string(4000)
        password string(255)

    record Schema:

        *name Name
        *version Version
        *boundedContext !BoundedContext null
        *namespace !Namespace null
        type !SchemaType
        attributeMap *AttributeMap
        schemaSource SchemaSource null
        entities *Entity null
        !include AuditField


```
