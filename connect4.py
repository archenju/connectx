from players import Human, ComputerRand, ComputerDef, ComputerAI
from gameboard import Board
from gamerules import Checker
import argparse

class Connect4:
    
    def __init__(self):
        self.col = -1
        self.board = -1
        self.checkre = -1
        self.player1 = -1
        self.player2 = -1
        self.repeat = 1
        
    def initgame(self):
        
        parser = argparse.ArgumentParser(description="....")
        parser.add_argument("size", 
                            type=int,
                            help="number of columns in the board")
        parser.add_argument("-m", "--mode", 
                            type=str,
                            help="type of game (hxh, hxr, rxh, rxr)",
                            choices=["hxh","hxr","rxh","rxr"],
                            default = "hxh")
        parser.add_argument("-r", "--repeat", 
                            type=int,
                            help="repeat game",
                            default = 1)
        args = parser.parse_args()

        self.col = args.size
        self.repeat = args.repeat
        self.board = Board(self.col)
        self.checker = Checker(self.board)
        self.board.display()
    
        if args.mode == "hxh":
            self.player1 = Human(1, self.board, self.checker)
            self.player2 = Human(-1, self.board, self.checker)
        elif args.mode == "hxr":
            self.player1 = Human(1, self.board, self.checker)
            self.player2 = ComputerAI(-1, self.board, self.checker)
        elif args.mode == "rxh":
            self.player1 = ComputerAI(1, self.board, self.checker)
            self.player2 = Human(-1, self.board, self.checker)
            pass
        else:
            self.player1 = ComputerRand(1, self.board, self.checker)
            self.player2 = ComputerAI(-1, self.board, self.checker)

            
    def startgame(self):
        while self.repeat > 0:
            print("Repeat left: ", self.repeat)
            self.repeat = self.repeat - 1
            self.board.reset()
            
            while self.board.keepplaying:
                print("Player 1")
                self.player1.play()
                self.board.display()
                if self.board.keepplaying:
                    print("Player 2")
                    self.player2.play()
                    self.board.display()
            self.player1.savestate()
            self.player2.savestate()
            print("Repeating", self.repeat, "times")
 


print("")
game = Connect4()
game.initgame()
game.startgame()
