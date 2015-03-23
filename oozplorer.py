""" Insert docstring here

- Matthew Carlis
- Chris Nguyen
- Shunt Balushian
-Chris branch
"""
import sys
import random
from agents import Thing, XYEnvironment, Wall
from logic import KB, FolKB

class OzKB(KB):
    """ I don't know if we need this or if we can inherit something more 
            evolved from the logic.py classes.
        Inherit a KB.
    """
    def __init__(self, sentence=None):
        self.sentence = sentence
    def tell(self, sentence):
        """ Implement parent->KB.tell()
        """
        pass
    def ask_generator(self, query):
        """ Implement parent->KB.ask_generator()
        """
        pass
    def retract(self, sentence):
        """ Implement parent->KB.retract()
        """
        pass

class Agent(Thing):
    """ The player that we want to win.  Or lose depending on how evil you
    are. Inherit a thing.
    """

    def __init__(self, some_number, program=None):
        """
        """
        self.alive = True
        self.some_number = some_number
        self.location = None
        if program is None:
            def program(percept):
                return raw_input('percept=%s; action?' % percept)
        assert callable(program)
        self.program = program

    def start(self):
        """ Start the game and loop over the moves etc breaking when
            we've won or lost.
        """
        playing = True
        while playing:
            playing = False

class OzPit(Thing):
    """ The pit for this game. Inherit a thing.
    """
    def __init__(self):
        self.location = None


class OzPit(Thing):
    """ The pit for this game. Inherit a thing.
    """
    def __init__(self):
        self.state = -1
        super(Thing,self).__init__()
    def show_state(self):
        print self.state 

class OzGold(Thing):
    """ The goal for this game. Inherit a thing.
    """
    def __init__(self):
        self.location = None

class Board(XYEnvironment):
    """ The board of the oozplorer game.  Inherit XYEnvironment
    """
    def __init__(self, width=10, height=10):
        """
        """
        super(Board, self).__init__(width, height)
        #self.width, self.height = width, height
        self.add_walls()

    def thing_classes(self):
        """
        """
        return [Wall, Gold, Pit, Agent]

    def default_location(self, thing):
        """
        """
        if isinstance(thing, Agent):
            return (1, 1)
        else:
            get_rand = lambda arg: random.choice(range(1, arg))
            return (get_rand(self.width), get_rand(self.height))

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this."""
        #if not isinstance(thing, Thing):
        #    thing = Agent(thing)
        assert thing not in self.things, "Don't add the same thing twice"
        thing.location = location or self.default_location(thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)
        thing.holding = []
        thing.held = None
        for obs in self.observers:
            obs.thing_added(thing)

    def move(self, pair):
        """
        Args:
            pair (tuple): (x, y) coordinates of the matrix.
        Returns:
            (tuple): (sensor, state)
                sensor - True if a breeze in that square else false.
                state - If oozplorer loses moving into (x, y) square -1, 
                    if it wins 1, otherwise 0.
        Actions:
            If the square didn't have an oozplayer and it was a legal move 
                then the square is not occupied by oozplorer.
        Throws:
            IndexError (Exception): If pair (x, y) is not in the map.
        """
        # super(OzBoard, self).move_to(thing, destination) # From super
        pass

def run_game(number):
    """
    Args:
        number (int): The integer 
    """
    pass


def parse_arguments(arguments):
    """ 
    Args: 
        arguments (list): sys.argv object.
    Returns:
        number (int): The integer command line argument.
    """
    def bail_out():
        print 'Invalid Command line arguments.  Use Integers only.'
        #sys.exit(1)
    try:
        number = int(arguments[1])
    except IndexError:
        bail_out()
    except ValueError:
        bail_out()
    return number


if __name__ == '__main__':
    ARGS = sys.argv
    NUMBER = parse_arguments(ARGS)
    run_game(NUMBER)
    print NUMBER
