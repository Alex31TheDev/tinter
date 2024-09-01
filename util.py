from os import path, listdir

def get_files(dir_path):
    files = [f for f in listdir(dir_path) if path.isfile(path.join(dir_path, f))]
    return files