import os

def target_is_in_working_directory(absolute_path_to_working_directory, absolute_path_to_target):
    return absolute_path_to_target.startswith(absolute_path_to_working_directory)

def get_absolute_target_path(absolute_path_to_working_directory, target=None):
    if target is None:
        return absolute_path_to_working_directory
    else:
        return os.path.abspath(os.path.join(absolute_path_to_working_directory, target))
