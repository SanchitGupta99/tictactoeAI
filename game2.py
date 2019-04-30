import copy

playerX = "X"
playerO = "O"
playerEmpty ="-"


class GameState(object):
    player=""
    curBoardNumber=0
    lastMove=0
    lastBoardNumber=0
    boards= [[playerEmpty for x in range(1,10)] for o in range(1,10)]
    xPlayerScore=0
    oPlayerScore=0

    def setPlayer(self,player):
        self.player=player

    def move(self,board,move, me):
        if board == None:
            board = self.curBoardNumber

        xbefore = self.score(board,playerX)
        obefore = self.score(board,playerO)

        if me:
            self.boards[board-1][move-1]= self.player
        elif self.player == playerO:
            self.boards[board-1][move-1]= playerX
        else:
            self.boards[board-1][move-1]= playerO

        xafter = self.score(board,playerX)
        oafter = self.score(board,playerO)

        difx= xafter-xbefore
        difo = oafter-obefore

        self.xPlayerScore +=difx
        self.oPlayerScore+=difo

        self.lastMove=move
        self.lastBoardNumber=board
        self.curBoardNumber=move


    def score(self,board,player):
        score =0
        winners=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

        for combos in winners:
            count =0
            for i in combos:
                if self.boards[board-1][i]==player:
                    count+=1
                elif self.boards[board-1][i]!=playerEmpty:
                    count-=2
            if count ==3:
                score +=10000
            elif count==2:
                score +=10
            elif count==1:
                score+=3

        return score

    def checkLegalMove(self,move):
        return self.boards[self.curBoardNumber-1][move-1]==playerEmpty

    def getMoves(self):
        moves=[]
        for i in range(1,10):
            if self.checkLegalMove(i):
                moves.append(i)
        return moves

    def getScore(self):
        if self.player == playerX:
            return self.xPlayerScore-self.oPlayerScore
        else:
            return self.oPlayerScore-self.xPlayerScore

    def __copy__(self):
        copied = GameState()
        copied.player = copy.deepcopy(self.player)
        copied.curBoardNumber=copy.deepcopy(self.curBoardNumber)
        copied.lastMove=copy.deepcopy(self.lastMove)
        copied.lastBoardNumber=copy.deepcopy(self.lastBoardNumber)
        copied.boards= copy.deepcopy(self.boards)
        copied.xPlayerScore=copy.deepcopy(self.xPlayerScore)
        copied.oPlayerScore=copy.deepcopy(self.oPlayerScore)
        return copied

    def nextBoard(self,me,move):
        newB = copy.copy(self)
        newB.move(move,self.curBoardNumber,not me)
        return newB



    def isEnd(self):
        winners=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for i in range(9):
            for combo in winners:
                xcount =0
                ocount =0
                for j in combo:
                    if self.boards[i][j]==playerX:
                        xcount = xcount +1
                    elif self.boards[i][j]==playerO:
                        ocount = ocount +1
                if ocount ==3 or xcount ==3:
                    print('Somones won')
                    return True
        return False
