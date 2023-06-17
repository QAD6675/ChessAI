import random
import time
# NOTE - noob just picks random legal moves
def findBestMove(gs,validMoves):
    time.sleep(0.5)
    return validMoves[random.randint(0, len(validMoves)-1)]