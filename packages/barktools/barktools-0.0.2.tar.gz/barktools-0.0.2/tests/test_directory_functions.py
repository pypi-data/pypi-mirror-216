import os
from os.path import join

from barktools.base_utils import find_nbr_of_files, list_files, list_files_recursive

from tests.test_helper import EXAMPLE_DIR

def test_find_nbr_of_files():
    n_files_1 = find_nbr_of_files(EXAMPLE_DIR)
    assert n_files_1 == 5
    n_files_2 = find_nbr_of_files(EXAMPLE_DIR, extension='txt')
    assert n_files_2 == 4

def test_list_files():
    files_gt = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.file"]
    files_1 = list_files(EXAMPLE_DIR)
    assert set(files_1) == set(files_gt)
    files_2 = list_files(EXAMPLE_DIR, include_dir=True)
    assert set(files_2) == set([join(EXAMPLE_DIR, file) for file in files_gt])
    files_3 = list_files(EXAMPLE_DIR, extension="txt")
    assert set(files_3) == set(files_gt[:-1])
    files_4 = list_files(EXAMPLE_DIR, extension="txt", include_dir=True)
    assert set(files_4) == set([join(EXAMPLE_DIR, file) for file in files_gt[:-1]])

def test_list_files_recursive():
    files_gt = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.file", \
        "subdirectory"+os.sep+"file1.txt", "subdirectory"+os.sep+"file2.txt", \
        "subdirectory"+os.sep+"subsubdirectory"+os.sep+"file1.file"]
    files_1 = list_files_recursive(EXAMPLE_DIR)
    assert set(files_1) == set(files_gt)
    files_2 = list_files_recursive(EXAMPLE_DIR, extension="file")
    assert set(files_2) == set([file for file in files_gt if file.endswith("file")])
    files_3 = list_files_recursive(EXAMPLE_DIR, include_dir=True)
    assert set(files_3) == set([join(EXAMPLE_DIR, file) for file in files_gt])
    files_4 = list_files_recursive(EXAMPLE_DIR, extension=("txt", "file"))
    assert set(files_4) == set([file for file in files_gt if ((file.endswith("txt")) or (file.endswith("file")))])
    files_5 = list_files_recursive(EXAMPLE_DIR, extension=["txt", "file"])
    assert set(files_5) == set([file for file in files_gt if ((file.endswith("txt")) or (file.endswith("file")))])