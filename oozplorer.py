""" Insert docstring here

- Matthew Carlis
- Chris Nguyen
- Shunt Balushian
"""
import sys
import random
from collections import defaultdict
from agents import Thing, XYEnvironment, Wall
from utils import print_table
from logic import KB, FolKB

AGENT = 'A{}{}'
GOLD = 'G{}{}'
PIT = 'P{}{}'
BREEZE = 'B{}{}'

def is_iterable(thing):
    try: iter(thing)
    except TypeError: return False
    else: return True

def sentence_builder(some_val):
    """ A simple decorator to create boolean expressions.
    """
    rv_s = ''
    if isinstance(some_val, str): return some_val
    for item in some_val:
        if is_iterable(item):
            rv_s += sentence_builder(item)
    return rv_s

def _valid_neighbors(location, some_num):
    """ Return a list of the valid neighboring coordinates.

    Args:
        location (tuple): of (x, y) cordinates.
        some_num (int): The game some_num.
    """
    xloc, yloc = location
    vector = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    ret_v = []
    for vect in vector:
        xpos = xloc + vect[0]
        ypos = yloc + vect[1]
        if xpos <= 0 or ypos <= 0:
            continue
        if xpos > some_num or ypos > some_num:
            continue
        ret_v.append((xpos, ypos))
    return ret_v

def iff_format(location, some_num, sentence, loop=False):
    """
    Args:
        location (tuple): of (x, y) cordinates.
        some_num (int): The game some_num.
        sentence (str): The string to apply formatting
    """
    positions = _valid_neighbors(location, some_num)
    repeat = len(positions) - 1
    xloc, yloc = location
    loc_master = lambda statement: statement.format(xloc, yloc)
    if loop:
        rv = [sentence[0].format(_x[0], _x[1]) for _x in positions[:-1]]
        rv.append(sentence[1].format(positions[-1][0], positions[-1][1]))
        return rv
    return [loc_master(sentence)]

def pit_iff(location, some_num):
    """
    Args:
        location (tuple): of (x, y) cordinates.
        some_num (int): The game some_num.
    """
    # A Pit iff all his neighbors have breezes
    #PIT_IFF = 'P{}{} <=> (B{}{} & B{}{} & B{}{} & B{}{})'
    rv = iff_format(location, some_num, 'P{}{} <=> (')
    rv.extend(iff_format(location, some_num, ['B{}{} & ', 'B{}{})'], loop=True))
    return sentence_builder(rv)

def not_pit_iff(location, some_num):
    # No pit iff one or more neighbors has no breeze.
    #N_PIT_IFF = '~P{}{} <=> (~B{}{} | ~B{}{} | ~B{}{} | ~B{}{})'
    rv = iff_format(location, some_num, '~P{}{} <=> (')
    rv.extend(iff_format(location, some_num, ['~B{}{} | ', '~B{}{})'], loop=True))
    return sentence_builder(rv)

def breeze_iff(location, some_num):
    # A breeze iff one or more neighbors has a pit
    #BREEZE_IFF = 'B{}{} <=> (P{}{} | P{}{} | P{}{} | P{}{})'
    rv = iff_format(location, some_num, 'B{}{} <=> (')
    rv.extend(iff_format(location, some_num, ['P{}{} | ', 'P{}{})'], loop=True))
    return sentence_builder(rv)

def not_breeze_iff(location, some_num):
    # No breeze iff none of the neighbors have pits.
    #N_BREEZE_IFF = '~B{}{} <=> (~P{}{} & ~P{}{} & ~P{}{} & ~P{}{})'
    rv = iff_format(location, some_num, '~B{}{} <=> (')
    rv.extend(iff_format(location, some_num, ['~P{}{} & ', '~P{}{})'], loop=True))
    return sentence_builder(rv)

def which_position(location, some_number, logic_gen):
    """ Determine if location is a corner, edge or has 4 neighbors.

    Args:
        - location (tuple): (x, y) position of the map.
        - some_number (int): The largest x or y value which is a valid move.
    """
    xpos, ypos = location
    # Is this location in a corner?
    upper_r = xpos == 4 and ypos == 4
    lower_l = xpos == 1 and ypos == 1 
    others = (1 in location and some_number in location)
    if upper_r or lower_l or others:
        return 2 # CORNER. 2- Neighbors.
    # Is this location a non-edge (by priority) corner?
    elif (1 in location or some_number in location):
        return 3 # EDGE. 3- Neighbors.
    # This is not a corner or an edge.
    else:
        return 4 # Else 4- Neighbors.

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

def KnowledgeBasedReflexAgent(rules, update_state, dimens):
    """
    """
    knowledge = defaultdict(list)
    for xloc in range(dimens):
        for yloc in range(dimens):
            knowledge[xloc][yloc] = []
    def program(percept):
        action = None
        return action
    return program

class Agent(Thing):
    """ The player that we want to win.  Or lose depending on how evil you
    are. Inherit a thing.
    """
    def __init__(self, some_number, program=None):
        """
        """
        self.alive = True
        self.winner = False
        self.some_number = some_number
        self.location = None
        if program is None:
            def program(percept):
                program.dimens = some_number
                if not self.alive or self.winner:
                    return self.location
                while True:
                    ret_v = raw_input('percept=%s; action: x, y? ' % percept)
                    try:
                        move = tuple([int(val.strip(' ')) for val in ret_v.split(',')])
                        # Out of boundaries.
                        if move[0] <= 0 or move[1] <= 0:
                            raise Exception('Continue')
                        if move[0] > some_number or move[1] > some_number:
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
    def is_winner(self):
        return self.winner

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
    def __init__(self, some_number):
        """
        """
        # some_number + 2 since the map is surrounded by walls.  2 extra cols/rows
        super(Board, self).__init__(some_number+2, some_number+2)
        self.some_number = some_number
        self.add_walls()
        self.remove_duplicate_walls()
        self.matrix = None
        self.frontier = None
        self.make_board()
        self.print_board()

    def print_board(self):
        if self.matrix is None:
           self.matrix = get_static_board_layout(self.things, self.width, self.height) 
        agent = self.agents[0]
        xloc, yloc = agent.location
        place_hold = self.matrix[self.height - yloc - 1][xloc]
        self.matrix[self.height - yloc - 1][xloc] = agent
        print_table(self.matrix)
        self.matrix[self.height - yloc - 1][xloc] = place_hold
        print ''

    def remove_duplicate_walls(self):
        """ The stupid self.add_walls() function duplicates some walls.
        Whoever wrote it must be super lazy.
        """
        wall_map = {}
        duplicates = []
        for cnt, thing in enumerate(self.things):
            if isinstance(thing, Wall):
                if not wall_map.has_key(thing.location):
                    wall_map[thing.location] = True
                else:
                    duplicates.append(cnt)
        for cnt, item in enumerate(duplicates):
            self.things.pop(item - cnt)


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
        if any(self.list_things_at((xloc, yloc), tclass=Gold)):
            agent.winner = True
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

    def is_done(self):
        """ We're done if the Agent is dead or if he's a winner.  Dead is
        higher priority than Winner.
        """
        dead = not any(agent.is_alive() for agent in self.agents)
        winner = any(agent.is_winner() for agent in self.agents)
        def winner_msg(msg):
            try: # This is a hack to avoid printing the winning message twice.
                if not self.printed_message:
                    pass # We already printed.
            except AttributeError: # Throw exception the first time.
                self.printed_message = True
                print msg
        if dead:
            winner_msg('Your Agent Died')
            return dead
        elif winner:
            winner_msg('Your Agent Wins')
            return winner
        return False

    def execute_action(self, agent, action):
        """
        """
        if self.is_done():
            return
        agent.bump = False
        xloc, yloc = agent.location
        axloc, ayloc = action
        if abs(axloc - xloc) >= 1 and abs(ayloc - yloc) >= 1:
            print 'Invalid Choice.  You lose your turn dummy.'
            print 'You can only move one square at a time.'
            return
        if abs(axloc - xloc) > 1 or abs(ayloc - yloc) > 1:
            print 'No Diagonal movement more than 1 duh'
            return
        agent.location = action
        self.print_board()

    def default_location(self, thing):
        """
        """
        if isinstance(thing, Agent):
            return (1, 1)
        else:
            get_rand = lambda arg: random.choice(range(1, arg-1))
            while True:
                xloc, yloc = (get_rand(self.width), get_rand(self.height))
                if (1, 1) == (xloc, yloc):
                    continue
                break
            return (xloc, yloc)

    def make_board(self):
        generate = lambda: random.randint(1, 10) in [1, 2]
        some_number = self.some_number
        agent = Agent(some_number)
        gold = Gold()
        self.add_thing(agent, None)
        self.agents.append(agent)
        self.add_thing(gold, None)
        row = 1
        for i in range(1, some_number + 1):
            col = 1
            for j in range(1, some_number + 1):
                if generate() and (row, col) != gold.location:
                    if (row, col) != gold.location and (row, col) != (1, 1):
                        pt = Pit()
                        pt.location = (row, col)
                        self.things.append(pt)
                col = col + 1
            row+=1

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


def satisfy(expr, true_var):
    """ Recursively remove true_var from expr.

    Args:
        - expr (Expr): An expression which trying to simplify.
        - true_var (Expr): A true variable to remove from the expression.

    Returns:
        - simplifed (Expr): The Expr now has no instances of true_var

    EXAMPLE:
    statement = expr('B01 <=> (P00 | P11 | P02) <=> (P00 | P11)')
    satisfy(statement, expr('P00'))
    statement becomes -> Expr('((B01 <=> (P11 | P02)) <=> P11)')
    """
    if len(expr.args) == 0:
        if expr.__repr__() == true_var.__repr__():
            return True
        else:
            return False
    cnt = 0
    while True:
        if cnt >= len(expr.args):
            break
        arg = expr.args[cnt]
        changed = satisfy(arg, true_var)
        if isinstance(changed, Expr):
            expr.args[cnt] = changed
        elif changed is True:
            expr.args.pop(cnt)
            expr = expr.args[0]
        cnt += 1
    return expr

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


def get_static_board_layout(things, width, height):
    obj_map = convert_to_dict(things)
    matrix = []
    for yloc in xrange(height):
        row = []
        for xloc in xrange(width):
            if obj_map.has_key((xloc, yloc)):
                row.append(obj_map[(xloc, yloc)])
            else:
                row.append('<---->')
        matrix.insert(0, row)
    return matrix

def convert_to_dict(things):
    rv_d = {}
    for this_thing in things:
        if isinstance(this_thing, Pit):
            xloc, yloc = this_thing.location
            rv_d[xloc, yloc] = this_thing
        if isinstance(this_thing, Gold):
            xloc, yloc = this_thing.location
            rv_d[xloc, yloc] = this_thing
        if isinstance(this_thing, Wall):
            xloc, yloc = this_thing.location
            rv_d[xloc, yloc] = this_thing
    return rv_d


if __name__ == '__main__':
    print 'updating\n'
    ARGS = sys.argv
    b = Board(3)
    b.run()
""" 
    pt = Pit()
    bd = Board()
    ag = Agent(3)
    ag.location = (1, 1)
    pt.location = (2, 2)
    bd.agents.append(ag)
    print bd.agents
    bd.things.append(ag)
    bd.things.append(pt)
    print len(bd.things)
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
"""
