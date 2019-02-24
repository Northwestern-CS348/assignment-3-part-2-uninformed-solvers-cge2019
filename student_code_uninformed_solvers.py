
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        #pre-set move as explored + get moves + check if win
        self.visited[self.currentState] = True

        options = self.gm.getMovables() 
        nextmove = self.currentState.nextChildToVisit
        if self.currentState.state == self.victoryCondition:
            return True


        while nextmove < len(options):
            n = options[nextmove]
            self.gm.makeMove(n)
            game_state = self.gm.getGameState()

            #action done before?
            done = False
            for state in self.visited.keys():
                if state.state == game_state:
                    done = True

            if done:
                self.gm.reverseMove(n)
                nextmove +=1

            #now we know if action has been done or not, add new child node for actions
            else:
                new_state = GameState(game_state, self.currentState.depth + 1, n)
                new_state.parent = self.currentState
                self.currentState.children.append(new_state)
                self.currentState.nextChildToVisit = nextmove + 1
                
                self.currentState = new_state
                break
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
