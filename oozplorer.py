""" Insert docstring here

- Matthew Carlis
- Chris Nguyen
- Shunt Balushian
-Chris branch
"""
import sys
import random
from collections import defaultdict
from agents import Thing, XYEnvironment, Wall
from logic import KB, FolKB,PropKB,expr,dpll_satisfiable
from logic import *

from logic import KB, FolKB

AGENT = 'A{}{}'
GOLD = 'G{}{}'
PIT = 'P{}{}'
BREEZE = 'B{}{}'

# A Pit iff all his neighbors have breezes
PIT_IFF = 'P{}{} <=> (B{}{} & B{}{} & B{}{} & B{}{})'
# No pit iff one or more neighbors has no breeze.
N_PIT_IFF = '~P{}{} <=> (~B{}{} | ~B{}{} | ~B{}{} | ~B{}{})'

# A breeze iff one or more neighbors has a pit
BREEZE_IFF = 'B{}{} <=> (P{}{} | P {}{} | P{}{} | P{}{})'
# No breeze iff none of the neighbors have pits.
N_BREEZE_IFF = '~B{}{} <=> (~P{}{} & ~P {}{} & ~P{}{} & ~P{}{})'

def which_position(location, some_number, logic_gen):
    """ Determine if location is a corner, edge or has 4 neighbors.

    Args:
        - location (tuple): (x, y) position of the map.
        - some_number (int): The largest x or y value which is a valid move.
    """
    xpos, ypos = location
    if xpos == ypos or (1 in location and some_number in location):
        #CORNER. 2- Neighbors.
        # logic_gen(location, some_number)
        pass
    elif (1 in location or some_number in location):
        # EDGE. 3- Neighbors.
        # logic_gen(location, some_number)
        pass
    else:
        # Else 4- Neighbors.
        # logic_gen(location, some_number)
        pass


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
                    ret_v = raw_input('percept=%s; action: x, y?' % percept)
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

<<<<<<< HEAD
=======

class Breeze(Thing):
    def __init__(self, location=None):
        if location is not None:
            self.location = location

>>>>>>> e0ef8f31b1096945c30082f59958ccf636999117
class Board(XYEnvironment):
    """ The board of the oozplorer game.  Inherit XYEnvironment
    """
    def __init__(self, width=10, height=10):
        """
        """
        super(Board, self).__init__(width, height)
        self.add_walls()
        self.remove_duplicate_walls()

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
    #randome function we can use
    def generate():
        p = 0.2
        return random.random() <= p

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
            get_rand = lambda arg: random.choice(range(1, arg-1))
            while True:
                xloc, yloc = (get_rand(self.width), get_rand(self.height))
                if (1, 1) == (xloc, yloc):
                    continue
                break
            return (xloc, yloc)

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

<<<<<<< HEAD
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


if __name__ == '__main__':
    print 'updating\n'
    b = make_board(3)
    print len(b.things)
    for t in b.things:
        print t, t.location
    #randompit = b.things[40]
    #print randompit.location
    ARGS = sys.argv

    NUMBER = parse_arguments(ARGS)
    run_game(NUMBER)
    create_logic(NUMBER)
    #print NUMBER


kb = PropKB()
P = OzPit()
Gold = expr(~G)
Pit = expr(~P)
Breeze = expr(~Breeze)
e2 = expr("B21 ==> C11")
kb.tell(Gold)
kb.tell(Pit)
C = expr("A11 & B21")
P = expr("P")
print kb.ask(~A) #returns empty clause {} thus true
print kb.ask(P) #returns false

print dpll_satisfiable(A & ~B & C & (A | ~D) & (~E | ~D) & (C | ~D) & (~A | ~F) & (E | ~F) & (~D | ~F) & (B | ~C | D) & (A | ~E | F) & (~A | E | D))


    #NUMBER = parse_arguments(ARGS)
    b.run()
    #print NUMBER
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

