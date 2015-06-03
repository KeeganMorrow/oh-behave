"""Actor module"""
import logging
import oh_behave

logger = logging.getLogger(__name__)

class Actor:
    """Represents a character in the world"""
    def __init__(self, *args, **kwargs):
        try:
            self.name = kwargs['name']
        except KeyError as e:
            raise oh_behave.MissingArgumentException(self, self.__init__, str(e))
        try:
            self._rootnode = kwargs['rootnode']
        except KeyError:
            self._rootnode = None
        logging.info('Constructed actor name "%s"', self.name)


    def execute(self):
        """
        Run the actor's root behavior tree node
        """
        logger.info('Actor "%s" running root node',self.name)
        if self._rootnode:
            ret = self._rootnode.execute()
            logger.info('Actor "%s" returns status "%s"', self.name, ret)
        else:
            ret = None
            logger.warning('Actor "%s" does not have root node', self.name)
        return ret

    def set_rootnode(self, node):
        """
        Set the actor's root behavior tree node
        """
        self._rootnode = node

