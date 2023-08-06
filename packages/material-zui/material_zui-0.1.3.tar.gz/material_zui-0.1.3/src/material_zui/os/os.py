import os
import sys
import shutil
from platform import platform


def is_mac() -> bool:
    '''
    Check current platform is `Mac` or not
    '''
    is_mac = False
    if not any(os_name in platform() for os_name in ["Windows", "Linux"]):
        is_mac = True
    return is_mac


def is_linux() -> bool: return sys.platform == "linux" or sys.platform == "linux2"


def is_window() -> bool: return sys.platform == "win64" or sys.platform == "win32"


def is_main() -> bool: return __name__ == "__main__"


def create_directory(directory_path: str) -> None:
    '''
    Check the exist of directory before create it
    '''
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)


def move(source_file_path: str, destination_directory_path: str) -> None:
    shutil.move(source_file_path, destination_directory_path)
