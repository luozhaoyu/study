"""
11:00
11:34
"""
import enum
from typing import *
from dataclasses import dataclass
import pickle

@dataclass
class Schema:
    version: int
    fields: Dict

type Migration = Callable[[Dict, Schema]]

def define_schema(version: int, fields: Dict) -> Schema:
    """Create schema definition"""
    return Schema(version, fields)


def serialize(obj: Dict, schema: Schema) -> bytes:
    """Serialize with schema"""
    whole_obj = {
        "obj": obj,
        "schema": schema
    }
    return pickle.dumps(whole_obj)

def deserialize(data: bytes, target_schema: Schema, migrations: List[Migration]) -> Dict:
    """Deserialize and migrate"""
    # deserialize
    whole_obj = pickle.loads(data)
    obj = whole_obj["obj"]
    schema = whole_obj["schema"]
    for migration in migrations:
        try:
            obj, schema = migration(obj, schema)
        except Exception as e:
            print("couldn't apply migration")
            raise e

    if schema.fields != target_schema.fields:
        print(obj, schema)
        raise Exception(f"couldn't evolve to {target_schema} after migrations")

    # fields match, it means migration to new schema successfully
    schema.version = target_schema.version
    return obj


def set_object(obj, nested_path, value):
    splits = nested_path.split(".")
    current = obj
    for index, each_field in enumerate(splits):
        if index == len(splits) - 1:
            current[each_field] = value
            break
        if each_field not in current:
            current[each_field] = {}
        current = current[each_field]


def AddField(field, default, from_version: int):
    def apply(obj: Dict, schema: Schema) -> Tuple[Dict, Schema]:
        if schema.version < from_version:  # version too old
            return obj, schema

        set_object(obj, field, default)
        set_object(schema.fields, field, type(default))
        return obj, schema
    return apply

def ChangeType(field, converter, from_version: int):
    def apply(obj: Dict, schema: Schema) -> Tuple[Dict, Schema]:
        if schema.version < from_version:  # version too old
            return obj, schema

        try:
            obj[field] = converter(obj[field])
        except Exception as e:
            raise TypeError(f"failed to upgrade from {obj[field]} to {converter}")
        schema.fields[field] = converter
        return obj, schema
    return apply


def test1():
    v1_schema = define_schema(1, {
        "name": str,
        "age": int
    })
    v2_schema = define_schema(2, {
        "name": str,
        "age": int,
        "email": str  # New field
    })
    migrations = [
        AddField("email", default="unknown@example.com", from_version=1)
    ]
    
    old_data = serialize({"name": "Alice", "age": 30}, v1_schema)
    new_obj = deserialize(old_data, v2_schema, migrations)
    assert new_obj == {"name": "Alice", "age": 30, "email": "unknown@example.com"}
    print("test1 passed")

def test2():
    v1_schema = define_schema(1, {"score": int})
    v2_schema = define_schema(2, {"score": float})
    migrations = [
        ChangeType("score", converter=float, from_version=1)
    ]
    old_data = serialize({"score": 100}, v1_schema)
    new_obj = deserialize(old_data, v2_schema, migrations)
    assert new_obj == {"score": 100.0}
    print("test2 passed")

test1()
test2()

def test3():
    v1_schema = define_schema(1, {
        "name": str,
        "age": int,
    })
    v2_schema = define_schema(2, {
        "name": str,
        "age": int,
        "email": str,  # New field
        "secret": {
            "sex": str,
            "balance": float,
        }
    })
    migrations = [
        AddField("email", default="unknown@example.com", from_version=1),
        AddField("secret.sex", default="man", from_version=1),
        AddField("secret.balance", default=15.0, from_version=1),
    ]
    
    old_data = serialize({"name": "Alice", "age": 30}, v1_schema)
    new_obj = deserialize(old_data, v2_schema, migrations)
    assert new_obj == {"name": "Alice", "age": 30, "email": "unknown@example.com", "secret": {"sex": "man", "balance": 15}}
    print("test3 passed")

test3()