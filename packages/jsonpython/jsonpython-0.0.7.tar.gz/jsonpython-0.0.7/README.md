# Jsonpython

## A package to deserialize and serialize json.

### Installing:
```shell
pip install jsonpython
```

### Example:

#### data.json
```json
{
  "name": "Alex",
  "age": 23,
  "car": {
    "model": "Tesla X",
    "cost": 40000,
    "company": {
      "name": "Tesla"
    }
  }
}
```

#### main.py

```python
from jsonpython import *

jobj = get_json_object("data.json")

print(jobj['name'])  # Alex
print(jobj['car']['model'])  # Tesla X


class Company:
    name: str


class Car:
    model: str
    cost: int
    company: Company


class Person:
    age: int
    name: str
    car: Car


person = to_cls(Person, "data.json")

print(person.car.model)  # Tesla X
```