'''Player X is 1
   Player O is -1
   No one played so far is 0
'''

import copy

#this is a object which represents the current state of the board
class boardState(object):
    def __init__(self,player):
        self.curPlayer = player
        self.boards = [[0 for x in range(1, 10)] for o in range(1, 10)]
        self.curBoardNumber = 0
        self.lastMove = 0
        self.lastBoardNumber = 0
        self.xPlayerScore = 0
        self.oPlayerScore = 0

    # generating a list of valid moves for the current board
    def validMoves(self):
        validMoves=[]

        for i in range(9):
            if self.boards[curBoardNumber][i]==0:
                validMoves.append(i+1)

        return validMoves

    #updates the current state of the board by adding a move
    def move(self,move):
        self.lastBoardNumber= self.curBoardNumber
        self.lastMove= move
        self.curBoardNumber= move


		self.boards[curBoardNumber-1][move] = self.curPlayer

        '''HAVE TO ADD SCORE FUNCTION HERE'''

		self.curPlayer = -self.curPlayer


    # creates a new board which adds a move to the current board
    def nextBoard(self,move):
        newB= copy.deepcopy(self)
        newB.move(move)
        return newB
