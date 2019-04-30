from game2 import GameState
from math import inf
import socket
import sys

gameState= GameState()
currBoard=None
depth=5

def minimaxMove():
    def alphaBeta(game,depth,alpha,beta,me):
        if game.isEnd() or depth==0:
            return (game.getScore(),-1)

        moves = game.getMoves()
        if me:
            ans = (-float('Inf'),-1)
            for move in moves:
                ans = max(ans,(alphaBeta(game.nextBoard(me,move),depth-1,alpha,beta,not me)[0],move))
                alpha= max(alpha,ans)
                if alpha >= beta:
                    break
            return alpha
        else:
            ans = (float('Inf'),-1)
            for move in moves:
                ans = min(ans,(alphaBeta(game.nextBoard(me,move),depth-1,alpha,beta,not me)[0],move))
                beta = min(beta,ans)
                if alpha>= beta:
                    break
            return beta

    alphaInitial=(-float('Inf'),-1)
    betaInitial = (float('Inf'),-1)

    ut,action = alphaBeta(gameState,depth, alphaInitial,betaInitial,True)
    gameState.move(currBoard,action,True)
    print("action is {}".format(action))
    return action



def agentSecondMove(firstBoard, firstMove):
    # First move
    gameState.move(firstBoard, firstMove,False)
    # Next move
    return minimaxMove()

def agentThirdMove(firstBoard, firstMove, secondMove):
    # First two moves
    gameState.move(firstBoard, firstMove,True)
    gameState.move(currBoard, secondMove,False)
    # Next move
    return minimaxMove()

def agentNextMove(prevMove):
    # Previous move
    gameState.move(currBoard, prevMove,False)
    # Next move
    return minimaxMove()

def agentLastMove(prevMove):
    gameState.move(currBoard, prevMove,False)


# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command =="start":
        if args[0] == "x":
            print("setting player to x")
            gameState.setPlayer('x')
        elif args[0] == "o":
            print("setting player to o ")
            gameState.setPlayer('o')
    elif command == "second_move":
        return agentSecondMove(int(args[0]), int(args[1]))
    elif command == "third_move":
        return agentThirdMove(int(args[0]), int(args[1]), int(args[2]))
    elif command == "next_move":
        return agentNextMove(int(args[0]))
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            print(response)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
