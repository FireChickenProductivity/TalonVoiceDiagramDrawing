import os
from .mouse_position import MousePosition
from .path_utilities import create_directory_if_nonexistent, is_absolute_path, join_path, compute_directory_at_path, compute_file_directory
from .json_conversion import JSONConverter

class DirectoryRelativeException(Exception):
    pass

DEFAULT_MAX_BYTES = 50000000
class Storage:
    #Half a gigabyte
    def __init__(self, directory, *, max_bytes = DEFAULT_MAX_BYTES):
        if is_absolute_path(directory):
            self.directory = directory
        else:
            raise DirectoryRelativeException(directory)
        create_directory_if_nonexistent(self.directory)
        self.max_bytes = max_bytes

    def get_position_file(self, name: str):
        return self.get_storage_file(name, MousePositionFile) 
    
    def get_integer_file(self, name: str):
        return self.get_storage_file(name, IntegerFile)
    
    def get_float_file(self, name: str):
        return self.get_storage_file(name, FloatFile)
    
    def get_string_file(self, name: str):
        return self.get_storage_file(name, StringFile)
    
    def get_boolean_file(self, name: str):
        return self.get_storage_file(name, BooleanFile)

    def get_json_file(self, name: str, from_json = None, *, default = None, cls = None, initial_value = None):
        return JSONFile(self.get_path(), name, from_json = from_json, default = default, cls = cls, 
        initial_value = initial_value)

    def get_storage_file(self, name: str, type):
        return type.create(self.get_path(), name, max_bytes = self.max_bytes)

    def get_path(self):
        return self.directory


class RelativeStorage(Storage):
    def __init__(self, path, name = 'Fire Chicken Storage', *, max_bytes = DEFAULT_MAX_BYTES):
        target_directory = compute_directory_at_path(path)
        dir = join_path(target_directory, name)
        Storage.__init__(self, dir, max_bytes = max_bytes)


#Parent class not meant to be instantiated
#Implement Python string method for storing object for storage
    #or override _convert_to_text
#Implement classmethod get_value_from_text for reading from the file
#Implement _get_initial_value for setting the initial value
class StorageFile:
    def __init__(self, directory: str, name: str, *, max_bytes: int = DEFAULT_MAX_BYTES):
        self.directory = directory
        self.name = name
        self.max_bytes = max_bytes
        self._initialize_file_if_nonexistent()
        self._load_value_from_file()
    @classmethod
    def create(cls, directory: str, name: str, *, max_bytes: int = DEFAULT_MAX_BYTES):
        return cls(directory, name, max_bytes = max_bytes)


    def get(self):
        return self.value
    
    def set(self, value):
        self.value = value
        self._store_value()
    
    def _store_value(self):
        with open(self.get_path(), 'w') as value_file:
            value_text = self._convert_to_text()
            value_file.write(value_text)
    
    def _convert_to_text(self) -> str:
        return str(self.value)

    def _load_value_from_file(self):
        if self._file_too_big():
            self._raise_file_too_big_exception()
        with open(self.get_path(), 'r') as position_file:
            value_text = position_file.read(self.max_bytes)
            self.value = self.get_value_from_text(value_text)

    def _file_too_big(self):
        file_size = os.path.getsize(self.get_path())
        return file_size > self.max_bytes

    def _raise_file_too_big_exception(self):
        raise InvalidFileSizeException(f'Storage file at path {self.get_path()} exceeded maximum size of'
        f'{self.max_bytes} bytes!'
        )

    def get_path(self):
        return os.path.join(self.directory, self.name)

    def _initialize_file_if_nonexistent(self):
        if self.exists():
            self.initialize()
    def exists(self):
        return not os.path.exists(self.get_path())
    def initialize(self):
        self._make_directory_if_nonexistent()
        initial_value = self._get_initial_value()
        self.set(initial_value)
    
    def _make_directory_if_nonexistent(self):
        create_directory_if_nonexistent(self.directory)
    
    def delete(self):
        os.remove(self.get_path())

class JSONFile(StorageFile):
    def __init__(self, folder: str, name: str, *, max_bytes: int = DEFAULT_MAX_BYTES, initial_value = None, 
        default = None, cls = None, from_json = None):
        self.initial_value = initial_value
        self.converter = JSONConverter(from_json, to_json_function = default, to_json_class = cls)
        StorageFile.__init__(self, folder, name, max_bytes = max_bytes)

    def _convert_to_text(self) -> str:
        return self.converter.convert_object_to_json(self.value)
  
    def get_value_from_text(self, text: str):
        return self.converter.convert_json_to_object(text)
    
    def _get_initial_value(self):
        return self.initial_value

    
class InvalidFileSizeException(Exception):
    pass

class MousePositionFile(StorageFile):
    def set_to_current_mouse_position(self):
        position = MousePosition.current()
        self.set(position)
    
    @classmethod
    def get_value_from_text(self, text: str):
        return MousePosition.from_text(text)
    
    def _get_initial_value(self):
        return MousePosition(0, 0)
    
class IntegerFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return int(text)
    
    def _get_initial_value(self):
        return 0

class FloatFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return float(text)
    
    def _get_initial_value(self):
        return 0.0
    
class StringFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return text
    
    def _get_initial_value(self):
        return ''

class BooleanFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return text == 'True'
    
    def _get_initial_value(self):
        return False

