import unittest
import json
import pprint
from unittest import mock

from oh_behave import reader

test_string ='{\n' \
'    "type": "Actor",\n' \
'    "id": "actor_01",\n' \
'    "name": "Billy Bob",\n' \
'    "rootnode": [\n' \
'        {\n' \
'            "type": "NodeSequence",\n' \
'            "id": "sequence_01",\n' \
'            "children": [\n' \
'                {\n' \
'                    "type": "NodeLeafIterative",\n' \
'                    "id": "sequence_01",\n' \
'                    "execs": 5\n' \
'                },\n' \
'                {\n' \
'                    "type": "NodeLeafIterative",\n' \
'                    "id": "sequence_02",\n' \
'                    "execs": 5\n' \
'                }\n' \
'            ]\n' \
'        }\n' \
'    ]\n' \
'}'

def mock_classname_match_table():
    mock_table = {}
    for name, baseclass in reader.classname_match_table_default.items():
        mock_table[name] = mock.Mock(spec=baseclass)
    return mock_table

class TestDataParser(unittest.TestCase):
    """Tests data parser class"""

    def setUp(self):
        self.table = mock_classname_match_table()
        self.parser = reader.DataParser(classname_match_table=self.table)

    def test_parse_object_string_actor(self):
        """Parse simple json representation of actor and add it to correct list"""
        input_string = '{\n' \
            '        "type": "Actor",\n' \
            '        "id": "actor_01",\n' \
            '        "name": "Billy Bob"\n' \
            '}'
        self.parser.parse_object_string(input_string)
        mock_base = self.table['Actor']
        self.assertEqual(1, self.table['Actor'].call_count)
        mock_actor = self.parser._actors[0]
        mock_base.assert_called_with(type='Actor', id='actor_01', name='Billy Bob')

    def test_parse_object_string_node(self):
        """Parse simple json representation of node and add it to correct list"""
        input_string = '{\n' \
            '        "type": "NodeSelector",\n' \
            '        "name": "node1"\n' \
            '}'
        self.parser.parse_object_string(input_string)
        mock_base = self.table['NodeSelector']
        self.assertEqual(1, self.table['NodeSelector'].call_count)
        mock_node = self.parser._nodes[0]
        mock_base.assert_called_with(type='NodeSelector', name='node1')
