import random
import time

materialValue = {"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE= 1000
DEPTH = 4

def findBestMove(gs,validMoves):
    global nextMove
    nextMove=None
    random.shuffle(validMoves)
    findNiggaMaxWithPruningMove(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.white_to_move else -1)
    return nextMove

def findNiggaMaxWithPruningMove(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * evaluate(gs)
    maxEval = -CHECKMATE
    for move in validMoves:
        gs.make_move(move,True)
        nextMoves=gs.getLegalMoves()
        eval = -findNiggaMaxWithPruningMove(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if eval> maxEval:
            maxEval = eval
            if depth == DEPTH:
                nextMove = move
        gs.undo_move()
        if maxEval > alpha:
            alpha = maxEval
        if alpha >= beta:
            break
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