"""Module for parsing data files and creating objects from them"""

import json
import oh_behave
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

class MissingFieldException(BaseException):
    pass

class ObjectEntry:
    """Represents an object and linking data"""
    def __init__(self, values):
        self.values = values
        self.classtype = values.get('type', None)
        self.ident = values.get('id', None)
        self.rootnode = values.get('rootnode', None)
        self.childnodes = values.get('childnodes', [])

        if self.classtype is None:
            raise MissingFieldException('Missing required field "type"')
        if self.ident is None:
            raise MissingFieldException('Missing required field "id"')

class DataParser:
    """Class used to parse configuration files"""
    def __init__(self, classname_match_table=None):
        if classname_match_table is None:
            self._classname_match_table = classname_match_table_default
        else:
            self._classname_match_table = classname_match_table

        self._entries = []

    def parse_file(self, filepath):
        """Parse a file"""
        pass

    def _parse_object_string(self, string):
        """Create an object from a json string"""
        parsed = json.loads(string)

        self._entries.append(ObjectEntry(parsed))

    def link_objects(self):
        """Link all parsed objects into the determined hierarchy"""
        pass

    def _add_object(self, obj, classname):
        """Add an object to the appropriate list"""
        # entry = ObjectEntry(
        self._entries.append(obj)

