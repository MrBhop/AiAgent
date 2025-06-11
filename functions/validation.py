import os

def target_is_in_working_directory(absolute_path_to_working_directory, absolute_path_to_target):
    return absolute_path_to_target.startswith(absolute_path_to_working_directory)

def get_absolute_target_path(absolute_path_to_working_directory, directory=None):
    target = absolute_path_to_working_directory
    if directory != None:
        target = os.path.abspath(os.path.join(absolute_path_to_working_directory, directory))

    return target
