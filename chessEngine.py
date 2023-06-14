class GameState():
    def __init__(self):
        self.board =[["bR","bN","bB","bQ","bK","bB","bN","bR"],
                     ["bp","bp","bp","bp","bp","bp","bp","bp"],
                     ["--","--","--","--","--","--","--","--"],
                     ["--","--","--","--","--","--","--","--"],
                     ["--","--","--","--","--","--","--","--"],
                     ["--","--","--","--","--","--","--","--"],
                     ["wp","wp","wp","wp","wp","wp","wp","wp"],
                     ["wR","wN","wB","wQ","wK","wB","wN","wR"],]
        self.white_to_move= True
        self.move_log = []
        self.whiteKingLocation=(7,4)
        self.blackkingLocation=(0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate=False
        self.staleMate=False             
    def make_move(self,move):
        if move.movedPiece== "wK":
            self.whiteKingLocation= (move.endRow, move.endColumn)
        if move.movedPiece== "bK":
            self.blackKingLocation= (move.endRow, move.endColumn) 
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.movedPiece
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
    def undo_move(self):
        if len(self.move_log)==0:
            return
        move=self.move_log.pop()
        if move.movedPiece== "wK":
            self.whiteKingLocation= (move.startRow, move.startColumn)
        if move.movedPiece== "bK":
            self.blackKingLocation= (move.startRow, move.startColumn)        
        self.board[move.endRow][move.endColumn] = move.capturedPiece
        self.board[move.startRow][move.startColumn] = move.movedPiece
        self.white_to_move = not self.white_to_move
    def getPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn =="w" and self.white_to_move) or (turn=="b" and not self.white_to_move):
                    piece= self.board[r][c][1]
                    if piece =="p":
                        self.getPawnMoves(r,c,moves)
                    elif piece =="R":
                        self.getRookMoves(r,c,moves)
                    elif piece=="K":
                        self.getKingMoves(r,c,moves)
                    elif piece=="Q":
                        self.getQueenMoves(r,c,moves)
                    elif piece=="N":
                        self.getKnightMoves(r,c,moves)
                    elif piece=="B":
                        self.getBishopMoves(r,c,moves)
        return moves                   
    def getPawnMoves(self,r,c,moves):   
        if self.white_to_move:
            if self.board[r-1][c] =="--":
                moves.append(Move((r,c),(r-1,c),self))
                if r ==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self))
            if c-1 >= 0:
                if self.board[r-1][c-1][0]== "b":
                    moves.append(Move((r,c),(r-1,c-1),self))
            if c+1<=7:
                if self.board[r-1][c+1][0]== "b":
                    moves.append(Move((r,c),(r-1,c+1),self))
        if  not self.white_to_move:
            if self.board[r+1][c] =="--":
                moves.append(Move((r,c),(r+1,c),self))
                if  r == 1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self))
            if c-1 >= 0:
                if self.board[r+1][c-1][0]== "w":
                    moves.append(Move((r,c),(r+1,c-1),self))
            if c+1<=7:
                if self.board[r+1][c+1][0]== "w":
                    moves.append(Move((r,c),(r+1,c+1),self))                   
    def getKnightMoves(self,r,c,moves):
        if r-2>=0:
            if c-1>=0:
                if self.board[r-2][c-1]=="--"or self.board[r-2][c-1][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r-2,c-1),self))
            if c+1<=7:
                if self.board[r-2][c+1]=="--"or self.board[r-2][c+1][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r-2,c+1),self))
        if r-1>=0:
            if c-2>=0:
                if self.board[r-1][c-2]=="--"or self.board[r-1][c-2][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r-1,c-2),self))
            if c+2<=7:
                if self.board[r-1][c+2]=="--"or self.board[r-1][c+2][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r-1,c+2),self))
        if r+2<=7:
            if c-1>=0:
                if self.board[r+2][c-1]=="--"or self.board[r+2][c-1][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r+2,c-1),self))
            if c+1<=7:
                if self.board[r+2][c+1]=="--"or self.board[r+2][c+1][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r+2,c+1),self))
        if r+1<=7:
            if c-2>=0:
                if self.board[r+1][c-2]=="--"or self.board[r+1][c-2][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r+1,c-2),self))
            if c+2<=7:
                if self.board[r+1][c+2]=="--"or self.board[r+1][c+2][0]!=self.board[r][c][0]:
                    moves.append(Move((r,c),(r+1,c+2),self))
    def getBishopMoves(self,r,c,moves):
        directons =[(-1,-1),(-1,1),(1,-1),(1,1)]
        enemyColor = "b" if self.white_to_move else "w"
        for d in directons:
            for i in range(1,8):
                endRow = r + d[0] *i
                endCol = c + d[1] *i
                if 0 <= endRow <8 and 0<= endCol<8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self))
                        break
                    else:
                        break
                else:
                    break
    def getKingMoves(self,r,c,moves):
        adjSquares =[(-1,-1),(-1,0),(-1 ,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        allyColor = "w" if self.white_to_move else "b"
        for i in range(8):
            endRow= r+ adjSquares[i][0]
            endCol= c + adjSquares[i][1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self))
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)
    def getRookMoves(self,r,c,moves):
        directons =[(-1,0),(0,-1),(1,0),(0,1)]
        enemyColor = "b" if self.white_to_move else "w"
        for d in directons:
            for i in range(1,8):
                endRow = r + d[0] *i
                endCol = c + d[1] *i
                if 0 <= endRow <8 and 0<= endCol<8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self))
                        break
                    else:
                        break
                else:
                    break
    def inCheck(self):
        if self.white_to_move:
            return self.squareAttacked(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareAttacked(self.blackkingLocation[0],self.blackkingLocation[1])
    def getLegalMoves(self):
        moves=self.getPossibleMoves()
        for i in range(len(moves)-1,-1,-1):
            self.make_move(moves[i])
            self.white_to_move= not self.white_to_move
            if self.inCheck():
                moves.pop(i)
            self.white_to_move= not self.white_to_move
            self.undo_move() 
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.checkMate=False
            self.staleMate=False
            
        return moves
    def checkforChecksAndPins():
        inCheck = False
        pins = []
        checks = []
        if self.white_to_move:
            enemyColor="b"
            allyColor="w"
            startRow=self.whiteKingLocation[0]
            startCol=self.whiteKingLocation[1]
        else:
            enemyColor="w"
            allyColor="b"
            startRow=self.blackKingLocation[0]
            startCol=self.blackKingLocation[1]
        directions=((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d=directions[j]
            possiblePin=()
            for i in range(1,8):
                endRow= startRow+d[0]*i
                endCol= startCol+d[1] *i
                if 0<=endRow <8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece[0] ==allyColor:
                        if possiblePin==():
                            possiblePin=(endRow,endCol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type =endPiece[1]
                        if (0<=j<3 and type== R) or (0<=j<=7
    def squareAttacked(self,r,c):
        self.white_to_move= not self.white_to_move
        oppMoves=self.getPossibleMoves()
        self.white_to_move= not self.white_to_move
        for move in oppMoves:
            if move.endRow==r and move.endColumn==c:
                return True
        return False
class Move():
    #NOTE - fu**ing maps from
    rankToRow={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowToRank={v:k for k,v in rankToRow.items()}
    fileToCol={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colToFile={v:k for k,v in fileToCol.items()}
    
    def __init__(self,start,end,gs):
        self.startRow = start[0]
        self.endRow = end[0]
        self.startColumn = start[1]
        self.endColumn = end[1]
        self.capturedPiece= gs.board[self.endRow][self.endColumn]
        self.movedPiece=gs.board[self.startRow][self.startColumn]
        
    def __eq__(self, other):
        if isinstance(other,Move):
            if self.startRow == other.startRow and self.startColumn == other.startColumn and self.endColumn == other.endColumn and self.endRow == other.endRow :
                return True
        return False
        
        
    def getChessNotation(self,gs):
        #TODO - enhance this by adding check,promotion and mate notation
        if self.movedPiece =="wK"or self.movedPiece == "bK":
            pieceName ="k"
        elif self.movedPiece =="wQ"or self.movedPiece == "bQ":
            pieceName = "Q"
        elif self.movedPiece =="wN"or self.movedPiece == "bN":              #SECTION - piece notation
            pieceName ="N"
        elif self.movedPiece =="wB"or self.movedPiece == "bB":
            pieceName = "B"
        elif self.movedPiece =="wR"or self.movedPiece == "bR":
            pieceName = "R"
            
            
        if self.capturedPiece != "--": #SECTION - capture logic
            if self.movedPiece =="wp"or self.movedPiece == "bp":
                return self.colToFile[self.startColumn]+"x"+self.getRankFile(self.endRow, self.endColumn)
            pieceName = pieceName+"x"
            
            
        if self.movedPiece =="wp"or self.movedPiece == "bp": #NOTE - pawn moves are notated deferentially
            return self.getRankFile(self.endRow, self.endColumn)
            
        return pieceName+self.getRankFile(self.endRow, self.endColumn)

        
    def getRankFile(self,r,c):
        return self.colToFile[c] + self.rowToRank[r]