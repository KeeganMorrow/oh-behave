"""Module for parsing data files and creating objects from them"""

import json
from oh_behave import behave
from oh_behave import actor
from oh_behave import action

classname_match_table_default = {
    'Actor' : actor.Actor,
    'ActionTimed' : action.ActionTimed,
    'NodeSequence' : behave.NodeSequence,
    'NodeSelector' : behave.NodeSequence,
    'NodeLeafAction' : behave.NodeLeafAction,
    'NodeDecoratorInvert' : behave.NodeDecoratorInvert,
    'NodeDecorator' : behave.NodeDecorator
}


class DataParser:
    """Class used to parse configuration files"""
    def __init__(self, classname_match_table=None):
        if classname_match_table is None:
            self._classname_match_table = classname_match_table_default
        else:
            self._classname_match_table = classname_match_table

        self._actors = []
        self._nodes = []

    def parse_file(self, filepath):
        """Parse a file"""
        pass

    def parse_object_string(self, string):
        """Create an object from a json string"""
        parsed = json.loads(string)
        classname = parsed['type']
        object_class = self._classname_match_table[classname]

        created = object_class(*[], **parsed)
        self._add_object(created, classname)

    def _add_object(self, obj, classname):
        """Add an object to the appropriate list"""
        if classname == 'Actor':
            self._actors.append(obj)
        else:
            self._nodes.append(obj)

