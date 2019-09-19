# YAML Stats

![Code Coverage](coverage.svg)

Detects duplicate, different and missing key/value pairs between two YAML files

## Installation

`make install`

## Usage

### Print a list of configuration items that are identical in both files

```./yamlstats.py file1.yml file2.yml```

```
#######################################
job is the same in both files:
Developer
#######################################
skill is the same in both files:
Elite
#######################################
...
```

### Print a table of configuration items that have different values

```./yamlstats.py -d file1.yml file2.yml```

```
+-----------+-----------------------------------------+-------------------------------------------+
|    Key    |           examples/file1.yaml           |            examples/file2.yaml            |
+-----------+-----------------------------------------+-------------------------------------------+
|   name    |             Martin Devloper             |              Martin D'vloper              |
+-----------+-----------------------------------------+-------------------------------------------+
...
```
