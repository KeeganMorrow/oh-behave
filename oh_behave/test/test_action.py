"""Unit tests for actions module"""

import unittest
from unittest import mock
import oh_behave
from oh_behave import actor
from oh_behave import action

class TestAction(unittest.TestCase):
    def setUp(self):
        self.actor = mock.Mock(spec=actor.Actor)
        self.action = action.Action(actor=self.actor, name='Sleep')

    def test_action__init__(self):
        """Tests that __init__ properly sets up action actor"""
        name = 'node00'
        act = mock.Mock()
        node = action.Action(name=name, actor=act)
        self.assertIs(node._actor, act)

    def test_action__init__no_actor(self):
        """Not providing an actor results in an exception being raised"""
        with self.assertRaises(oh_behave.MissingArgumentException):
            node = action.Action(name='asdf')

    def test_action_execute_passthrough(self):
        """The execute call is correctly passed through"""
        with mock.patch.object(self.action, '_execute', autospec=True) as mock_execute:
            expected_ret = mock.Mock()
            mock_execute.return_value = expected_ret
            ret = self.action.execute()
            self.assertEqual(expected_ret, ret)
            mock_execute.assert_called_with()

    def test_action_failed_passthrough(self):
        """The failed call is correctly passed through"""
        with mock.patch.object(self.action, '_failed', autospec=True) as mock_failed:
            expected_ret = mock.Mock()
            mock_failed.return_value = expected_ret
            ret = self.action.failed()
            self.assertEqual(expected_ret, ret)
            mock_failed.assert_called_with()

    def test_action_success_passthrough(self):
        """The failed call is correctly passed through"""
        with mock.patch.object(self.action, '_success', autospec=True) as mock_success:
            expected_ret = mock.Mock()
            mock_success.return_value = expected_ret
            ret = self.action.success()
            self.assertEqual(expected_ret, ret)
            mock_success.assert_called_with()

class TestActionTimed(unittest.TestCase):
    """Tests the iterative leaf  node's logic"""

    def setUp(self):
        self.actor = mock.Mock(spec=actor.Actor)

    def test_action_timed__init__(self):
        """Tests that __init__ properly sets up action actor"""
        name = 'node00'
        node = action.Action(name=name, actor=self.actor, timegoal=5)
        self.assertIs(node._actor, self.actor)

    def test_action_timed__init__no_timegoal(self):
        """Not providing an actor results in an exception being raised"""
        with self.assertRaises(oh_behave.MissingArgumentException):
            node = action.ActionTimed(name='asdf', actor=self.actor)

    def test_node_action_timed_execute_loops(self):
        """Tests that the iterative leaf returns success after n executions"""
        execs = 10
        timed = action.ActionTimed(actor=self.actor, name='bing watch netflix', timegoal=execs)
        status = None
        loops = 0
        while status is not oh_behave.ExecuteResult.success:
            status = timed.execute()
            loops += 1
            # Fail if it looks like we are going to loop forever
            self.assertGreater(execs*1.5, loops)
        self.assertEqual(execs, loops)
