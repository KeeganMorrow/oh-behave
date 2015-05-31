"""Behavior Module"""
#TODO: Come up with a better name!

import enum

ERR_ABSTRACT_CALL = "Attempted to call abstract method"

def print_node_decorator(func):
    """
    Returns decorator function that prints execution information
    """

    def func_decorator(self, *args, **kwargs):
        """See print_node_decorator documentation"""
        print('{0}.{1} running'.format(self.get_name(), func.__name__))

        ret = func(self, *args, **kwargs)

        msg = '{0}.{1} finished'.format(self.get_name(), func.__name__)
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
    def __init__(self, name):
        self._name = name

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

    def get_name(self):
        """
        Method to read the name variable
        """
        return self._name

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
    def __init__(self, name):
        super().__init__(name)
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

    def __init__(self, name):
        super().__init__(name)
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


class NodeSelector(NodeComposite):
    """Sequence node class"""

    def __init__(self, name):
        super().__init__(name)
        self.name = 'sequence'

    def _success(self):
        pass

    def _failed(self):
        pass

    def _execute(self):
        """Execute until one of the children succeed"""

        if len(self._children) == 0:
            status = ExecuteResult.failure
        else:
            firstnode = self._children[0]
            status = firstnode.execute()
            if status is ExecuteResult.failure:
                firstnode.failed()
                self._children.pop(0)
                if len(self._children) == 0:
                    status = ExecuteResult.failure
                else:
                    status = ExecuteResult.ready

            elif status is ExecuteResult.success:
                firstnode.success()

        return status

class NodeDecorator(Node):
    """Base Decorator, passes everything through"""

    def __init__(self, name, decoratee):
        super().__init__(name)
        self._decoratee = decoratee

    def _success(self):
        self._decoratee.success()

    def _failed(self):
        self._decoratee.failed()

    def _execute(self):
        return self._decoratee.execute()

class NodeDecoratorInvert(NodeDecorator):
    """Inverts execute result of child node"""
    def _execute(self):
        status = self._decoratee.execute()
        if status is ExecuteResult.success:
            status = ExecuteResult.failure
        elif status is ExecuteResult.failure:
            status = ExecuteResult.success
        return status

class NodeLeafIterative(Node):
    """Node that takes a number of executions before success"""

    def __init__(self, name, executions):
        super().__init__(name)
        self._remaining_exec = executions

    def _success(self):
        pass

    def _failed(self):
        pass

    def _execute(self):
        """Execute until enough iterations for success"""
        #TODO: _remaining_exec should possibly be stored in the actor?
        if self._remaining_exec < 1:
            ret = ExecuteResult.success
        elif self._remaining_exec == 1:
            ret = ExecuteResult.success
            self._remaining_exec -= 1
        else:
            ret = ExecuteResult.ready
            self._remaining_exec -= 1
        return ret


