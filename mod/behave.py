"""Behavior Module"""
#TODO: Come up with a better name!

import enum

ERR_ABSTRACT_CALL = "Attempted to call abstract method"

def print_node_decorator(func):

    def func_decorator(*args, **kwargs):
        msg = '{0} running'.format(func.__name__)
        ret = func(*args, **kwargs)
        if ret in ExecuteResult:
            msg += ' returns status \"{0}\"'.format(str(ret))
        print(msg)
        return ret

    return func_decorator

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

    @print_node_decorator
    def execute(self):
        """
        Wrapper with some common code for execution of nodes
        """
        ret = self._execute()
        return ret

    @print_node_decorator
    def failed(self):
        """
        Wrapper with some common code for execution of nodes
        """
        ret = self._failed()
        return ret

    @print_node_decorator
    def success(self):
        """
        Wrapper with some common code for success methods of nodes
        """
        ret = self._success()
        return ret

    def _execute(self):
        """
        Abstract private method for executing the node

        Implementations should return an ExecuteResult
        """
        raise NotImplementedError(ERR_ABSTRACT_CALL)

    def _failed(self):
        """
        Abstract method to run on node failure
        """
        raise NotImplementedError(ERR_ABSTRACT_CALL)

    def _success(self):
        """
        Abstract method to run on node success
        """
        raise NotImplementedError(ERR_ABSTRACT_CALL)

class NodeComposite(Node):
    """Abstract Base composite node class"""
    def __init__(self):
        super().__init__()
        self._children = []

    def addchild(self, childnode):
        """
        Wrapper with some common code for addchild methods of composite nodes
        """
        return self._addchild(childnode)
    def _addchild(self, childnode):
        """ Add a child to the composite node"""
        self._children.append(childnode)

class NodeSequence(NodeComposite):
    """Sequence node class"""

    def __init__(self):
        super().__init__()
        self.name = 'sequence'

    def _success(self):
        pass

    def _failed(self):
        pass

    def _execute(self):
        """Execute the child nodes in a sequence"""

        if len(self._children) == 0:
            status = ExecuteResult.success
        else:
            firstnode = self._children[0]
            status = firstnode.execute()
            if status is ExecuteResult.success:
                firstnode.success()
                self._children.pop(0)
                if len(self._children) == 0:
                    status = ExecuteResult.success
                else:
                    status = ExecuteResult.ready

            elif status is ExecuteResult.failure:
                firstnode.failed()

        return status

