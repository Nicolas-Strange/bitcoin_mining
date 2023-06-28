""" All about managing files
"""
import os
from csv import writer


def create_folders(path: str) -> None:
    """
    create the folder if not existing
    :param path: path to the folder
    """
    if not os.path.exists(path):
        os.makedirs(path)


def save_csv(path: str, row: list) -> None:
    with open(path, 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(row)
        f_object.close()

