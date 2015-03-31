""" Insert docstring here

- Matthew Carlis
- Chris Nguyen
- Shunt Balushian
-Chris branch
"""
import sys
import random
from agents import Thing, XYEnvironment, Wall

from logic import KB, FolKB,PropKB,expr,dpll_satisfiable
from logic import *

from utils import print_table


from logic import KB, FolKB
from logic import *

AGENT = 'A{}{}'
GOLD = 'G{}{}'
PIT = 'P{}{}'
BREEZE = 'B{}{}'
=======
from logic import dpll_satisfiable, expr


def is_iterable(thing):
    """
        Args: thing (any):
    """
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

def _iff_format(location, some_num, sentence, loop=False):
    """
    Args:
        location (tuple): of (x, y) cordinates.
        some_num (int): The game some_num.
        sentence (str): The string to apply formatting
    """
    positions = _valid_neighbors(location, some_num)
    xloc, yloc = location
    loc_master = lambda statement: statement.format(xloc, yloc)
    if loop:
        ret_v = [sentence[0].format(_x[0], _x[1]) for _x in positions[:-1]]
        ret_v.append(sentence[1].format(positions[-1][0], positions[-1][1]))
        return ret_v
    return [loc_master(sentence)]

def pit_iff(location, some_num):
    """Args:
        location (tuple): of (x, y) cordinates.
        some_num (int): The game some_num.
    """
    # A Pit iff all his neighbors have breezes
    #PIT_IFF = 'P{}{} <=> (B{}{} & B{}{} & B{}{} & B{}{})'
    ret_v = _iff_format(location, some_num, 'P{}{} <=> (')
    ret_v.extend(_iff_format(location, some_num, ['B{}{} & ', 'B{}{})'], loop=True))
    return sentence_builder(ret_v)
def not_pit_iff(location, some_num):
    """
    Args: location (tuple), some_num (int)
    """
    # No pit iff one or more neighbors has no breeze.
    #N_PIT_IFF = '~P{}{} <=> (~B{}{} | ~B{}{} | ~B{}{} | ~B{}{})'
    ret_v = _iff_format(location, some_num, '~P{}{} <=> (')
    ret_v.extend(_iff_format(location, some_num, ['~B{}{} | ', '~B{}{})'], loop=True))
    return sentence_builder(ret_v)
def breeze_iff(location, some_num):
    """
    Args: location (tuple), some_num (int)
    """
    # A breeze iff one or more neighbors has a pit
    #BREEZE_IFF = 'B{}{} <=> (P{}{} | P{}{} | P{}{} | P{}{})'
    ret_v = _iff_format(location, some_num, 'B{}{} <=> (')
    ret_v.extend(_iff_format(location, some_num, ['P{}{} | ', 'P{}{})'], loop=True))
    return sentence_builder(ret_v)
def not_breeze_iff(location, some_num):
    """
    Args: location (tuple), some_num (int)
    """
    # No breeze iff none of the neighbors have pits.
    #N_BREEZE_IFF = '~B{}{} <=> (~P{}{} & ~P{}{} & ~P{}{} & ~P{}{})'
    ret_v = _iff_format(location, some_num, '~B{}{} <=> (')
    ret_v.extend(_iff_format(location, some_num, ['~P{}{} & ', '~P{}{})'], loop=True))
    return sentence_builder(ret_v)

def which_position(location, some_number):
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
    elif 1 in location or some_number in location:
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

def get_stdin_agent(reference):
    """ A standard input based agent.
    Args:
        reference (Board): This is the reference to the board object
            for which you will be using the stdin_agent().  Often this
            would be the 'self' pointer inside of a class.
    """
    self = reference
    def stdin_agent(percept):
        """ A stdin agent.
        """
        if not self.alive or self.winner:
            return self.location
        while True:
            ret_v = raw_input('percept=%s; action: x, y? ' % percept)
            try:
                move = tuple([int(val.strip(' ')) for val in ret_v.split(',')])
                # Out of boundaries.
                if move[0] <= 0 or move[1] <= 0:
                    raise Exception('Continue')
                if move[0] > self.some_number or move[1] > self.some_number:
                    raise Exception('Continue')
            except Exception:
                print 'Invalid input.  Try: 1, 3   etc'
                continue
            break
        return move
    return stdin_agent

def tell_kb(percept, location, oz_kb):
    """ Tell the kb stuff
    """
    xloc, yloc = location
    if isinstance(percept, Breeze):
        oz_kb['B{}{}'.format(xloc, yloc)] = True
    else:
        oz_kb['B{}{}'.format(xloc, yloc)] = False
    oz_kb['P{}{}'.format(xloc, yloc)] = False

def ask_kb(percept, move, agent):
    """ Ask the kb stuff
    """
    oz_kb = agent.oz_kb
    sentence = pit_iff(move, agent.some_number)
    satisfy_dpll = dpll_satisfiable(expr(sentence))
    isin_kb = lambda item_s: oz_kb.has_key(item_s)
    contradicts_kb = lambda item_s, obj: oz_kb[item_s] != satisfy_dpll[obj]
    for key in satisfy_dpll.keys():
        var = key.__repr__()
        if isin_kb(var) and contradicts_kb(var, key):
            return True
    return False

def Oozeplorer_Percept(reference):
    """ A standard input based agent.
    Args:
        reference (Agent): This is the reference to the board object
            for which you will be using the stdin_agent().  Often this
            would be the 'self' pointer inside of a class.
    """
    self = reference
    self.our_frontier = list()
    self.unsure_moves = list() # Popped moves we didn't want.
    self.ignore_moves = list()
    def knowledge_based_program(percept):
        """ The agent program
        """
        if not self.alive or self.winner:
            return self.location
        # Telling the Dict

        print frontier
        tell_kb(percept, self.location, oz_kb)

        tell_kb(percept, self.location, self.oz_kb)

        local_frontier = _valid_neighbors(self.location, self.some_number)
        random.shuffle(local_frontier)
        local_frontier.extend(self.our_frontier)
        n_count = 0
        for _x in range(len(local_frontier)):
            # Update the random moves.
            move = local_frontier[n_count]
            if move in self.unsure_moves:
                self.unsure_moves.remove(move)
            # Check if we've been there
            if self.explored.has_key(move) and self.explored[move]:
                local_frontier.pop(n_count) # remove this node
                continue
            # Check for Validity.
            valid_move = ask_kb(percept, move, self)
            if valid_move:
                move = local_frontier.pop(n_count)
                self.our_frontier = local_frontier
                self.explored[move] = True
                return move
            else:
                _nmove = local_frontier.pop(n_count)
                self.unsure_moves.append(_nmove)
                continue
        move = random.choice(self.unsure_moves)
        self.explored[move] = True
        self.unsure_moves.remove(move)
        return move
    return knowledge_based_program

class Agent(Thing):
    """ The player that we want to win.  Or lose depending on how evil you
    are. Inherit a thing.
    """
    def __init__(self, some_number, program=None):
        self.some_number = some_number
        self.performance = 0
        self.alive = True
        self.winner = False
        self.oz_kb = {}
        self.explored = {} # The set of explored states.
        if program is None:
            program = get_stdin_agent(self)
        assert callable(program)
        self.program = program
        self.location = None

    def is_alive(self):
        """Return true if alive"""
        return self.alive
    def is_winner(self):
        """Return true if we found gold"""
        return self.winner

    def init_agent(self, location):
        """ Initialize the agent"""
        if self.location is None:
            self.location = location
            self.explored[self.location] = True
            return True
        return False

    def start(self):
        """ Start the game and loop over the moves etc breaking when
            we've won or lost.
        """
        playing = True
        while playing:
            if not self.is_alive(): return
            if self.is_winner(): return


class Pit(Thing):
    """ The pit for this game. Inherit a thing.
    """
    def __init__(self):
        self.state = -1
        self.location = None
        super(Thing, self).__init__()
    def show_state(self):
        print self.state

class Gold(Thing):
    """ The goal for this game. Inherit a thing.
    """
    def __init__(self):
        self.state = 1
        self.location = None
        super(Thing, self).__init__()
    def show_state(self):
        print self.state

class Breeze(Thing):
    """ A breeze object
    """
    def __init__(self, location=None):
        if location is not None:
            self.location = location
        super(Thing, self).__init__()


class Board(XYEnvironment):
    """ The board of the oozplorer game.  Inherit XYEnvironment
    """
    def __init__(self, some_number, prob_pit=20, silent=False):
        # some_number + 2 since the map is surrounded by walls.  2 extra cols/rows
        super(Board, self).__init__(some_number+2, some_number+2)
        self.p_pit = prob_pit
        self.silent = silent
        self.some_number = some_number
        self.add_walls()
        self.remove_duplicate_walls()
        self.matrix = None
        self.make_board()
        self.print_board()

    def print_board(self):
        """ Print the board.
        """
        if self.matrix is None:
            self.matrix = get_static_board_layout(self.things, self.width, self.height)
        if self.silent:
            return
        agent = self.agents[0]
        xloc, yloc = agent.location
        self.matrix[self.height - yloc - 1][xloc] = agent
        print_table(self.matrix)
        self.matrix[self.height - yloc - 1][xloc] = '<*  *>'
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
        """ Get the list of things in this world
        """
        return [Wall, Gold, Pit, Agent]
    #randome function we can use
    def generate():
        p = 0.2
        return random.random() <= p

    def percept(self, agent):
        """ Ride on top of lower things_near, but we don't want to know
        if the Pit is near, we want to know if a breeze is here.
        """
        xloc, yloc = agent.location
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
        if dead:
            print 'Your Agent Died'
            return dead
        elif winner:
            print 'Your Agent Wins'
            return winner
        return False

    def execute_action(self, agent, action):
        """ Have agent take an action.
        """
        if self.is_done():
            return
        agent.bump = False
        axloc, ayloc = action
        #time.sleep(1)
        self.executing_agent = agent
        sensor, state = self.move((axloc, ayloc))

    def default_location(self, thing):
        """ Get the default location for a thing.
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

    def add_agent(self, agent):
        """ Add an agent.
        """
        assert isinstance(agent, Agent)
        xloc, yloc = self.default_location(agent)
        agent.init_agent((xloc, yloc))
        self.things.append(agent)
        self.agents.append(agent)

    def make_board(self):
        """ Initialize the board according to assignment specs
        """
        generate = lambda: random.randint(1, 100) in range(1, self.p_pit+1)
        some_number = self.some_number
        agent = Agent(some_number)
        agent.program = Oozeplorer_Percept(agent)
        self.add_agent(agent)
        gold = Gold()
        self.add_thing(gold, None)
        for row in range(1, some_number + 1):
            for col in range(1, some_number + 1):
                valid_spot = (row, col) != gold.location and (row, col) != (1, 1)
                if valid_spot and generate():
                    t_pt = Pit()
                    t_pt.location = (row, col)
                    self.things.append(t_pt)

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
        xloc, yloc = pair
        self.executing_agent.location = (xloc, yloc)
        state = 0
        if any(self.list_things_at((xloc, yloc), tclass=Pit)):
            self.executing_agent.alive = False
            state = -1
        elif any(self.list_things_at((xloc, yloc), tclass=Gold)):
            self.executing_agent.winner = True
            state = 1
        percepts = self.percept(self.executing_agent)
        sensor = False
        if isinstance(percepts, Breeze):
            sensor = True
        self.print_board()
        return (sensor, state)


def satisfy(expression, true_var):
    """ Recursively remove true_var from expression.

    Args:
        - expression (Expr): An expression which trying to simplify.
        - true_var (Expr): A true variable to remove from the expression.

    Returns:
        - simplifed (Expr): The Expr now has no instances of true_var

    EXAMPLE:
    statement = expr('B01 <=> (P00 | P11 | P02) <=> (P00 | P11)')
    satisfy(statement, expr('P00'))
    statement becomes -> Expr('((B01 <=> (P11 | P02)) <=> P11)')
    """
    if len(expression.args) == 0:
        if expression.__repr__() == true_var.__repr__():
            return True
        else:
            return False
    cnt = 0
    while True:
        if cnt >= len(expression.args):
            break
        arg = expression.args[cnt]
        changed = satisfy(arg, true_var)
        if isinstance(changed, Expr):
            expression.args[cnt] = changed
        elif changed is True:
            expression.args.pop(cnt)
            expression = expression.args[0]
        cnt += 1
    return expression


def generate():
    return random.random() <= p

def create_logic(some_number):
	print some_number

def make_board(some_number):
    generate = lambda: random.randint(1, 10) in [1, 2]

    # some_number + 2 since the map is surrounded by walls.  2 extra cols/rows
    board = Board(width=some_number + 2, height=some_number + 2)
    agent = Agent(some_number)
    gold = Gold()
    board.add_thing(agent, None)
    board.agents.append(agent)
    board.add_thing(gold, None)
    row = 1
    for i in range(1, some_number + 1):
        col = 1
        #print "Row is %d" %row
        for j in range(1, some_number + 1):
            #print "Colum is %d" %col 
            if generate() and (row, col) != gold.location:
                #print "Enters here"
                if (row, col) != gold.location and (row, col) != (1, 1):
                    pt = Pit()
                    pt.location = (row, col)
                    board.things.append(pt)
            col = col + 1
        row+=1
    return board


def get_static_board_layout(things, width, height):
    """ Get a matrix of the board layout.
    """
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
    """ Hash the stuff in them map by their (x,y)
    """
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

def parse_arguments(arguments):
    """
    Args:
        arguments (list): sys.argv object.
    Returns:
        number (int): The integer command line argument.
    """
    def bail_out():
        """ End the program.
        """
        print 'Invalid Command line arguments.  Use Integers only.'
        sys.exit(1)
    try:
        number = int(arguments[1])
    except IndexError:
        bail_out()
    except ValueError:
        bail_out()
    if number <= 1:
        bail_out()
    return number

if __name__ == '__main__':
    print 'updating\n'

    b = make_board(3)

    print len(b.things)
    for t in b.things:
        print t, t.location
    out = convert_to_dict(b)
    print out 

    b.print_board()

    #randompit = b.things[40]
    #print randompit.location
    ARGS = sys.argv

    NUMBER = parse_arguments(ARGS)
    run_game(NUMBER)
    create_logic(NUMBER)
    #print NUMBER




    #NUMBER = parse_arguments(ARGS)

    #print NUMBER
    ARGS = sys.argv
    b = Board(4)
    b.run()

#pit = pit_iff((2,2),4)

#print pit
#print dpll_satisfiable(expr(pit))

""" 
=======
    SOME_NUM = parse_arguments(ARGS)
    _B = Board(SOME_NUM)
    _B.run()

    # wins = 0
    # for num in range(1000):
    #     B_ = Board(SOME_NUM, prob_pit=20, silent=True)
    #     B_.run()
    #     if B_.agents[0].is_winner():
    #         wins += 1
    # print 'Win Ratio:', ((wins*1.0) / 1000) * 100
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
    print bd.pe
    rcept(ag)
    print 'INITIAL MAP'
    print '   . . .   '
    print '   . P .   '
    print '   A . .   '
    print 'Move around the Pit and sense him or try to die.'
    bd.run()
"""

