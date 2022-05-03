from ast import arg
from importlib.metadata import files
import os
import sys
from unittest.mock import patch


def main():
    args = sys.argv

    if len(args) >= 2:
        path = args[1]
        files = os.listdir(path=path)
        file_list = [f for f in files if os.path.isdir(os.path.join(args[1], f))]

        for file in file_list:
            src_title = "{}/{}".format(path, file)

            rename_title = file.replace('】', '').replace('【', '').replace('(FREEing)', '')
            rename_title = "{}/{}".format(path, rename_title)
            os.rename(src_title, rename_title)

if __name__ == '__main__':
    main()