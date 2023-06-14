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
            elif e.type == p.MOUSEBUTTONDOWN: #SECTION - onclick
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
                    if move in validMoves:
                        print(move.getChessNotation(gs))
                        gs.make_move(move)
                        moveMade = True
                        sqSelected= ()
                        playerClicks= []
                    else:
                        playerClicks= [sqSelected]
                    
        if moveMade:
            validMoves=gs.getLegalMoves()
            moveMade=False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
        
#SECTION - graphics
def drawGameState(screen ,gs): 
    drawBoard(screen) #NOTE - this draws the squares
    #TODO - add highlighting or suggestion later
    drawPieces(screen,gs.board)#NOTE - this draws the pieces
    
def drawBoard(screen):
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
    
    
    
    
                
if __name__=='__main__':
    main()