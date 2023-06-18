import random
import time

materialValue = {"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE= 1000
DEPTH = 2

def findBestMove(gs,validMoves):
    global nextMove
    nextMove=None
    findMinMaxMove(gs,validMoves,DEPTH,gs.white_to_move)
    return nextMove

def findMinMaxMove(gs,validMoves,depth,white_to_move):
    global nextMove
    if depth==0:
        return evaluate(gs)
    if white_to_move:
        maxEval = -CHECKMATE
        for move in validMoves:
            gs.make_move(move)
            nextMoves=gs.getLegalMoves()
            eval = findMinMaxMove(gs,nextMoves,depth-1,False)
            if eval> maxEval:
                maxEval = eval
                if depth == DEPTH:
                    nextMove =move
            gs.undo_move()
        return maxEval
    else:
        minEval = CHECKMATE
        for move in validMoves:
            gs.make_move(move)
            nextMoves=gs.getLegalMoves()
            eval = findMinMaxMove(gs,nextMoves,depth-1,True)
            if eval< minEval:
                minEval = eval
                if depth == DEPTH:
                    nextMove =move
            gs.undo_move()
        return minEval
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