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
