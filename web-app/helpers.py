import os
import fnmatch
import shutil
import glob

# Miscellaneous functions


def split_list(list_to_split, position):
    first_part = list_to_split[:position]
    second_part = list_to_split[position:]
    return first_part, second_part


def get_arg(value, default):
    print value
    if value is None:
        print 'It is None'
        print default
        return default
    print 'It is not None'
    return value

# Files


def find(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)


def find_multi(pattern, path):
    file_paths = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                file_paths.append(os.path.join(root, name))
    return file_paths


def find_directories(path):
    print path
    return glob.glob(path + '*/')


def move_files(original_paths, destination_directory):
    for path in original_paths:
        os.rename(path, destination_directory + path.split('/')[-1])


def copy_files(original_paths, destination_directory, dont_copy=False):
    for path in original_paths:
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        if not dont_copy:
            try:
                shutil.copy2(path, destination_directory)
            except IOError as error:
                print error


def copy_tree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
