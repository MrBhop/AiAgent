import os

def get_files_info(working_directory, directory=None):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_directory = absolute_working_directory
        if directory != None:
            target_directory = os.path.abspath(os.path.join(absolute_working_directory, directory))

        if not target_directory.startswith(absolute_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the premitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        output = []
        for item in os.listdir(target_directory):
            path = os.path.join(target_directory, item)
            output.append(f' - {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}')

        return '\n'.join(output)

    except Exception as e:
        return f'Error: {e}'
