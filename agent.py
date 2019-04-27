from game import GameState
from math import inf

gameState = None
currBoard = None
MINIMAX_DEPTH = 5

def minimaxMove():
    return alphaBeta(gameState, MINIMAX_DEPTH, (-1 * inf,-1), (inf,-1))[1]

def alphaBeta(game, depth, alpha, beta):
    if game.isEnd() or depth == 0:
        return (game.getScore(),-1)

    moves = game.validMoves()

    for move in moves:
        alpha = max(alpha, (-1 * alphaBeta(game.nextBoard(move), depth-1, -beta, -alpha)[0],move))
        if alpha >= beta:
            return alpha
    return alpha

# called at the beginning of each game
def agentSecondMove(firstBoard, firstMove):
    # First move
    gameState.move(firstBoard, firstMove)
    gameState.flipPlayer()
    # Next move
    minimaxMove()

def agentThirdMove(firstBoard, firstMove, secondMove):
    # First two moves
    gameState.move(firstBoard, firstMove)
    gameState.move(currBoard, secondMove)
    # Next move
    minimaxMove()

def agentNextMove(prevMove):
    # Previous move
    gameState.move(currBoard, prevMove)
    # Next move
    minimaxMove()

def agentLastMove(prevMove):
    gameState.move(currBoard, prevMove)


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
            gameState = GameState(1)
        elif args[0] == "o":
            gameState = GameState(-1)
    elif command == "second_move":
        agentSecondMove(int(args[0]), int(args[1]))
    elif command == "third_move":
        agentThirdMove(int(args[0]), int(args[1]), int(args[2]))
    elif command == "next_move":
        agentNextMove(int(args[0]))
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
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
