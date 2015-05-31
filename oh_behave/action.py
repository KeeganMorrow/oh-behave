"""Action module"""
import enum
import oh_behave

def print_node_decorator(func):
    """
    Returns decorator function that prints execution information
    """

    def func_decorator(self, *args, **kwargs):
        """See print_node_decorator documentation"""
        print('Action {0}.{1} running'.format(
            self.__class__.__name__,
            func.__name__))

        ret = func(self, *args, **kwargs)

        msg = 'Action {0}.{1} finished.'.format(self.__class__.__name__, func.__name__)
        if ret in oh_behave.ExecuteResult:
            msg += ' returns status \"{0}\"'.format(str(ret))
        print(msg)

        return ret

    return func_decorator

class Action:
    """
    Action base class
    """
    def __init__(self, actor):
        self._actor = actor

    @print_node_decorator
    def execute(self):
        return self._execute()

    @print_node_decorator
    def failed(self):
        return self._failed()

    @print_node_decorator
    def success(self):
        return self._success()

    def _execute(self):
        """
        Abstract execute method

        Overriders must return type oh_behave.ExecuteResult
        """
        raise NotImplementedError(oh_behave.ERR_ABSTRACT_CALL)

    def _failed(self):
        """
        Abstract execute method

        Overriders must return type oh_behave.ExecuteResult
        """
        raise NotImplementedError(oh_behave.ERR_ABSTRACT_CALL)

    def _success(self):
        """
        Abstract execute method

        Overriders must return type oh_behave.ExecuteResult
        """
        raise NotImplementedError(oh_behave.ERR_ABSTRACT_CALL)

class ActionTimed(Action):
    """Action that takes a certain amount of time"""
    def __init__(self, actor, time):
        self.timegoal = time
        self.time = 1

    def _execute(self):
        if self.time>= self.timegoal:
            status = oh_behave.ExecuteResult.success
        else:
            status = oh_behave.ExecuteResult.ready
        self.time += 1
        return status

    def _failed(self):
        pass
    def _success(self):
        pass
