# pymongobox 
Set of tools allowing the operation of a mongodb database

* [Requirements](#requirements)
* [crud](#crud)
		* [Usage](#usage)
* [streaming](#streaming)
		* [Usage](#usage-1)


## Requirements 
* System requirements:
	- mongodb 4.2 or higher
	- mongodb replica set available

## Package install 
- `pip install .`

## crud 
CRUD operations create, read, update, and delete documents.
```bash
from pymongobox.crud import crud
```

#### Usage 
- Set configuration for a collection 
```python
my_collection = crud.MongoDB("mongodb://localhost:27017", "database_name", "collection_name")
```
- insert 
```python 
doc = {"field1" : "value"}
my_collection._insert(doc)
```

- update 
```python 
# my_collection._update(filter,update_data, upsert, many)
my_collection._update({"field1" : "value"},{"field1" : "value2", "field2" : [1,2,3]}, False, True)
```

- find 
```python
_filter = {}
cursor = my_collection.find(_filter)
my_collection._process_cursor(cursor)
```

## streaming
streaming package is a simple mongodb streaming service based on mongodb change streams feature.

The service allows to launch asynchronous streams in parallel.

```bash
from pymongobox.streaming import services
```

#### Usage 
- Set configuration for multiple mongoDB collections :
```python 
stream_config1 = ["mongodb://localhost:27017","database_name","collection_name1"]
stream_config2 = ["mongodb://localhost:27017","database_name","collection_name2"]
stream_config=(stream_config1,stream_config2)
```
- Init the worker
```python 
# Worker(number of cpu you want to allocate, stream configurations)
worker = services.Worker(2, stream_config)
```

- Run
```python 
worker.pool_handler()
```


