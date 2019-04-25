'''Player X is 1
   Player O is -1
   No one played so far is 0
'''

import copy

#this is a object which represents the current state of the board
class BoardState(object):
    def __init__(self,player):
        self.curPlayer = player
        self.boards = [[0 for x in range(1, 10)] for o in range(1, 10)]
        self.curBoardNumber = 0
        self.lastMove = 0
        self.lastBoardNumber = 0
        self.xPlayerScore = 0
        self.oPlayerScore = 0


    def getScore(self):
        if self.curPlayer==1:
            return self.xPlayerScore - self.oPlayerScore
        else:
            return self.oPlayerScore - self.xPlayerScore


    # generating a list of valid moves for the current board
    def validMoves(self):
        validMoves=[]

        for i in range(9):
            if self.boards[curBoardNumber][i]==0:
                validMoves.append(i+1)

        return validMoves

    #updates the current state of the board by adding a move
    def move(self,board,move):

        if board is None:
            board = self.curBoardNumber

        self.lastBoardNumber= self.curBoardNumber
        self.lastMove= move
        self.curBoardNumber= move


		self.boards[board-1][move] = self.curPlayer


        self.xPlayerScore= self.boardScore(1)
        self.oPlayerScore = self.boardScore(-1)

		self.curPlayer = -self.curPlayer



    def boardScore(self,player):
        current = self.lastBoardNumber-1
        score =0

        combos = []
        for i in range(0, 3):
            combos.append(range(i*3, i*3+3))
            combos.append(range(i, 9, 3))
        combos.append(range(2, 8, 2))
        combos.append(range(0, 9, 4))
        for possibleWinner in combos:
            count = 0
            for i in possibleWinner:
                if self.boards[current][i] == player:
                    count += 1
                elif self.boards[current][i] == -player:
                    count -= 3
            if count == 3:
                score += 1000000
            elif count == 2:
                score += 10
            elif count == 1:
                score += 1
        return score



    # creates a new board which adds a move to the current board
    def nextBoard(self,move):
        newB= copy.deepcopy(self)
        newB.move(None,board)
        return newB
