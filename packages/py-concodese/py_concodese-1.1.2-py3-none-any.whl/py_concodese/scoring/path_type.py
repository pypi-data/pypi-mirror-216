from enum import Enum


class PathType(Enum):
    RELATIVE = 0
    NAMESPACE = 1


def calc_path_type(string) -> PathType:
    """ calculates the type of path used in a string """
    path_type = PathType.NAMESPACE
    if "/" in string:
        path_type = PathType.RELATIVE

    return path_type
