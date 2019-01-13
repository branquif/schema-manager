# 2. schema technology selected

Date: 2018-10-26

## Status

Proposed

## Context

In order to prove that a common root of schema definitions is possible, an
initial set of schema definition technologies needs to be selected and adjusted.

The initial types of technologies will be data storage and
integrations/interfaces.

The list and parameterization of the schema definition technologies also needs
to accomodate new technologies through configurations files as much as possible.


## Decision

The list of selected technologies are:
- Data Storage:
	- Oracle
	- MySQL
	- Postgres
- Interfaces:
	- OpenAPI
	- AVRO

The parameterization of the mapping between the general schema definitions and
the specific technologies will be represented by yaml files.
There will be one file per technology.

At the selected technologies, there will be one file to define the general
datatypes, and one file to map the general datatypes to the specific datatypes
of the technology:
- abstract_datatypes.yaml
- oracle_datatype_mappings.yaml
- mysql_datatype_mappings.yaml
- postgres_datatype_mappings.yaml
- openapi_datatype_mappings.yaml
- avro_datatype_mappings.yaml


# Consequences

The number of specific schema technologies can grow without the need of another
configuration
