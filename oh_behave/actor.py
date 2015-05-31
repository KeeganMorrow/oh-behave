"""Actor module"""

class Actor:
    """Represents a character in the world"""
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self._rootnode = kwargs['rootnode']

    def execute(self):
        """
        Run the actor's root behavior tree node
        """
        print("Actor {0} running root node".format(self.name))
        if self._rootnode:
            ret = self._rootnode.execute()
            print("Actor {0} returns status {0}".format(ret))
        else:
            ret = None
            print("Actor {0} does not have root node".format(self.name))
        return ret

    def set_rootnode(self, node):
        """
        Set the actor's root behavior tree node
        """
        self._rootnode = node

