"""Unit tests for actions module"""

import unittest
from unittest import mock
import oh_behave
from oh_behave import actor
from oh_behave import action

class TestAction(unittest.TestCase):
    def setUp(self):
        self.actor = mock.Mock(spec=actor.Actor)
        self.action= action.Action(self.actor)

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

    def test_node_action_timed_execute_loops(self):
        """Tests that the iterative leaf returns success after n executions"""
        execs = 10
        timed = action.ActionTimed(self.actor, execs)
        status = None
        loops = 0
        while status is not oh_behave.ExecuteResult.success:
            status = timed.execute()
            loops += 1
            # Fail if it looks like we are going to loop forever
            self.assertGreater(execs*1.5, loops)
        self.assertEqual(execs, loops)
