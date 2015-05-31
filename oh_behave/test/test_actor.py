"""Unit tests for actory module"""

import unittest
from unittest import mock

from oh_behave import actor
from oh_behave import behave
import oh_behave.test.test_behave

class TestActor(unittest.TestCase):
    """Tests the actor class"""
    def setUp(self):
        from oh_behave import behave
        self.mock_rootnode = oh_behave.test.test_behave.mocknode_builder(
                behave.ExecuteResult.ready)
        self.name = "Billy Bob"
        self.actor = actor.Actor(self.name, self.mock_rootnode)

    def test__init__(self):
        """__init__ method sets up required resources"""
        a = actor.Actor(self.name, self.mock_rootnode)
        self.assertIs(a.name, self.name)
        self.assertIs(a._rootnode, self.mock_rootnode)

    def test_execute_no_rootnode(self):
        """execute does not attempt to run if rootnode is None"""
        self.actor._rootnode = None
        # If it tries to run an exception will be thrown
        self.actor.execute()

    def test_execute_rootnode_failure(self):
        """execute returns failure if root node execution returns failure"""
        self.actor._rootnode.execute.return_value = behave.ExecuteResult.failure
        self.assertEqual(behave.ExecuteResult.failure, self.actor.execute())

    def test_execute_rootnode_success(self):
        """execute returns success if root node execution returns success"""
        self.actor._rootnode.execute.return_value = behave.ExecuteResult.success
        self.assertEqual(behave.ExecuteResult.success, self.actor.execute())

    def test_execute_rootnode_ready(self):
        """execute returns ready if root node execution returns ready"""
        self.actor._rootnode.execute.return_value = behave.ExecuteResult.ready
        self.assertEqual(behave.ExecuteResult.ready, self.actor.execute())

    def test_set_rootnode_changes_node(self):
        """set_rootnode changes actor's rootnode"""
        old_node = self.actor._rootnode
        self.assertIs(self.actor._rootnode, old_node)
        new_node = mock.Mock()
        self.actor.set_rootnode(new_node)
        self.assertIs(self.actor._rootnode, new_node)

