"""
5:33
6:24
"""
import numbers
import pickle
from typing import *
from dataclasses import dataclass


@dataclass
class Schema:
    name: str
    value: Any

@dataclass
class Compression:
    schema_name: str
    delta: float = 0


class SameSchemaSerializer:
    """
    1. store the same schema
    2. repeat value
    3. random access

    {"prompt": "Hello", "max_tokens": 100, "temperature": 0.7, "model": "gpt-4"}
    -> {k1: Compression(k1, v1), k2: k2v2, k3}
    -> {k1: k2, k3: delta}
    key = Compression(schema_name)
    value = Compression(schema_name, delta)
    Attributes:
        schemas: {
            schema_name: Schema
        }
        compressions: {
            key: Compression(schema_name, delta)
        }
        compress_data: []
        max_row_size: int, max row size for compression, exceed it would fail 
    """
    def __init__(self):
        self.schemas: Dict[str, Schema] = {}
        self.compressions: Dict[str, Compression] = {}
        self.max_row_size = 0

    def find_next_name(self):
        """find next available compression symbol
        """
        count = len(self.schemas)
        name = f"c{count}"
        if name not in self.schemas:
            return name
        raise Exception(f"{name} already used in {self.schemas}")
    
    def register_str(self, key):
        """given key, compress it
        """
        name = self.find_next_name()
        self.schemas[name] = Schema(name, key)
        self.compressions[key] = Compression(name)
    
    def register_number(self, key, value):
        name = self.find_next_name()
        self.schemas[key] = Schema(key, value)
    
    def compress_str(self, data: str):
        """Given key, either find corresponding compression name or register a new name"""
        if data in self.compressions:
            return self.compressions[data].schema_name
    
        self.register_str(data)
        return self.compressions[data].schema_name

    def decompress_str(self, compressed_str: str):
        return self.schemas[compressed_str].value

    def compress_number(self, key, value):
        schema = self.schemas[key]
        base_value = schema.value
        return value - base_value

    def decompress_number(self, key, value):
        schema = self.schemas[key]
        base_value = schema.value
        return base_value + value
    
    def calculate_max_row_size(self, compressed):
        data = pickle.dumps(compressed)
        self.max_row_size = 2 * len(data)
    
    def register(self, request):
        """use a single object to register schema"""
        for key, value in request.items():
            if isinstance(value, numbers.Number):
                self.register_number(key, value)
            else:
                self.register_str(key)
    
    def compress(self, request) -> Dict:
        result = {}
        for key, value in request.items():
            if isinstance(value, numbers.Number):  # it must register before
                schema_name = key
                compress_value = self.compress_number(key, value)
            else:
                schema_name = self.compress_str(key)
                compress_value = self.compress_str(value)
            result[schema_name] = compress_value
        return result

    PADDING_BYTE = b"\x00"

    def compressed_to_bytes(self, compressed) -> bytes:
        data = pickle.dumps(compressed)
        if len(data) > self.max_row_size:
            raise ValueError(f"{len(data)} exceeds {self.max_row_size}")

        result = data.ljust(self.max_row_size, self.PADDING_BYTE)
        return result

    def bytes_to_compressed(self, data) -> Dict:
        result = data.rstrip(self.PADDING_BYTE)
        obj = pickle.loads(result)
        return obj

    def decompress(self, compressed) -> Dict:
        result = {}
        for compressed_key, compressed_value in compressed.items():
            if isinstance(compressed_value, numbers.Number):
                key = compressed_key
                value = self.decompress_number(compressed_key, compressed_value)
            else:
                key = self.decompress_str(compressed_key)
                value = self.decompress_str(compressed_value)
            result[key] = value
        return result
    
    def serialize_batch(self, requests: List[Dict]) -> bytes:
        """Serialize a batch
        for each object
        1. map each field to corresponding schema: key -> schema
        2. map each value to corresponding value_mapping: value -> value_mapping
        """
        self.register(requests[0])
        compressed = self.compress(requests[0])
        self.calculate_max_row_size(compressed)
        print(self.schemas, self.compressions)
        result = bytes()
        for index, request in enumerate(requests):
            compressed = self.compress(request)
            result += self.compressed_to_bytes(compressed)
        return result
    
    def deserialize_batch(self, data: bytes) -> List[Dict]:
        """Deserialize entire batch"""
        start = 0
        result = []
        while start < len(data):
            chunk = data[start: start + self.max_row_size]
            compressed = self.bytes_to_compressed(chunk)
            plain = self.decompress(compressed)
            result.append(plain)
            start += self.max_row_size
        print(result)
        return result
    
    def get_request_at(self, data: bytes, index: int) -> Dict:
        """Access single request without full deserialization"""
        start = index * self.max_row_size
        chunk = data[start: start + self.max_row_size]
        compressed = self.bytes_to_compressed(chunk)
        plain = self.decompress(compressed)
        return plain


def test1():
    requests = [
        {"prompt": "Hello", "max_tokens": 100, "temperature": 0.7, "model": "gpt-4"},
        {"prompt": "World", "max_tokens": 105, "temperature": 0.8, "model": "gpt-4"},
        {"prompt": "Test", "max_tokens": 95, "temperature": 0.5, "model": "gpt-4"}
    ]
    serializer = SameSchemaSerializer()
    data = serializer.serialize_batch(requests)
    # Should be significantly smaller than naive JSON serialization
    assert serializer.deserialize_batch(data) == requests
    assert serializer.get_request_at(data, 1) == requests[1]
    print("test 1 passed!")


def test2():
    requests = [
        {"user_id": 123, "action": "query", "timestamp": 1000000},
        {"user_id": 123, "action": "query", "timestamp": 1000001},
        {"user_id": 456, "action": "update", "timestamp": 1000002}
    ]
    serializer = SameSchemaSerializer()
    data = serializer.serialize_batch(requests)
    print("test 2 passed!")

test1()
test2()