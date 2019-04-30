'''Player X is 1
   Player O is -1
   No one played so far is 0
'''

import copy

#this is a object which represents the current state of the board
class GameState(object):
    def __init__(self):
        self.us=0
        self.curPlayer = 0
        self.boards = [[0 for x in range(9)] for o in range(9)]
        self.curBoardNumber = None
        self.lastBoardNumber = None
        self.xPlayerScore = 0
        self.oPlayerScore = 0



    def __copy__(self):
        board_copy = GameState()
        board_copy.boards = copy.deepcopy(self.boards)
        board_copy.us = copy.deepcopy(self.us)
        board_copy.xPlayerScore = copy.deepcopy(self.xPlayerScore)
        board_copy.oPlayerScore = copy.deepcopy(self.oPlayerScore)
        board_copy.curBoardNumber = copy.deepcopy(self.curBoardNumber)
        board_copy.curPlayer= copy.deepcopy(self.curPlayer)
        return board_copy

    def setPlayer(self,a):
        if a=='x':
            self.us=1
            self.curPlayer=1
        elif a=='o':
            self.us=-1
            self.curPlayer=-1


    def getScore(self):
        if self.us==1:
            return self.xPlayerScore - self.oPlayerScore
        else:
            return self.oPlayerScore - self.xPlayerScore

    def flipPlayer(self):
        self.curPlayer=self.curPlayer*-1

    # generating a list of valid moves for the current board
    def validMoves(self):
        validMoves=[]
        for i in range(9):
            if self.boards[self.curBoardNumber][i]==0:
                validMoves.append(i+1)

        return validMoves

    #updates the current state of the board by adding a move
    def move(self,board,move):
        move=move-1

        if board is None:
            board = self.curBoardNumber
        else:
            board = board-1



        if self.lastBoardNumber == None:
            self.lastBoardNumber=board
        else:
            self.lastBoardNumber= self.curBoardNumber

        previous_x = self.boardScore(1,board)
        previous_o = self.boardScore(-1,board)

        self.boards[board][move] = self.curPlayer

        new_x = self.boardScore(1,board)
        new_o = self.boardScore(-1,board)

        self.xPlayerScore= self.xPlayerScore - previous_x + new_x
        self.oPlayerScore = self.oPlayerScore - previous_o + new_o

        self.curBoardNumber= move
        self.curPlayer = -self.curPlayer



    def boardScore(self,player,current):
        score =0
        combos = []
        for i in range(0, 3):
            combos.append(list(range(i*3, i*3+3)))
            combos.append(list(range(i, 9, 3)))
        combos.append(list(range(2, 8, 2)))
        combos.append(list(range(0, 9, 4)))
        for possibleWinner in combos:
            count = 0
            for i in possibleWinner:
                if self.boards[current][i] == player:
                    count += 1
                elif self.boards[current][i] == -player:
                    count -= 2
            if count == 3:
                score += 1000000
            elif count == 2:
                score += 10
            elif count == 1:
                score += 1
        return score



    def isEnd(self):
        combos = []
        for i in range(0, 3):
            combos.append(range(i*3, i*3+3))
            combos.append(range(i, 9, 3))
        combos.append(range(2, 8, 2))
        combos.append(range(0, 9, 4))
        for current in range(9):
            for possibleWinner in combos:
                count = 0
                for i in possibleWinner:
                    if self.boards[current][i] == 1:
                        count += 1
                if count == 3:
                    print("IVE HTI END WITH X")
                    return True
            for possibleWinner in combos:
                count = 0
                for i in possibleWinner:
                    if self.boards[current][i] == -1:
                        count += 1
                if count == 3:
                    return True
        return False
    # creates a new board which adds a move to the current board
    def nextBoard(self,move):
        #print(move)
        newB= copy.copy(self)
        newB.move(None,move)
        return newB
