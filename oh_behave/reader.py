"""Module for parsing data files and creating objects from them"""

import json
import oh_behave
import logging
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

logger = logging.getLogger(__name__)

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
        logger.info("Built Entry: type:\"%s\" id:\"%s\"", self.classtype, self.ident)
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

    def build_objects(self):
        """Build all parsed objects into the determined hierarchy"""
        #TODO: Future optimization: Filter out objects that don't need linking in first pass
        objects = {}
        for entry in self._entries:
            logger.info("Building entry id:'%s' class '%s'", entry.ident, entry.classtype)
            baseclass = self._classname_match_table[entry.classtype]
            obj = baseclass([], **entry.values)
            objects[entry.ident] = obj
        for entry in self._entries:
            logger.info("Linking entry id:'%s' class '%s'", entry.ident, entry.classtype)
            if entry.classtype == 'Actor':
                if entry.rootnode:
                    logger.info("Linking actor id:'%s' to rootnode id '%s'", entry.ident, entry.rootnode)
                    objects[entry.ident].set_rootnode(objects[entry.rootnode])
            elif entry.classtype.startswith('Node'):
                for child in entry.childnodes:
                    logger.info("Linking node id:'%s' to childnode id '%s'", entry.ident, child)
                    objects[entry.ident].add_child(objects[child])

        return objects

    def _add_object(self, obj, classname):
        """Add an object to the appropriate list"""
        # entry = ObjectEntry(
        self._entries.append(obj)
        json.tests

