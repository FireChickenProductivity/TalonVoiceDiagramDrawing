import os

def create_directory_if_nonexistent(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_absolute_path(path):
    return os.path.isabs(path)

def join_path(directory, path):
    return os.path.join(directory, path)

def compute_directory_at_path(path):
    if os.path.isdir(path):
        return path
    else:
        return compute_file_directory(path)

def compute_file_directory(path):
    absolute_filepath = os.path.abspath(path)
    file_directory = os.path.dirname(absolute_filepath)
    return file_directory