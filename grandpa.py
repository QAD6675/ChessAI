#NOTE - grandpa is greedy
materialValue = {"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE= 1000


def findBestMove(gs,validMoves):
    turnMultiplier = 1 if gs.white_to_move else -1
    maxEval=-CHECKMATE
    for playerMove in validMoves:
        gs.make_move(playerMove)
        eval=turnMultiplier * evaluate(gs,gs.board)
        if eval > maxEval:
            maxEval=eval
            bestMove=playerMove
        gs.undo_move()
    return bestMove

def evaluate(gs,board):
    eval = 0
    for rank in board:
        for square in rank:
            if square[0]=="w":
                eval += materialValue[square[1]]
            elif square[0]=="b":
                eval -= materialValue[square[1]]
    if gs.checkMate:
        eval= CHECKMATE
    elif gs.staleMate:
        eval= 0
    return eval