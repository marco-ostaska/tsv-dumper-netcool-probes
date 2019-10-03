Netcool tsv dumper
====

Simple script to add/remove/lit entries in a tsv formats readable by a netcool automation to conver to probe rules.

Requirements
---

- Python 3.6+
-  pprint module

Usage
----

interative mode:

```
python ceim.py <tsv file> <opt>
```


Using JSON:

```
python  ceim.py <tsv file> <opt> <json file>
```

### < opt >
- list: list all entries in tsv file
- add: add new entry to tsv file
- json: creates tsv from json file
- json-dump: creates json from tsv file
