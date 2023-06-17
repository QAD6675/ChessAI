import random
import time

def findRandomMove(validMoves):
    time.sleep(0.5)
    return validMoves[random.randint(0, len(validMoves)-1)]