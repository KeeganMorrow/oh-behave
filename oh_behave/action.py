"""Action module"""
import enum
import oh_behave

class Action:
    """
    Action base class
    """
    def __init__(self, actor):
        self._actor = actor

    def execute(self):
        return self._execute()

    def failed(self):
        return self._failed()

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
