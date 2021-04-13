from gameboard import Board
import random
from gamerules import Checker
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        self.id = playernum
        self.board = board
        self.checker = checker
    
    @abstractmethod
    def play(self) -> int:
        pass

    def savestate(self):
        pass

class Human(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
      
    def play(self) -> int:
        col = int( input("Column: ") ) -1
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            print("Wrong column")
            self.play()


class ComputerRand(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)

    def play(self) -> int:
        col = random.randint(0, self.board.cols -1)
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            self.play() #Invalid column selected, try again
            

class ComputerDef(Player): #Defensive IA player
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
      
    def play(self) -> int:
        maxscore = 0
        selectedcolumn = 0
        
        # Tries to predict other player's best move and 'steals' it:
        for col in range(self.board.cols):
            row = self.board.insert(col, 1, trial=True)
            if row != -1:
                trialscore = self.checker.checkgrid(1, row, col)
                #print("trialscore: ", trialscore)
                if trialscore > maxscore:
                    maxscore = trialscore
                    selectedcolumn = col
                
        col = selectedcolumn
        #print("CPUscore: ", maxscore)
        if maxscore < 2:
            col = random.randint(0, self.board.cols -1)
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            self.play() #Invalid column selected, try again
            

class ComputerAI(Player): #Defensive IA player
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
        self.history = []
      
    def play(self) -> int:
        self.history.append(self.board.grid.copy()) #Saving opponent's last move
        maxscore = 0
        selectedcolumn = 0
        
        # Tries to predict other player's best move and 'steals' it:
        for col in range(self.board.cols):
            row = self.board.insert(col, 1, trial=True)
            if row != -1:
                trialscore = self.checker.checkgrid(1, row, col)
                #print("trialscore: ", trialscore)
                if trialscore > maxscore:
                    maxscore = trialscore
                    selectedcolumn = col
                
        col = selectedcolumn
        #print("CPUscore: ", maxscore)
        if maxscore < 2:
            col = random.randint(0, self.board.cols -1)
        row = self.board.insert(col, self.id)
        if row != -1:
            self.history.append(self.board.grid.copy()) # Saving ComputerAI's move
            print("History-len: ", len(self.history))
            return self.checker.check4win(self.id, row, col)
        else:
            self.play() #Invalid column selected, try again