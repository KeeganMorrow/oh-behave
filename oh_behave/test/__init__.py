"""Behave module"""
# TODO: rename the mod directory

import enum

ERR_ABSTRACT_CALL = "Attempted to call abstract method"

class ExecuteResult(enum.Enum):
    """
    Represents results of executing a node

    Can be either a success, ready to run again, or failure
    """
    failure = -1
    ready = 0
    success = 1

