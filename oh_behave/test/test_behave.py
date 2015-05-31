"""Test for behavior module"""
import unittest
import pprint
from unittest import mock
from oh_behave import behave


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
        self.composite = behave.NodeComposite('composite00')

    def test_node_composite__init__(self):
        """Test the composite node's constructor"""
        composite = behave.NodeComposite('composite01')
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
        self.sequence = behave.NodeSequence('sequence00')

    def test_node_sequence__init__(self):
        """Test sequence initialization"""
        self.assertTrue(isinstance(self.sequence.name, str))

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

    def test_node_sequence_execute_empty(self):
        """Sequence exec returns success when called and already empty"""
        result = self.sequence.execute()
        self.assertEqual(result, behave.ExecuteResult.success)

class TestNodeSelector(unittest.TestCase):
    """Tests the selector node's logic"""

    def setUp(self):
        self.selector = behave.NodeSelector('selector00')

    def test_node_selector__init__(self):
        """Test selector initialization"""
        self.assertTrue(isinstance(self.selector.name, str))

    def test_node_selector_execute_repeat(self):
        """selector exec repeats when node returns ready status the first time"""
        node1 = mocknode_builder(behave.ExecuteResult.ready)
        node2 = mocknode_builder(behave.ExecuteResult.success)
        self.selector.addchild(node1)
        self.selector.addchild(node2)
        result = self.selector.execute()
        self.assertEqual(result, behave.ExecuteResult.ready)
        assert_node_calls(node1, 0, 0, 1)
        assert_node_calls(node2, 0, 0, 0)
        result = self.selector.execute()
        self.assertEqual(result, behave.ExecuteResult.ready)
        assert_node_calls(node1, 0, 0, 2)
        assert_node_calls(node2, 0, 0, 0)

    def test_node_selector_execute_child_failure(self):
        """selector moves to next child when current fails"""
        node1 = mocknode_builder(behave.ExecuteResult.failure)
        node2 = mocknode_builder(behave.ExecuteResult.ready)
        self.selector.addchild(node1)
        self.selector.addchild(node2)
        result = self.selector.execute()
        self.assertEqual(result, behave.ExecuteResult.ready)
        assert_node_calls(node1, 0, 1, 1)
        assert_node_calls(node2, 0, 0, 0)
        result = self.selector.execute()
        self.assertEqual(result, behave.ExecuteResult.ready)
        assert_node_calls(node1, 0, 1, 1)
        assert_node_calls(node2, 0, 0, 1)

    def test_node_selector_execute_child_success(self):
        """selector succeeds when current child succeeds"""
        node1 = mocknode_builder(behave.ExecuteResult.success)
        node2 = mocknode_builder(behave.ExecuteResult.ready)
        self.selector.addchild(node1)
        self.selector.addchild(node2)
        result = self.selector.execute()
        self.assertEqual(result, behave.ExecuteResult.success)
        assert_node_calls(node1, 1, 0, 1)
        assert_node_calls(node2, 0, 0, 0)
        result = self.selector.execute()
        self.assertEqual(result, behave.ExecuteResult.success)

        # Note: This test means that success() will be
        # called multiple times if execute is run succesfully
        assert_node_calls(node1, 2, 0, 2)
        assert_node_calls(node2, 0, 0, 0)

    def test_node_selector_execute_empty(self):
        """selector exec returns success when called and already empty"""
        result = self.selector.execute()
        self.assertEqual(result, behave.ExecuteResult.failure)

class TestNodeDecorator(unittest.TestCase):
    """Tests the decorator node base's logic"""
    def setUp(self):
        self.mock_node = mocknode_builder(behave.ExecuteResult.ready)
        self.decorator = behave.NodeDecorator('decorator', self.mock_node)

    def test_node_decorator_execute_success(self):
        """Tests that the decorator passes succesful execution through"""
        self.mock_node.execute.return_value = behave.ExecuteResult.success
        ret = self.decorator.execute()
        self.assertIs(ret, behave.ExecuteResult.success)
        self.mock_node.execute.assert_called_with()

    def test_node_decorator_execute_failure(self):
        """Tests that the decorator passes failed execution through"""
        self.mock_node.execute.return_value = behave.ExecuteResult.failure
        ret = self.decorator.execute()
        self.assertIs(ret, behave.ExecuteResult.failure)
        self.mock_node.execute.assert_called_with()

    def test_node_decorator_execute_ready(self):
        """Tests that the decorator passes ready execution through"""
        self.mock_node.execute.return_value = behave.ExecuteResult.ready
        ret = self.decorator.execute()
        self.assertIs(ret, behave.ExecuteResult.ready)
        self.mock_node.execute.assert_called_with()

    def test_node_decorator_success_passthrough(self):
        """Tests that the decorator passes success call through"""
        self.decorator.success()
        self.mock_node.success.assert_called_with()

    def test_node_decorator_failed_passthrough(self):
        """Tests that the decorator passes failed call through"""
        self.decorator.failed()
        self.mock_node.failed.assert_called_with()

class TestNodeDecoratorInvert(unittest.TestCase):
    """Tests the decorator node base's logic"""
    def setUp(self):
        self.mock_node = mocknode_builder(behave.ExecuteResult.ready)
        self.decorator = behave.NodeDecoratorInvert('invert', self.mock_node)

    def test_node_decorator_invert_execute_success(self):
        """Tests that the decorator makes success into failure"""
        self.mock_node.execute.return_value = behave.ExecuteResult.success
        ret = self.decorator.execute()
        self.assertIs(ret, behave.ExecuteResult.failure)
        self.mock_node.execute.assert_called_with()

    def test_node_decorator_invert_execute_failure(self):
        """Tests that the decorator makes failure into success"""
        self.mock_node.execute.return_value = behave.ExecuteResult.failure
        ret = self.decorator.execute()
        self.assertIs(ret, behave.ExecuteResult.success)
        self.mock_node.execute.assert_called_with()

    def test_node_decorator_invert_execute_ready(self):
        """Tests that the decorator passes ready execution state through"""
        self.mock_node.execute.return_value = behave.ExecuteResult.ready
        ret = self.decorator.execute()
        self.assertIs(ret, behave.ExecuteResult.ready)
        self.mock_node.execute.assert_called_with()

class TestNodeLeafIterative(unittest.TestCase):
    """Tests the iterative leaf  node's logic"""

    def setUp(self):
        pass

    def test_node_leaf_iterative_execute_loops(self):
        """Tests that the iterative leaf returns success after n executions"""
        execs = 10
        leaf = behave.NodeLeafIterative('leaf_iterate00', execs)
        status = None
        loops = 0
        while status is not behave.ExecuteResult.success:
            status = leaf.execute()
            loops += 1
            # Fail if it looks like we are going to loop forever
            self.assertGreater(execs*1.5, loops)
        self.assertEqual(execs, loops)
