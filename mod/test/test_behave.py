"""Test for behavior module"""
import unittest
import pprint
from unittest import mock
from mod import behave


def mocknode_builder(execstatus):
    mock_node = mock.Mock(spec=behave.Node)
    mock_node.execute.return_value = execstatus
    return mock_node

def assert_node_calls(mock_node, succ_count, fail_count, exec_count):
    """
    Helper to test out a mock node's call counts
    """
    failmsg = "Node call count mismatch: "
    failureformat = "{0} call count expected: {1} != actual: {2}"
    failed = False

    # TODO: Reduce the obvious code repetition
    lhs = succ_count
    rhs = mock_node.success.call_count
    if lhs != rhs:
        failmsg += failureformat.format("success()", lhs, rhs)
        failed = failed or True

    lhs = fail_count
    rhs = mock_node.failed.call_count
    if lhs != rhs:
        failmsg += failureformat.format("failed()", lhs, rhs)
        failed = failed or True

    lhs = exec_count
    rhs = mock_node.execute.call_count
    if lhs != rhs:
        failmsg += failureformat.format("execute()", lhs, rhs)
        failed = failed or True

    if failed:
        raise AssertionError(failmsg)

class TestNodeComposite(unittest.TestCase):
    """Tests the composite node's logic"""
    def setUp(self):
        self.composite = behave.NodeComposite()

    def test_node_composite__init__(self):
        """Test the composite node's constructor"""
        composite = behave.NodeComposite()
        self.assertEqual(composite._children, [])

    def test_node_composite_addchild(self):
        """Tests adding a child to the sequence"""
        node = mocknode_builder(behave.ExecuteResult.ready)
        self.assertEqual(self.composite._children, [])
        self.composite.addchild(node)
        self.assertIn(node, self.composite._children)

class TestNodeSequence(unittest.TestCase):
    """Tests the sequence node's logic"""

    def setUp(self):
        self.sequence = behave.NodeSequence()

    def test_node_sequence_execute_repeat(self):
        """Sequence exec repeats when node returns ready status the first time"""
        node1 = mocknode_builder(behave.ExecuteResult.ready)
        node2 = mocknode_builder(behave.ExecuteResult.success)
        self.sequence.addchild(node1)
        self.sequence.addchild(node2)
        result = self.sequence.execute()
        self.assertEqual(result, behave.ExecuteResult.ready)
        assert_node_calls(node1, 0, 0, 1)
        assert_node_calls(node2, 0, 0, 0)
        result = self.sequence.execute()
        self.assertEqual(result, behave.ExecuteResult.ready)
        assert_node_calls(node1, 0, 0, 2)
        assert_node_calls(node2, 0, 0, 0)

    def test_node_sequence_execute_failure(self):
        """Sequence exec returns failure on child failure"""
        node1 = mocknode_builder(behave.ExecuteResult.failure)
        node2 = mocknode_builder(behave.ExecuteResult.success)
        self.sequence.addchild(node1)
        self.sequence.addchild(node2)
        result = self.sequence.execute()
        assert_node_calls(node1, 0, 1, 1)
        assert_node_calls(node2, 0, 0, 0)
        self.assertEqual(result, behave.ExecuteResult.failure)

    def test_node_sequence_execute_succeed(self):
        """Sequence exec progresses and calls success() on child success"""
        node1 = mocknode_builder(behave.ExecuteResult.success)
        node2 = mocknode_builder(behave.ExecuteResult.success)
        self.sequence.addchild(node1)
        self.sequence.addchild(node2)
        result = self.sequence.execute()
        assert_node_calls(node1, 1, 0, 1)
        assert_node_calls(node2, 0, 0, 0)
        self.assertEqual(result, behave.ExecuteResult.ready)
        result = self.sequence.execute()
        assert_node_calls(node1, 1, 0, 1)
        assert_node_calls(node2, 1, 0, 1)
        self.assertEqual(result, behave.ExecuteResult.success)


