"""Behavior Module"""
#TODO: Come up with a better name!

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

class Node:
    """Base node class"""
    def __init__(self):
        pass

    def success(self):
        """
        Abstract method to run on node completion
        """
        raise NotImplementedError(ERR_ABSTRACT_CALL)

    def execute(self):
        """
        Abstract method for executing the node

        Implementations should return an ExecuteResult
        """
        raise NotImplementedError(ERR_ABSTRACT_CALL)

    def failed(self):
        """
        Abstract method to run on node failure
        """
        raise NotImplementedError(ERR_ABSTRACT_CALL)

class NodeComposite(Node):
    """Abstract Base composite node class"""
    def __init__(self):
        super().__init__()
        self._children = []

    def addchild(self, childnode):
        """ Add a child to the composite node"""
        self._children.append(childnode)

class NodeSequence(NodeComposite):
    """Sequence node class"""

    def __init__(self):
        super().__init__()

    def success(self):
        pass

    def failed(self):
        pass

    def execute(self):
        """Execute the child nodes in a sequence"""
        if len(self._children) == 0:
            return ExecuteResult.success

        firstnode = self._children[0]
        status = firstnode.execute()
        if status is ExecuteResult.success:
            firstnode.success()
            self._children.pop(0)
            if len(self._children) == 0:
                status =  ExecuteResult.success
            else:
                status =  ExecuteResult.ready

        elif status is ExecuteResult.failure:
            firstnode.failed()
        return status

class NodePrintLeaf(Node):
    """
    Simple leaf for initial testing purposes
    """
    def __init__(self, executemsg, failmsg, completemsg, status):
        super().__init__()
        self.executemsg = executemsg
        self.failmsg = failmsg
        self.completemsg = completemsg
        self.status = status

    def success(self):
        print(self.completemsg)

    def failed(self):
        print(self.failmsg)

    def execute(self):
        print(self.executemsg)
        return self.status


