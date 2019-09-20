# YAML Stats

![Code Coverage](coverage.svg)
[![CircleCI](https://circleci.com/gh/jwholdsworth/yamlstats.svg?style=svg)](https://circleci.com/gh/jwholdsworth/yamlstats)

Detects duplicate, different and missing key/value pairs between two YAML files. The idea being it simplifys the soup that becomes of ansible group_vars files.

## Installation

`make install`

## Usage

### Print a list of configuration items that are identical in both files

```./main.py file1.yml file2.yml```

```
+----------+--------------------------------------------+
|   Key    |                   Value                    |
+----------+--------------------------------------------+
|   job    |                 Developer                  |
+----------+--------------------------------------------+
|  skill   |                   Elite                    |
+----------+--------------------------------------------+
| employed |                    True                    |
+----------+--------------------------------------------+
|  foods   | ['Apple', 'Orange', 'Strawberry', 'Mango'] |
+----------+--------------------------------------------+
```

### Print a table of configuration items that have different values

```./main.py -d file1.yml file2.yml```

```
+-----------+-----------------------------------------+-------------------------------------------+
|    Key    |           examples/file1.yaml           |            examples/file2.yaml            |
+-----------+-----------------------------------------+-------------------------------------------+
|   name    |             Martin Devloper             |              Martin D'vloper              |
+-----------+-----------------------------------------+-------------------------------------------+
...
```

### Print a list of configuration keys that are not in both files

```./main.py -a file2.yml file3.yml```

```
+---------------------+---------------------+
| examples/file2.yaml | examples/file3.yaml |
+---------------------+---------------------+
|      location       |     university      |
+---------------------+---------------------+
```
