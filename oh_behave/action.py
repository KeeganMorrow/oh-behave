"""Action module"""
import enum
import oh_behave
from oh_behave import behave

class Action(behave.Node):
    """
    Action base class
    """
    def __init__(self, actor, name):
        super().__init__(name)
        self._actor = actor

class ActionTimed(Action):
    """Action that takes a certain amount of time"""
    def __init__(self, actor, name, time):
        super().__init__(actor, name)
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
