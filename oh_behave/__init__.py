"""oh_behave module"""

import enum

class ExecuteResult(enum.Enum):
    """
    Represents results of executing a node

    Can be either a success, ready to run again, or failure
    """
    failure = -1
    ready = 0
    success = 1

class MissingArgumentException(ValueError):
    def __init__(self, methodclass, method, argument):
        msg = "Method {0}.{1} missing required argument {2}".format(
                methodclass.__class__.__name__, method.__name__, argument)
        super().__init__(msg)
