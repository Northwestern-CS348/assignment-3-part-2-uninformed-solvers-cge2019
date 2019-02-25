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
        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            if self.victoryCondition == self.currentState.state: 
                return True
            else:
                return False

        elif self.currentState not in self.visited:
            self.visited[self.currentState] = True

            if self.currentState.state == self.victoryCondition:
                return True
            else:
                return False

        nxt = self.currentState.nextChildToVisit
        curr = self.currentState

        if nxt == False:
            for p in self.gm.getMovables():
                self.gm.makeMove(p)

                game_state = self.gm.getGameState()
                new_state = GameState(game_state, curr.depth + 1, p)

                if new_state not in self.visited:
                    new_state.parent = curr
                    curr.children.append(new_state)

                self.gm.reverseMove(p)            
            
        childs = len(self.currentState.children)
        if nxt >= childs:

            nxt = nxt + 1
            curr = curr.parent
            self.gm.reverseMove(self.currentState.requiredMovable)
            
            return self.solveOneStep()


        else:
            game_state = curr.children[self.currentState.nextChildToVisit]
            nxt = nxt + 1
            self.currentState = game_state
            
            self.gm.makeMove(game_state.requiredMovable)

            return self.solveOneStep()


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

        if self.currentState.state == self.victoryCondition:
                self.visited[self.currentState] = True
                if self.victoryCondition == self.currentState.state: 
                    return True
                else:
                    return False

        if self.currentState not in self.visited:
            self.visited[self.currentState] = True

            if self.currentState.state == self.victoryCondition:
                return True
            else:
                return False

        sd = self.currentState.depth
        start = True
        while start:
            res = self.helper(sd)

            if not res:
                start = False

            else:
                if self.currentState.state != self.victoryCondition:
                    sd = sd + 1

                else:
                    res = True
                    return res
        return False


    def helper(self, depth):
        curr = self.currentState
        #stops working at some point?
        if curr.depth > depth:
            self.gm.reverseMove(curr.requiredMovable)
            curr = curr.parent
            output = self.helper(depth)

            return output

        elif curr.depth == depth:
            if len(curr.children) == 0 and not depth:
                for p in self.gm.getMovables():
                    self.gm.makeMove(p)
                    game_state = self.gm.getGameState()
                    new_state = GameState(game_state, curr.depth + 1, p)  
                    if new_state not in self.visited:
                        new_state.parent = curr
                        curr.children.append(new_state)
                    self.gm.reverseMove(p)  

            elif curr not in self.visited:
                for p in self.gm.getMovables():
                    self.gm.makeMove(p)
                    game_state = self.gm.getGameState()
                    new_state = GameState(game_state, curr.depth + 1, p)  
                    if new_state not in self.visited:
                        new_state.parent = curr
                        curr.children.append(new_state)
                    self.gm.reverseMove(p)  

            if self.currentState not in self.visited:
                self.visited[self.currentState] = True

                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False
            
            elif self.currentState.state == self.victoryCondition:
                self.visited[self.currentState] = True
                if self.victoryCondition == self.currentState.state: 
                    return True
                else:
                    return False

            

            else:
                if not self.currentState.depth: 
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)

                self.currentState = self.currentState.parent
                return self.helper(depth)   

        else:
            childs = len(self.currentState.children)

            if self.currentState.nextChildToVisit > childs:
                self.currentState.nextChildToVisit = 0

            if self.currentState.nextChildToVisit == childs:
                 
                self.currentState.nextChildToVisit=self.currentState.nextChildToVisit + 1
                
                if not self.currentState.depth: 
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                
                self.currentState = self.currentState.parent
                return self.helper(depth)

            else:
                game_state = self.currentState.children[self.currentState.nextChildToVisit]

                self.currentState.nextChildToVisit =self.currentState.nextChildToVisit + 1
                self.currentState = game_state
                self.gm.makeMove(game_state.requiredMovable)
                
                return self.helper(depth)
