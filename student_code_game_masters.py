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

        p1 = []
        p2 = []
        p3 = []

        fivedisk = self.kb.kb_ask(parse_input("fact: (on disk5 ?X"))

        if fivedisk is True:
            disk = ["disk1", "disk2", "disk3", "disk4", "disk5"]

        else:
            disk = ["disk1", "disk2", "disk3"]


        for d in disk:
            check = parse_input("fact: (on " + d + " ?X)")

            bindings = self.kb.kb_ask(check)
            b = str(bindings[0])

            if b == "?X : peg1":
                p1.append(int(d[-1]))

            elif b == "?X : peg2":
                p2.append(int(d[-1]))

            elif b == "?X : peg3":
                p3.append(int(d[-1]))
            else:
                print("Given impossible fact: only four pegs")

        peg1 = tuple(p1)
        peg2 = tuple(p2)
        peg3 = tuple(p3)

        return (peg1,peg2,peg3)

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
        ### Student code goes here
        
        game_state = self.getGameState()

        disk = str(movable_statement.terms[0])
        init_peg = str(movable_statement.terms[1])

        init = int(init_peg[-1])
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + init_peg + ")"))

        new_peg = str(movable_statement.terms[2])
        new = int(new_peg[-1])
        self.kb.kb_add(parse_input("fact: (on " + disk + " " + new_peg + ")"))

        status = game_state[new-1]
        if status:
            diskstr =str(game_state[new - 1][0])+" "
            self.kb.kb_retract(parse_input("fact: (top disk" +diskstr + new_peg + ")"))
        else:
            self.kb.kb_retract(parse_input("fact: (empty " +new_peg+ ")"))

        game_state = self.getGameState()
        nstatus = game_state[init-1]

        self.kb.kb_add(parse_input("fact: (top " + disk + " " + new_peg + ")"))
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + init_peg + ")"))

        if not nstatus:
            self.kb.kb_add(parse_input("fact: (empty " + init_peg + ")"))
        else:
            diskstr = str(nstatus[0]) +" "
            self.kb.kb_add(parse_input("fact: (top disk" + diskstr +init_peg+ ")"))
        

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
        row1 = []
        row2 = []
        row3 = []

        for row in range(3):
            for col in range(3):
                pos = parse_input("fact: (pos ?X pos" + str(row+1) + " pos" + str(col+1) + ")")
                tile = str(self.kb.kb_ask(pos)[0])[-1]

                if tile =="y":
                    tile = -1

                if col == 0:
                    row1.append(int(tile))
                elif col == 1:
                    row2.append(int(tile))
                elif col == 2:
                    row3.append(int(tile))

        r1 = tuple(row1)
        r2 = tuple(row2)
        r3 = tuple(row3)
        return (r1,r2,r3)
        


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
        game_state = self.getGameState()

        tile = str(movable_statement.terms[0])+" "
        oldx = str(movable_statement.terms[1])
        newx = str(movable_statement.terms[3])

        oldy = str(movable_statement.terms[2])
        newy = str(movable_statement.terms[4])

        self.kb.kb_retract(parse_input("fact: (pos " + tile + oldx + " " + oldy + ")"))
        self.kb.kb_add(parse_input("fact: (pos " + tile + newx + " " + newy + ")"))
        
        self.kb.kb_retract(parse_input("fact: (pos empty " + newx + " " + newy + ")"))
        self.kb.kb_add(parse_input("fact: (pos empty " + oldx + " " + oldy + ")"))

        
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