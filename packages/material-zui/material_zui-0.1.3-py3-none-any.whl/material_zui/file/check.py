import os


def file_exists(file_path: str) -> bool:
    """Checks if the file exists.
    Args:
      filename: The name of the file to check.
    Returns:
      True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def directory_exists(directory_path: str) -> bool:
    """Checks if the directory exists.
    Args:
      path: The path of the directory to check.

    Returns:
      True if the directory exists, False otherwise.
    """
    return os.path.isdir(directory_path) and os.path.exists(directory_path)
