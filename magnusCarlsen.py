import random
import time
from chessEngine import Move

materialValue = {"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE= 1000


def findBestMove(gs,validMoves):
    turnMultiplier = 1 if gs.white_to_move else -1
    oppMinMaxEval=CHECKMATE
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.make_move(playerMove,isAI=True)
        oppMoves = gs.getLegalMoves()
        if gs.checkMate:
            oppMaxEval=-CHECKMATE
        elif gs.staleMate:
            oppMaxEval=0
        else:
            oppMaxEval = -CHECKMATE
            for oppMove in oppMoves:
                gs.make_move(oppMove,isAI=True)
                if gs.checkMate:
                    eval= CHECKMATE
                elif gs.staleMate:
                    eval= 0
                else:
                    eval=-turnMultiplier * evaluate(gs)
                if eval > oppMaxEval:
                    oppMaxEval=eval
                gs.undo_move()
            if oppMaxEval < oppMinMaxEval:
                oppMinMaxEval=oppMaxEval
                bestMove=playerMove
            gs.undo_move()
    
    return bestMove

def evaluate(gs):
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