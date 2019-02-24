from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        disks = {}
        disk = ''
        ask = [parse_input("fact: (on ?disk peg1)")]
        ask.append(parse_input("fact: (on ?disk peg2)"))
        ask.append(parse_input("fact: (on ?disk peg3)"))
        tuples = []
        for question in range(3):
            bindings = self.kb.kb_ask(ask[question])
            disks[question] = []
            if bindings:
                for b in bindings:
                    b = list(b.bindings_dict.values())[0]
                    disk = int(''.join(el for el in b if el.isdigit()))
                    disks[question].append(disk)
            tuples.append(tuple(sorted(disks[question])))

        tuples = tuple(tuples)
        return tuples

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes heredisk = movable_statement.terms[0].term.element
        init_peg = movable_statement.terms[1].term.element
        init_peg_num = int(''.join(el for el in init_peg if el.isdigit()))
        new_peg = movable_statement.terms[2].term.element

        # Change what's on what
        fact = parse_input("fact: (on " + disk + " " + init_peg + ")")
        self.kb.kb_retract(fact)
        new_fact = parse_input("fact: (on " + disk + " " + new_peg + ")")
        self.kb.kb_assert(new_fact)

        # Change empties and tops for destination peg
        old_empty = parse_input("fact: (empty " + new_peg + ")")
        self.kb.kb_retract(old_empty)
        old_top_binding = self.kb.kb_ask(parse_input("fact: (top ?disk " + new_peg + ")"))
        old_top_disk = ''
        if old_top_binding:
            old_top_disk = old_top_binding[0].bindings[0].constant.element
        old_top_dst = parse_input("fact: (top " + old_top_disk + " " + new_peg + ")")
        self.kb.kb_retract(old_top_dst)
        new_top_dst = parse_input("fact: (top " + disk + " " + new_peg + ")")
        self.kb.kb_assert(new_top_dst)

        # Change empties and tops for original peg
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + init_peg + ")"))
        on_init_peg = self.getGameState()[init_peg_num - 1]
        if not on_init_peg:
            new_empty = parse_input("fact: (empty " + init_peg + ")")
            self.kb.kb_assert(new_empty)
        else:
            self.kb.kb_assert(parse_input("fact: (top disk" + str(on_init_peg[0]) + " " + init_peg + ")"))

        return


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        state = [[],[],[]]
        l1 = 'fact: (location ?x {} pos1)'
        l2 = 'fact: (location ?x {} pos2)'
        l3 = 'fact: (location ?x {} pos3)'

        ask_loc = [l1,l2,l3]
        axis = ['pos1', 'pos2','pos3']

        for i,q in enumerate(ask_loc):
            for x in axis:
                p1  = q.format(x)
                question = parse_input(p1)
                exist = self.kb.kb_ask(question)
                tile = exist[0].bindings[0].constant.element
                if tile == 'empty':
                    state[i].append(-1)
                else:
                    state[i].append(int(tile[-1]))

        state = tuple([tuple(item) for item in state])

        return state


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        given = movable_statement.terms
        tile = given[0]
        x = given[1]
        y =given[2]
        newx = given[3]
        newy = given[4]
        #retract this
        old_loc = parse_input('fact: (location {} {} {})').format(tile,x,y)
        old_empty_loc = parse_input('fact: (location empty {} {})').format(newx, newy)
        self.kb.kb_retract(old_loc)
        self.kb.kb_retract(old_empty_loc)

        #assert this
        new_loc = parse_input('fact: (location {} {} {})').format(tile, newx, newy)
        new_empty_loc = parse_input('fact: (location empty {} {})').format(x, y)
        self.kb.kb_assert(new_loc)
        self.kb.kb_assert(new_empty_loc)

        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
