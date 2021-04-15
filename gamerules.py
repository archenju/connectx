from gameboard import Board

class Checker:
    def __init__(self, board: Board):
        self.board = board
        self.rows = board.rows
        self.cols = board.cols
        #print("Checker created")

    def check4win(self, player: int, row: int, col:int):
        score = self.checkgrid(player, row, col)
        done = score > 3
        reward = 0
        if score > 3:
            reward = 1
            if player == 1:
                print("Player 1 wins")
            else:
                print("Player 2 wins")
            self.board.keepplaying = False
            #return True
        if self.board.maxturns == 0:
            self.board.keepplaying = False
            print("DRAW")

        return self.board.grid,reward,done

    
    def checkgrid(self, player: int, x: int, y: int) -> int:
        score = self.__checkX(x,y,player)
        #if score > 3: return score
        score2 = self.__checkY(x,y,player)
        if score2 > score: score = score2
        score2 = self.__checkDiagUp(x,y,player)
        if score2 > score: score = score2
        score2 = self.__checkDiagDown(x,y,player)
        if score2 > score: score = score2
        return score
    
    def __checkY(self, x: int, y: int, player: int) -> int:
        score = 1
        xback = x
        xfwd = x
        while xback > 0:
            xback = xback - 1
            if self.board.grid[xback, y] == player:
                score = score + 1
            else:
                break
        while xfwd < self.rows-1:
            xfwd = xfwd + 1
            if self.board.grid[xfwd, y] == player:
                score = score + 1
            else:
                break
        #print("scoreY: ", score)
        return score
        
    def __checkX(self, x: int, y: int, player: int) -> int:
        score = 1 
        yback = y
        yfwd = y
        while yback > 0:
            yback = yback -1
            if self.board.grid[x, yback] == player:
                score = score + 1
            else:
                break
        while yfwd < self.cols-1:
            yfwd = yfwd + 1
            if self.board.grid[x, yfwd] == player:
                score = score + 1
            else:
                break
        #print("scoreX: ", score)
        return score

    def __checkDiagUp(self, x: int, y: int, player: int) -> int:
        score = 1
        xback = x
        yback = y
        while xback > 0 and yback > 0:
            xback = xback -1
            yback = yback -1
            if self.board.grid[xback, yback] == player:
                score = score + 1
            else:
                break
        xfwd = x
        yfwd = y
        while xfwd < self.rows-1 and yfwd < self.cols-1 :
            xfwd = xfwd +1
            yfwd = yfwd +1
            if self.board.grid[xfwd, yfwd] == player:
                score = score +1
            else:
                break
        #print("scoreDiag: ", score)
        return score
    
    def __checkDiagDown(self, x: int, y: int, player: int) -> int:
        score = 1
        xback = x
        yback = y
        while xback > 0 and yback < self.cols-1:
            xback = xback -1
            yback = yback +1
            if self.board.grid[xback, yback] == player:
                score = score + 1
            else:
                break
        xfwd = x
        yfwd = y
        while xfwd < self.rows-1 and yfwd > 0 :
            xfwd = xfwd +1
            yfwd = yfwd -1
            if self.board.grid[xfwd, yfwd] == player:
                score = score +1
            else:
                break
        #print("scoreDiag2: ", score)
        return score        
