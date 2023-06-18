import random
import time

materialValue = {"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE= 1000
DEPTH = 2

def findBestMove(gs,validMoves):
    global nextMove
    nextMove=None
    random.shuffle(validMoves)
    findNiggaMaxMove(gs,validMoves,DEPTH,1 if gs.white_to_move else -1)
    return nextMove

def findNiggaMaxMove(gs,validMoves,depth,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * evaluate(gs)
    maxEval = -CHECKMATE
    for move in validMoves:
        gs.make_move(move,True)
        nextMoves=gs.getLegalMoves()
        eval = -findNiggaMaxMove(gs,nextMoves,depth-1,-turnMultiplier)
        if eval> maxEval:
            maxEval = eval
            if depth == DEPTH:
                nextMove = move
        gs.undo_move()
    return maxEval
    

def evaluate(gs):
    if gs.checkMate:
        if gs.white:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return 0
    eval = 0
    for rank in gs.board:
        for square in rank:
            if square[0]=="w":
                eval += materialValue[square[1]]
            elif square[0]=="b":
                eval -= materialValue[square[1]]
    return eval


def findRandomMove(validMoves):
    time.sleep(0.5)
    return validMoves[random.randint(0, len(validMoves)-1)]