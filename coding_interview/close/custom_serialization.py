"""
1:26
2:21
"""
from types import NoneType


class Serializer:
    """
    1. primitive; special chars
    2. nested / list
    3. custom medatadata fields
    4. space-efficient, human-readable
    5. circular references
        handle the same object again
    6. < 2x JSON

    Procotol:
        type:data

    null:
    str:abc
    int:123
    list:[something,s2,s3]
    dict:[key1:value1,k2:v2,k3:v3]

    Attributes:
        visited_obj: set(), to detect circular dependency if handle the exact same object
    """
    def __init__(self):
        self.visited_obj = set()

    def serialize(self, obj) -> str:
        """
        1. check object type, serialized
        2. 
        """
        obj_type = type(obj)

        if obj_type == str:
            # need to escape special ch
            return f"str:{obj}"
        elif obj_type == int:
            return f"int:{obj}"
        elif obj_type == float:
            return f"float:{obj}"
        elif obj_type == bool:
            return f"bool:{obj}"
        elif obj_type == NoneType:
            return f"none:"
        elif obj_type == list:
            result = ",".join([self.serialize(item) for item in obj])
            return f"list:[{result}]"
        elif obj_type == dict:
            result = []
            for key, value in obj.items():
                item_result = f"{key}:{self.serialize(value)}"
                result.append(item_result)
            return f"dict:[{','.join(result)}]"
        raise Exception("serialize error")


    def deserialize(self, data: str):
        """"""
        if not isinstance(data, str):
            raise Exception(f"{data} is not str, is {type(data)}")

        splits = data.split(":")
        # if len(splits) <= 1:
        #     raise Exception(f"malformed data: {splits}")
        
        obj_type = splits[0]
        if obj_type == "str":
            return str(splits[1])
        if obj_type == "int":
            return int(splits[1])
        if obj_type == "float":
            return float(splits[1])
        if obj_type == "bool":
            if splits[1] == "True":
                return True
            else:
                return False
        if obj_type == "none":
            return None
        if obj_type == "list":
            content = data.removeprefix("list:")[1:][:-1]
            result = []
            while content:
                content, value = self.find_next_value(content)
                # print("debug", value, content)
                try:
                    result.append(self.deserialize(value))
                except Exception as e:
                    print(f"deserialize list error: {value} {content} {data}")
                    raise e
            return result
        if obj_type == "dict":
            content = data.removeprefix("dict:")[1:][:-1]
            result = {}
            while content.rstrip(","):  # it has more data after ,
                """
                key1:value1,key2:value2,
                1. find next key
                2. find next value
                3. find next ,
                """
                # print(content)
                content, key, value = self.find_next_token(content)
                # print(key, value, content)
                try:
                    result[key] = self.deserialize(value)
                except Exception as e:
                    print(f"error deserialize dict: {key} {value}")
                    raise e
            return result
        raise Exception(f"not implemented for {data}")

    def find_next_value(self, content):
        """find next value from list content
        """
        value = ""
        left_bracket = 0
        for ch in content:
            if ch == "[":
                left_bracket += 1
            elif ch == "]":
                left_bracket -= 1

            if ch == "," and left_bracket == 0:  # not in bracket
                break
            value += ch
        return content.removeprefix(value).removeprefix(","), value


    def find_next_token(self, content):
        """parse string to return key, value

        Assumption: key is always a string at beginning
        """
        key = content.split(":")[0]
        content = content.removeprefix(key).removeprefix(":")

        value = ""
        # find value
        left_bracket = 0
        for ch in content:
            if ch == "[":
                left_bracket += 1
            elif ch == "]":
                left_bracket -= 1

            if ch == "," and left_bracket == 0:  # not in bracket
                break
            value += ch
        # print(content, value)
        content = content.removeprefix(value).removeprefix(",")
        # print(content, key, value)
        return content, key, value


class Serializer2:

    def serialize(self, obj) -> str:
        """
        1. it can be nested up to 10 levels deep
        2. handle circular references
        """
        return self._serialize(obj, set(), 0)

    def _serialize(self, obj, visited_obj, depth=0) -> str:
        """
        Args:
            visited_obj: set() store visited obj id
            depth: int
        """
        if depth > 10:
            raise Exception("doesn't support more than 10 levels deep")

        if id(obj) in visited_obj:
            raise Exception("Circular reference: meet same object again")

        type_obj = type(obj)
        if type_obj == str:
            return f"s:{self.serialize_str(obj)}"
        if type_obj == int:
            return f"i:{obj}"
        if type_obj == float:
            return f"f:{obj}"
        if type_obj == bool:
            if obj:
                return f"b:true"
            else:
                return f"b:false"
        if type_obj == NoneType:
            return f"n:none"

        # begin handling complex object which needs
        # handle circular reference
        obj_id = id(obj)
        visited_obj.add(obj_id)
        depth += 1

        if type_obj == list:
            result = ",".join([self._serialize(item, visited_obj, depth) for item in obj])
            # finish digging deep, needs to remove from it
            visited_obj.remove(obj_id)
            return f"l:[{result}]"

        if type_obj == dict:
            result = []
            for key, value in obj.items():
                serialized_key = self._serialize(key, visited_obj, depth)
                serialized_value = self._serialize(value, visited_obj, depth)
                result.append(f"{serialized_key}:{serialized_value}")
            result = ",".join(result)
            # finish digging deep, needs to remove from it
            visited_obj.remove(obj_id)
            return f"d:[{result}]"

        raise TypeError(f"not supported type: {type_obj}")

    def serialize_str(self, string_raw):
        return string_raw

    def parse_string(self, string_raw):
        return string_raw

    def deserialize(self, data: str):
        if len(data) <= 1:
            raise Exception(f"malformed data: {data}")

        type_marker = data[0]
        data = data[2:]
        if type_marker == "s":
            return self.parse_string(data)
        if type_marker == "i":
            return int(data)
        if type_marker == "f":
            return float(data)
        if type_marker == "b":
            if data == "true":
                return True
            else:
                return False
        if type_marker == "n":
            return None

        if type_marker == "l":
            data = data[1:][:-1]
            result = []
            while data:
                next_part = self.find_next_comma(data)
                data = data.removeprefix(next_part).lstrip(",")
                try:
                    result.append(self.deserialize(next_part))
                except Exception as e:
                    print(f"error: {next_part} {data}")
                    raise e
            return result

        if type_marker == "d":
            data = data[1:][:-1]
            result = {}
            while data:
                # keep finding next part
                next_part = self.find_next_comma(data)
                data = data.removeprefix(next_part).lstrip(",")
                print(data)

                serialized_key, serialized_value = self.parse_key_value(next_part)
                try:
                    key = self.deserialize(serialized_key)
                    value = self.deserialize(serialized_value)
                except Exception as e:
                    print(f"error: {next_part} {serialized_key} {serialized_value} {data}")
                    raise e
                result[key] = value
            return result

        raise TypeError(f"not supported type: {type_marker}")

    def find_next_comma(self, data):
        result = ""
        left_bracket = 0
        for ch in data:
            if ch == "[":
                left_bracket += 1
            if ch == "]":
                left_bracket -= 1

            if ch == "," and left_bracket == 0:
                return result
            result += ch
        return result

    def parse_key_value(self, data):
        splits = data.split(":")
        key = ":".join([splits[0], splits[1]])
        value = data.removeprefix(key).lstrip(":")
        return key, value



def serialize(obj) -> str:
    mySerializer = Serializer2()
    return mySerializer.serialize(obj)

def deserialize(data: str):
    mySerializer = Serializer2()
    return mySerializer.deserialize(data)


def test_obj(obj):
    data = serialize(obj)
    # print(obj, data)
    new_obj = deserialize(data)
    print(obj, data, new_obj)
    if obj != new_obj:
        raise Exception(f"test failed: {obj} != {new_obj}, data: {data}")
    assert obj == new_obj


def test():
    objs = [3.5, -2.2, 0, 1, -1, "abc", True, False, "", None]
    for obj in objs:
        test_obj(obj)

    test_obj(objs)
    # test_obj({"a": 1, -2: 3.1415})
    example1 = {
        "model": "gpt-4",
        "usage": {"prompt_tokens": 100, "completion_tokens": 50},
        "choices": [{"text": "Hello", "index": 0}]
    }
    test_obj(example1)

    example2 = {
        "data": [1, 2.5, "text", None, {"nested": True}],
        "metadata": {"version": "1.0"}
    }
    test_obj(example2)

    print("test passed!")


def test_quote():
    objs = ["\"", "\\", "\n", "\:", '', '"acutal"']
    for obj in objs:
        test_obj(obj)

    test_obj(objs)
    test_obj({"a\bcd": 1, "\\\bc": 1.55})
    print("quote passed!")

def test_comma():
    objs = ["a,b", "a,,b", ",,,"]
    for obj in objs:
        test_obj(obj)
    test_obj(objs)
    print("comma passed!")


test()
test_quote()
test_comma()