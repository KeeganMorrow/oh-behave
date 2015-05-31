"""Action module"""
import enum
import oh_behave
from oh_behave import behave

class Action(behave.Node):
    """
    Action base class
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actor = kwargs['actor']

class ActionTimed(Action):
    """Action that takes a certain amount of time"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timegoal = kwargs['timegoal']
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
