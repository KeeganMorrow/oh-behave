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
        try:
            self._actor = kwargs['actor']
        except KeyError as e:
            raise oh_behave.MissingArgumentException(self, self.__init__, str(e))

class ActionTimed(Action):
    """Action that takes a certain amount of time"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.timegoal = kwargs['timegoal']
        except KeyError as e:
            raise oh_behave.MissingArgumentException(self, self.__init__, str(e))
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
