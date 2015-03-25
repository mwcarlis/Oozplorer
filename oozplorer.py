""" Insert docstring here

- Matthew Carlis
- Chris Nguyen
- Shunt Balushian
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
                if not self.alive:
                    return self.location
                while True:
                    ret_v = raw_input('percept=%s; action: x, y?' % percept)
                    try:
                        move = tuple([int(val.strip(' ')) for val in ret_v.split(',')])
                        # Out of boundaries.
                        if move[0] < 0 or move[1] < 0:
                            raise Exception('Continue')
                        if move[0] > 9, or move[1] > 9:
                            raise Exception('Continue')
                    except Exception:
                        print 'Invalid input.  Try: 1, 3   etc'
                        continue
                    break
                return move
        assert callable(program)
        self.program = program

    def is_alive(self):
        return self.alive

    def start(self):
        """ Start the game and loop over the moves etc breaking when
            we've won or lost.
        """
        playing = True
        while playing:
            playing = False

class Pit(Thing):
    """ The pit for this game. Inherit a thing.
    """
    def __init__(self):
        self.state = -1
        self.location = None
        super(Thing,self).__init__()
    def show_state(self):
        print self.state 

class Gold(Thing):
    """ The goal for this game. Inherit a thing.
    """
    def __init__(self):
        self.state = 1
        self.location = None
        super(Thing,self).__init__()
    def show_state(self):
        print self.state 


class Breeze(Thing):
    def __init__(self, location=None):
        if location is not None:
            self.location = location

class Board(XYEnvironment):
    """ The board of the oozplorer game.  Inherit XYEnvironment
    """
    def __init__(self, width=10, height=10):
        """
        """
        super(Board, self).__init__(width, height)
        self.add_walls()

    def thing_classes(self):
        """
        """
        return [Wall, Gold, Pit, Agent]

    def percept(self, agent):
        """ Ride on top of lower things_near, but we don't want to know
        if the Pit is near, we want to know if a breeze is here.
        """
        xloc, yloc = agent.location
        # The agent falls into the darkness.
        if any(self.list_things_at((xloc, yloc), tclass=Pit)):
            agent.alive = False
        diag_vectors = [(1, 1), (-1, 1), (-1, -1), (1, -1)] # unit-vectors
        # Get the relative diagonal locations using unit-vectors.
        diagonals = [(x + xloc, y + yloc) for x, y in diag_vectors]
        near_items = self.things_near((xloc, yloc))
        for item in near_items:
            # Skip the diagonals
            if item.location in diagonals:
                continue
            if isinstance(item, Pit):
                return Breeze(location=(xloc, yloc))
        return None

    def execute_action(self, agent, action):
        if self.is_done():
            return
        agent.bump = False
        xloc, yloc = agent.location
        axloc, ayloc = action
        if abs(axloc - xloc) >= 1 and abs(ayloc - yloc) >= 1:
            print 'Invalid Choice.  You lose your turn dummy.'
            print 'You can only move one square at a time.'
        if abs(axloc - xloc) > 1 or abs(ayloc - yloc) > 1:
            print 'No Diagonal movement more than 1 duh'
            return
        agent.location = action

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
    print 'updating\n'
    ARGS = sys.argv
    #NUMBER = parse_arguments(ARGS)
    #run_game(NUMBER)
    #print NUMBER
    pt = Pit()
    bd = Board()
    ag = Agent(3)
    ag.location = (1, 1)
    pt.location = (2, 2)
    bd.agents.append(ag)
    print bd.agents
    bd.things.append(ag)
    bd.things.append(pt)
    print bd.percept(ag)
    ag.location = (2, 1)
    print bd.percept(ag)
    ag.location = (1, 1)
    print bd.percept(ag)
    print 'INITIAL MAP'
    print '   . . .   '
    print '   . P .   '
    print '   A . .   '
    print 'Move around the Pit and sense him or try to die.'
    bd.run()
