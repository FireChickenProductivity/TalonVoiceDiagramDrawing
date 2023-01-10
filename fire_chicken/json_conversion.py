import json

class JSONConverter:
    def __init__(self, from_json, *, to_json_function = None, to_json_class = None):
        self.json_from_object_converter = JSONFromObjectConverter(to_json_function = to_json_function, to_json_class = to_json_class)
        self.object_from_json_converter = ObjectFromJSONConverter(from_json)

    def convert_object_to_json(self, value):
        return self.json_from_object_converter.convert_object(value)

    def convert_json_to_object(self, text):
        return self.object_from_json_converter.convert_json(text)

class ObjectFromJSONConverter:
    def __init__(self, object_from_json):
        self.object_from_json = self._get_from_json_function(object_from_json)
    @classmethod
    def _get_from_json_function(cls, from_json):
        if cls._from_json_function_is_method(from_json):
            return cls._get_from_json_function_from_class(from_json)
        else:
            return from_json
    @classmethod
    def _get_from_json_function_from_class(cls, classname):
        return lambda value : classname.from_json(value)
    @classmethod
    def _from_json_function_is_method(cls, from_json):
        return cls._has_from_json_attribute(from_json) \
           and cls._has_callable_from_json_attribute(from_json)
    @classmethod
    def _has_from_json_attribute(cls, from_json):
        return hasattr(from_json, 'from_json')
    @classmethod
    def _has_callable_from_json_attribute(cls, from_json):
        return callable(from_json.from_json)

    def convert_json(self, text):
        json_value = self._convert_json_using_default_decoding(text)
        if _value_unavailable(self.object_from_json):
            return json_value
        return self.object_from_json(json_value)
    @classmethod
    def _convert_json_using_default_decoding(cls, text):
        return json.loads(text)

class JSONFromObjectConverter:
    def __init__(self, *, to_json_function, to_json_class):
        self.json_from_object = self._get_json_from_object_function(to_json_function, to_json_class)

    @classmethod
    def _get_json_from_object_function(cls, to_json_function, to_json_class):
        cls._raise_exception_if_invalid_json_from_object_argument_combination(to_json_function, to_json_class)
        if _value_provided(to_json_function):
            return cls._get_json_from_object_function_using_converter_function(to_json_function)
        if _value_provided(to_json_class):
            return cls._get_json_from_object_function_using_converter_class(to_json_class)
        return None
    @classmethod
    def _raise_exception_if_invalid_json_from_object_argument_combination(cls, to_json_function, to_json_class):
        if _values_provided(to_json_function, to_json_class):
            raise ValueError('JSONFile objects should not receive default and cls')
    @classmethod
    def _get_json_from_object_function_using_converter_function(cls, function):
        return lambda value : json.dumps(value, default = function)
    @classmethod
    def _get_json_from_object_function_using_converter_class(cls, converter_class):
        return lambda value : json.dumps(value, cls = converter_class)

    def convert_object(self, value) -> str:
        if _value_provided(self.json_from_object):
            return self.json_from_object(value)
        if self._value_has_encoder_method(value):
            return self._encode_using_encoder_method(value)
        return self._encode_using_json_default_encoding(value)
    @classmethod
    def _value_has_encoder_method(cls, value):
        return cls._value_has_to_json_attribute(value) \
           and cls._value_has_callable_to_json_attribute(value)
    @classmethod
    def _value_has_to_json_attribute(cls, value):
        return hasattr(value, 'to_json')
    @classmethod
    def _value_has_callable_to_json_attribute(cls, value):
        return callable(value.to_json)
    @classmethod
    def _encode_using_encoder_method(cls, value):
        json_object = value.to_json()
        return cls._encode_using_json_default_encoding(json_object)
    @classmethod
    def _encode_using_json_default_encoding(cls, value):
        return json.dumps(value)

    
def _value_provided(value):
    return value is not None
def _values_provided(*args):
    for value in args:
        if _value_unavailable(value):
            return False
    return True
def _value_unavailable(value):
    return value is None
