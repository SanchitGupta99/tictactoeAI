#!/usr/bin/python
from game import GameState
from math import inf
import socket
import sys

gameState = GameState()
currBoard = None
MINIMAX_DEPTH = 3
'''
class Tree(object):
    """A Tree with a list of Trees as children
        and a value (a Board)"""
    children = []
    value = None

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)


def generate_tree(current_board, depth):
    """Generate a Tree from a given board"""
    states = Tree(current_board)

    if depth == 0:
        return states

    moves = current_board.validMoves()
    if depth==3:
        print(moves)
    for i in moves:
        states.add_child(generate_tree(current_board.nextBoard(i), depth - 1))
    return states


def minimaxMove():
    move_tree = generate_tree(gameState,MINIMAX_DEPTH)

    best_board = None
    best_score = -1000000

    a = -1000000000
    b =  1000000000
    for child in move_tree.children:
        child_score = min_score(child, a, b)
        if child_score > best_score:
            best_board = child.value
            best_score = child_score

    gameState.move(currBoard,best_board.curBoardNumber)
    print("BEST ATION IS {} WITH SCORE {}".format(best_board.curBoardNumber,best_score))
    return best_board.curBoardNumber



def max_score(tree, a, b):

    if len(tree.children) == 0:
        return tree.value.getScore()

    for child in tree.children:
        a = max(a, min_score(child, a, b))
        if b <= a:
            break
    return a


def min_score(tree, a, b):

    if len(tree.children) == 0:
        return tree.value.getScore()

    for child in tree.children:
        b = min(b, max_score(child, a, b))
        if b <= a:
            break
    return b




#VERSION 2

'''
def minimaxMove():
    def alphaBeta(game,player,depth,alpha,beta):
        if game.isEnd() or depth==0:
            return (game.getScore(),-1)
        moves = game.validMoves()
        if depth==3:
            print(str(game.curBoardNumber) + "woth moves" + str(moves))
        if player ==1:
            ans = (-float('Inf'),-1)
            for move in moves:
                ans = max(ans, (alphaBeta(game.nextBoard(move),-player,depth-1,alpha,beta)[0],move))
                alpha = max(alpha,ans)
                if alpha>=beta:
                    break
            return alpha
        else:
            ans = (float('Inf'),-1)
            for move in moves:
                ans = min(ans,(alphaBeta(game.nextBoard(move),-player,depth-1,alpha,beta)[0],move))
                beta = min(beta,ans)
                if alpha>=beta:
                    break
            return beta
    alphInitial = (-float('Inf'),-1)
    betInitial = (float('Inf'),-1)
    ut,action=alphaBeta(gameState,1,MINIMAX_DEPTH,alphInitial,betInitial)
    print("THE ACTION IS {} with score {}".format(action,ut))
    gameState.move(currBoard,action)
    return action

'''

#VERSION 1

def minimaxMove():
    move= alphaBeta(gameState, MINIMAX_DEPTH, (-1 * inf,-1), (inf,-1))[1]
    gameState.move(currBoard,move)
    return move

def alphaBeta(game, depth, alpha, beta):
    if game.isEnd() or depth == 0:
        return (game.getScore(),-1)

    moves = game.validMoves()

    for move in moves:
        alpha = max(alpha, (alphaBeta(gameState.nextBoard(move),
							depth - 1, -1*beta, -1*alpha)[0]*-1, move))
        #print(alpha)
        if alpha >= beta:
            return alpha
    return alpha
'''



# called at the beginning of each game
def agentSecondMove(firstBoard, firstMove):
    # First move
    gameState.flipPlayer()
    gameState.move(firstBoard, firstMove)
    # Next move
    return minimaxMove()

def agentThirdMove(firstBoard, firstMove, secondMove):
    # First two moves
    gameState.move(firstBoard, firstMove)
    gameState.move(currBoard, secondMove)
    # Next move
    return minimaxMove()

def agentNextMove(prevMove):
    # Previous move
    gameState.move(currBoard, prevMove)
    # Next move
    return minimaxMove()

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
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
