'''Player X is 1
   Player O is -1
   No one played so far is 0
'''

class boardState(object):
    def __init__(self,player):
        curPlayer = player
        self.boards = [[0 for x in range(1, 10)] for o in range(1, 10)]
        self.curBoardNumber = 0
        self.lastMove = 0
        self.lastBoardNumber = 0
        self.xPlayerScore = 0
        self.oPlayerScore = 0

    def move(self,pos):
		self.boards[self.][pos[1]] = self.currPlayer
		self.updateMiniWinners(pos)
		self.updateWinner()
		self.updateValidMoves(pos)
		self.currPlayer = -self.currPlayer
		self.numMoves += 1
