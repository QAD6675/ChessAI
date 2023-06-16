import pygame as p
from chessEngine import GameState,Move

WIDTH = HEIGHT = 512
DIMENTIONS = 8
SQUARE_SIZE= HEIGHT // DIMENTIONS
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR","bN","bB","bQ","bK","bB","bN","bR","bp","wR","wN","wB","wQ","wK","wB","wN","wR","wp"]
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("pics/"+piece+".png"),(SQUARE_SIZE,SQUARE_SIZE))
        #NOTE - you can access imgs via the IMAGES dictionary

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    gs = GameState()
    validMoves = gs.getLegalMoves()
    gameOver = False
    animate=False
    loadImages()
    running = True
    sqSelected =()
    playerClicks = []
    moveMade = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    moveMade=True
                    animate = False
                elif e.key == p.K_r:
                    gs= GameState()
                    validMoves= gs.getLegalMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
            elif e.type == p.MOUSEBUTTONDOWN: #SECTION - onclick
                if not gameOver:
                    location = p.mouse.get_pos()
                    col=location[0] // SQUARE_SIZE
                    row=location[1] // SQUARE_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected= (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks)==2:
                        move = Move(playerClicks[0], playerClicks[1],gs)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.make_move(validMoves[i])
                                gs.inCheck,gs.pins,gs.checks=gs.checkforChecksAndPins()
                                print(validMoves[i].getChessNotation(gs))
                                moveMade = True
                                animate=True
                                sqSelected= ()
                                playerClicks= []
                        if not moveMade:
                            playerClicks= [sqSelected]

        if moveMade:
            validMoves=gs.getLegalMoves()
            if animate:
                animateMoves(gs.move_log[-1],screen,gs.board,clock)
            moveMade=False
        drawGameState(screen,gs,validMoves,sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        
        
#SECTION - graphics
def drawGameState(screen,gs,validMoves,sqSelected): 
    drawBoard(screen) #NOTE - this draws the squares
    highlightSquares(screen,gs,validMoves,sqSelected)   #NOTE - this draws the squares
    drawPieces(screen,gs.board)#NOTE - this draws the pieces
    
def drawBoard(screen):
    global colors
    colors =[p.Color("white"),p.Color(60,60,60)]
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQUARE_SIZE,r*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            
def drawPieces(screen,board):
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQUARE_SIZE,r*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
    
def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected !=():
        r,c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
            s = p.Surface((SQUARE_SIZE,SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s,(c * SQUARE_SIZE,r * SQUARE_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startColumn == c:
                    screen.blit(s,(SQUARE_SIZE * move.endColumn,SQUARE_SIZE * move.endRow))
            if len(gs.move_log)!=0:
                s.fill(p.Color("red"))
                screen.blit(s,(SQUARE_SIZE * gs.move_log[-1].endColumn,SQUARE_SIZE *gs.move_log[-1].endRow))
                
def animateMoves(move,screen,board,clock):
    global colors
    dR= move.endRow - move.startRow
    dC= move.endColumn - move.startColumn
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r,c =(move.startRow + dR * frame /frameCount,move.startColumn + dC * frame /frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        color = colors[(move.endRow + move.endColumn)%2]
        endSquare = p.Rect(move.endColumn * SQUARE_SIZE, move.endRow * SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE)
        p.draw.rect(screen,color,endSquare)
        if move.capturedPiece != "--":
            screen.blit(IMAGES[move.capturedPiece],endSquare)
        screen.blit(IMAGES[move.movedPiece],p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)
        
if __name__=='__main__':
    main()