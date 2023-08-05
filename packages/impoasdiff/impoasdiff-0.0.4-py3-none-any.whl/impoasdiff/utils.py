
import os
def get_diff_mapping(src_dir, tar_dir):
    src_files = get_file_names(src_dir)
    tar_files = get_file_names(tar_dir)
    src_tar_map = _generate_mapping(src_files, tar_files)
    return src_tar_map

def get_src_tar_file_relative(src_dir, tar_dir):
    src_files = get_file_names_with_parent_dir(src_dir)
    tar_files = get_file_names_with_parent_dir(tar_dir)
    return src_files, tar_files


def _generate_mapping(src_files, tar_files):
    src_tar_map = {}
    for file in src_files:
        _key = file.split("_")[1].split("-")[0].lower()
        for tar_file in tar_files:
            if _key in tar_file.lower():
                src_tar_map [file] = tar_file
                break
    return src_tar_map


def get_file_names(directory):
    file_names = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_names.append(filename)

    return file_names


def get_file_names_with_parent_dir(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_names.append(file_path)
    return file_names