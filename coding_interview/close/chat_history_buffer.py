"""
11:14
"""
from enum import Enum
import struct
from typing import *
import random


class Role(Enum):
    """
    Represents the fixed set of roles a user can have.
    """
    SYSTEM = 0
    USER = 1
    ASSISTANT = 2

class ChatHistoryBuffer:
    """
    Attributes:
        index_user_number_to_offset: dict {
            user_number: offset
        }
    """
    def __init__(self):
        self.index_user_number_to_offset = {}

    def map_role_to_enum(self, role: str) -> Role:
        if role == "system":
            return Role.SYSTEM
        if role == "user":
            return Role.USER
        if role == "assistant":
            return Role.ASSISTANT
        raise ValueError(f"unknown role: {role}")

    def serialize(self, message: Dict) -> bytes:
        role = message["role"]
        content = message["content"]
        length = len(content)
        format = f"BI{length}s"
        mapped_role = self.map_role_to_enum(role)
        data = struct.pack(format, mapped_role.value, length, content.encode())
        return data

    def batch_serialize(self, messages: List[Dict]) -> bytes:
        result = bytes()
        for message in messages:
            result += self.serialize(message)
        
        self.data = result
        return result

    def batch_deserialize(self, data: bytes) -> List[Dict]:
        offset = 0
        user_number = 0
        while offset < len(data):
            self.index_user_number_to_offset[user_number] = offset
            # read header
            header_size = struct.calcsize("BI")
            role, length = struct.unpack("BI", data[offset:offset+header_size])
            offset += header_size
            content = struct.unpack(f"{length}s", data[offset:offset+length])[0].decode()
            offset += length
            user_number += 1
            yield {"role": Role(role).name.lower(), "content": content}

    def get_by_user_number(self, user_number: int) -> Dict:
        if user_number not in self.index_user_number_to_offset:
            print(self.index_user_number_to_offset)
            raise Exception(f"user number {user_number} not found")

        offset = self.index_user_number_to_offset[user_number]
        header_size = struct.calcsize("BI")
        role, length = struct.unpack("BI", self.data[offset:offset+header_size])
        offset += header_size
        content = struct.unpack(f"{length}s", self.data[offset:offset+length])[0].decode()
        return {"role": Role(role).name.lower(), "content": content}

    def deserialize(self, byte_array: bytes):
        # does this work?
        header_size = struct.calcsize("BI")
        role, length = struct.unpack("BI", byte_array[:header_size])
        content = struct.unpack(f"{length}s", byte_array[header_size:])
        content = content[0].decode()
        return {"role": Role(role).name.lower(), "content": content}

def mock_messsages(length: int):
    result = []
    for i in range(length):
        result.append({"role": "user" if i % 2 == 0 else "assistant", "content": f"message {i} {random.randint(0, 1000000)}"})
    return result


def test_mock_messages():
    messages = mock_messsages(10)
    for message in messages:
        test_obj(message)

    buffer = ChatHistoryBuffer()
    data = buffer.batch_serialize(messages)
    new_messages = list(buffer.batch_deserialize(data))
    if messages != new_messages:
        raise Exception(f"test failed: {messages} != {new_messages}, data: {data}")
    
    my_data_length = len(data)
    import json
    json_data = json.dumps(messages)
    json_data_length = len(json_data)
    print(f"my_data_length: {my_data_length}, json_data_length: {json_data_length}")
    print("test_mock_messages passed!")

def test_obj(obj):
    buffer = ChatHistoryBuffer()
    data = buffer.serialize(obj)
    new_obj = buffer.deserialize(data)
    if obj != new_obj:
        raise Exception(f"test failed: {obj} != {new_obj}, data: {data}")


def test():
    test_obj({"role": "user", "content": "hello"})
    print("test_obj passed!")

def test_get_by_user_number():
    messages = mock_messsages(10)
    buffer = ChatHistoryBuffer()
    data = buffer.batch_serialize(messages)
    list(buffer.batch_deserialize(data))
    for i in range(len(messages)):
        message = buffer.get_by_user_number(i)
        if message != messages[i]:
            raise Exception(f"test failed: {messages[i]} != {message}, data: {data}")
    print("test_get_by_user_number passed!")

test()
test_mock_messages()
test_get_by_user_number()