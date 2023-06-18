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
        self.blackKingLocation=(0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate=False
        self.staleMate=False
        self.enPassantPossible =()
        self.enPassantPossibleLog=[]
        self.notationLog=[]
        self.currentCastlingRights = CastlingRights(True,True,True,True)
        self.CastlingRightsLog = [CastlingRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,self.currentCastlingRights.wqs,self.currentCastlingRights.bqs)]
    def promptUser(self,question):
        return input(question)
    def make_move(self,move,isAI=False):
        if move.movedPiece== "wK":
            self.whiteKingLocation= (move.endRow, move.endColumn)
        if move.movedPiece== "bK":
            self.blackKingLocation= (move.endRow, move.endColumn) 
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.movedPiece
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        
        if move.isPromotion:
            if not isAI:
                move.promotionPiece=self.promptUser("choose promotion piece: ").upper()
                if move.promotionPiece not in ["R","N","Q","B"]:
                    move.promotionPiece=self.promptUser("invalid piece choose an other promotion piece: ").upper()   #SECTION - promotion 
            self.board[move.endRow][move.endColumn] = move.movedPiece[0]+move.promotionPiece
            
        if move.isCastling:
            if move.endColumn-move.startColumn==2:
                self.board[move.endRow][move.endColumn-1]=self.board[move.endRow][move.endColumn+1]
                self.board[move.endRow][move.endColumn+1]="--"
            else:
                self.board[move.endRow][move.endColumn+1]=self.board[move.endRow][move.endColumn-2]
                self.board[move.endRow][move.endColumn-2]="--" 
        
        if move.isEnpassant:
            self.board[move.startRow][move.endColumn] ="--"
            
        if move.movedPiece[1] == "p" and abs(move.startRow - move.endRow)==2:
            self.enPassantPossible=((move.endRow + move.startRow)//2,move.endColumn)    #SECTION - en passant 
            self.enPassantPossibleLog.append(self.enPassantPossible)
        else:
            self.enPassantPossible=()
            self.enPassantPossibleLog.append(self.enPassantPossible)
            
        if move.movedPiece == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.movedPiece == "bK":               #
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.movedPiece == "wR":
            if move.startRow==7:
                if move.startColumn==0:
                    self.currentCastlingRights.wqs = False          #SECTION - castling rights
                elif move.startColumn==7:
                    self.currentCastlingRights.wks = False
        elif move.movedPiece == "bR":
            if move.startRow==0:
                if move.startColumn==0:
                    self.currentCastlingRights.bqs = False
                elif move.startColumn==7:
                    self.currentCastlingRights.bks = False
                    
        self.notationLog.append(move.getChessNotation(self))
        self.CastlingRightsLog.append(CastlingRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,self.currentCastlingRights.wqs,self.currentCastlingRights.bqs))
    def undo_move(self):
        if len(self.move_log)==0:
            return
        if self.move_log[-1].movedPiece== "wK":
            self.whiteKingLocation= (self.move_log[-1].startRow, self.move_log[-1].startColumn)
        if self.move_log[-1].movedPiece== "bK":
            self.blackKingLocation= (self.move_log[-1].startRow, self.move_log[-1].startColumn)
        move=self.move_log.pop()
        self.board[move.endRow][move.endColumn] = move.capturedPiece
        self.board[move.startRow][move.startColumn] = move.movedPiece
        self.white_to_move = not self.white_to_move
        
        if move.isPromotion:
            self.board[move.startRow][move.startColumn] = move.movedPiece[0]+"p"
            
        if move.isCastling:
            if move.endColumn-move.startColumn==2:
                self.board[move.endRow][move.endColumn+1]=self.board[move.endRow][move.endColumn-1]
                self.board[move.endRow][move.endColumn-1]="--"
            else:
                self.board[move.endRow][move.endColumn-2]=self.board[move.endRow][move.endColumn+1]
                self.board[move.endRow][move.endColumn+1]="--" 
        
        if move.isEnpassant:
            self.board[move.endRow][move.endColumn] ="--"
            self.board[move.startRow][move.endColumn] = "wp" if not self.white_to_move else "bp"
            self.enPassantPossible=(move.endRow,move.endColumn)
            self.enPassantPossibleLog.append(self.enPassantPossible)
        if move.movedPiece[1]=="p"  and abs(move.startRow-move.endRow) == 2:
            self.enPassantPossible=()
            
        self.CastlingRightsLog.pop()
        self.enPassantPossibleLog.pop()
        self.enPassantPossible= self.enPassantPossibleLog[-1]
        self.currentCastlingRights=self.CastlingRightsLog[-1]
        self.notationLog.pop()
        self.checkMate,self.staleMate=False,False
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
        piecePinned = False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
            
        if self.white_to_move:
            if self.board[r-1][c] =="--":
                if not piecePinned or pinDirection==(-1,0):
                    moves.append(Move((r,c),(r-1,c),self))
                    if r ==6 and self.board[r-2][c]=="--":
                        moves.append(Move((r,c),(r-2,c),self))
            if c-1 >= 0:
                if self.board[r-1][c-1][0]== "b":
                    if not piecePinned or pinDirection==(-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self))
                elif self.enPassantPossible == (r-1,c-1):
                    if not piecePinned or pinDirection==(-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self,isEnpassant=True))
            if c+1<=7:
                if self.board[r-1][c+1][0]== "b":
                    if not piecePinned or pinDirection==(-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self))
                elif self.enPassantPossible == (r-1,c+1):
                    if not piecePinned or pinDirection==(-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self,isEnpassant=True))                   
        else:
            if not piecePinned or pinDirection==(1,0):
                if self.board[r+1][c] =="--":
                    moves.append(Move((r,c),(r+1,c),self))
                    if  r == 1 and self.board[r+2][c]=="--":
                        moves.append(Move((r,c),(r+2,c),self))
            if c-1 >= 0:
                if self.board[r+1][c-1][0]== "w":
                    if not piecePinned or pinDirection==(1,-1):
                        moves.append(Move((r,c),(r+1,c-1),self))
                elif self.enPassantPossible == (r-1,c-1):
                    if not piecePinned or pinDirection==(1,-1):
                        moves.append(Move((r,c),(r+1,c-1),self,isEnpassant=True))
            if c+1<=7:
                if self.board[r+1][c+1][0]== "w":
                    if not piecePinned or pinDirection==(1,1):
                        moves.append(Move((r,c),(r+1,c+1),self))
                elif self.enPassantPossible == (r+1,c+1):
                    if not piecePinned or pinDirection==(1,1):
                        moves.append(Move((r,c),(r+1,c+1),self,isEnpassant=True))               
    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        if not piecePinned:
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
        piecePinned = False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directons =[(-1,-1),(-1,1),(1,-1),(1,1)]
        enemyColor = "b" if self.white_to_move else "w"
        for d in directons:
            for i in range(1,8):
                endRow = r + d[0] *i
                endCol = c + d[1] *i
                if 0 <= endRow <8 and 0<= endCol<8:
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],d[1]):
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
        rowMoves = [-1,-1,-1,0,0,1,1,1]
        colMoves = [-1,0,1,-1,1,-1,0,1]
        allyColor = "w" if self.white_to_move else "b"
        for i in range(8):
            endRow= r+ rowMoves[i]
            endCol= c + colMoves[i]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    if allyColor=="w":
                        self.whiteKingLocation = (endRow,endCol)
                    else:
                        self.blackKingLocation = (endRow,endCol)
                    inCheck,pins,checks = self.checkforChecksAndPins()
                    if not inCheck:
                        moves.append(Move((r,c),(endRow,endCol),self))
                    if allyColor=="w":
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)
        self.getCastlingMoves(r,c,moves,allyColor)
    def getCastlingMoves(self,r,c,moves,allyColor):
        if self.inCheck:
            return
        if (allyColor=="w" and self.currentCastlingRights.wks) or (allyColor=="b" and self.currentCastlingRights.bks):
            self.getKSCastlingMoves(r,c,moves,allyColor)
        if (allyColor=="w" and self.currentCastlingRights.wqs) or (allyColor=="b" and self.currentCastlingRights.bqs):
            self.getQSCastlingMoves(r,c,moves,allyColor)           
    def getKSCastlingMoves(self,r,c,moves,allyColor):
        if self.board[r][c+1] == "--" and self.board[r][c+2]=="--" and self.board[r][c+3][1] == "R":
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self,isCastling=True))
    def getQSCastlingMoves(self,r,c,moves,allyColor):
        if self.board[r][c-1] == "--" and self.board[r][c-2]=="--" and self.board[r][c-3] == "--" and self.board[r][c-4][1] == "R":
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self,isCastling=True))
    def squareUnderAttack(self,r,c):
        if self.white_to_move:
            enemyColor="b"
            allyColor="w"
            startRow=r
            startCol=c
        else:
            enemyColor="w"
            allyColor="b"
            startRow=r
            startCol=c
        directions=((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d=directions[j]
            for i in range(1,8):
                endRow= startRow+d[0]*i
                endCol= startCol+d[1] *i
                if 0<=endRow <8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece[0] ==allyColor and endPiece[1] != "K":
                            break
                    elif endPiece[0] == enemyColor:
                        type =endPiece[1]
                        if (0<=j<=3 and type== "R") or (4<=j<=7 and type== "B")or \
                            (i==1 and type== "p" and((enemyColor=="w" and 6<=j<=7)or(enemyColor=="b" and 4<=j<=5))or \
                            (type=="Q")or(i==1 and type=="K")):
                                return True
                        else:
                            break
                else:
                    break
        knightMoves=((-2,-1),(-1,-2),(1,-2),(-1,2),(2,-1),(-2,1),(1,2),(2,1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0]== enemyColor and endPiece[1]== "N":
                    return True
        return False
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)
    def getRookMoves(self,r,c,moves):
        piecePinned = False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] !="Q":
                    self.pins.remove(self.pins[i])
                break
        directons =[(-1,0),(0,-1),(1,0),(0,1)]
        enemyColor = "b" if self.white_to_move else "w"
        for d in directons:
            for i in range(1,8):
                endRow = r + d[0] *i
                endCol = c + d[1] *i
                if 0 <= endRow <8 and 0<= endCol<8:
                    if not piecePinned or pinDirection==d or pinDirection== (-d[0],-d[1]):
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
    def getLegalMoves(self):
        moves=[]
        self.inCheck,self.pins,self.checks=self.checkforChecksAndPins()
        if self.white_to_move:
            KingRow=self.whiteKingLocation[0]
            KingCol=self.whiteKingLocation[1]
        else:
            KingRow=self.blackKingLocation[0]
            KingCol=self.blackKingLocation[1]
        if self.inCheck:#SECTION - check situation valid moves
            if len(self.checks)==1:#NOTE - to sefrentiate check and double check logic
                moves=self.getPossibleMoves()
                check=self.checks[0]
                checkRow=check[0]
                checkCol=check[1]
                checkingPeice = self.board[checkRow][checkCol]
                validSquares=[]
                if checkingPeice[1]=="N":
                    validSquares=[(checkRow,checkCol)]
                else:
                    for i in range(1,8): #REVIEW - this generates where can a piece move in order to block the check
                        validSquare=(KingRow+check[2]*i,KingCol+check[3]*i)
                        validSquares.append(validSquare)
                        if  validSquare[0]==checkRow and validSquare[1]==checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].movedPiece[1]!="K":#REVIEW - validating if a certain non piece move blocks the check
                        if not (moves[i].endRow,moves[i].endColumn)in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(KingRow,KingCol,moves)
        else:
            moves=self.getPossibleMoves()
        return moves
    def checkforChecksAndPins(self):
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
                    if endPiece[0] ==allyColor and endPiece[1] != "K":
                        if possiblePin==():
                            possiblePin=(endRow,endCol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type =endPiece[1]
                        if (0<=j<=3 and type== "R") or (4<=j<=7 and type== "B")or \
                            (i==1 and type== "p" and((enemyColor=="w" and 6<=j<=7)or(enemyColor=="b" and 4<=j<=5))or \
                            (type=="Q")or(i==1 and type=="K")):
                                if possiblePin ==():
                                    inCheck=True
                                    checks.append((endRow,endCol,d[0],d[1]))
                                    break
                                else:
                                    pins.append(possiblePin)
                                    break
                        else:
                            break
                else:
                    break
        knightMoves=((-2,-1),(-1,-2),(1,-2),(-1,2),(2,-1),(-2,1),(1,2),(2,1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0]== enemyColor and endPiece[1]== "N":
                    inCheck = True
                    checks.append((endRow, endCol,m[0],m[1]))
        return inCheck,pins,checks
    
class Move():
    rankToRow={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowToRank={v:k for k,v in rankToRow.items()}
    fileToCol={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colToFile={v:k for k,v in fileToCol.items()}
    
    def __init__(self,start,end,gs,isEnpassant=False,isCastling=False):
        self.startRow = start[0]
        self.endRow = end[0]
        self.startColumn = start[1]
        self.endColumn = end[1]
        self.capturedPiece= gs.board[self.endRow][self.endColumn]
        self.movedPiece=gs.board[self.startRow][self.startColumn]
        self.promotionPiece = "Q"
        self.isPromotion=(self.movedPiece == "wp"and self.endRow==0)or(self.movedPiece == "bp"and self.endRow==7)
        self.isCastling=isCastling
        self.isEnpassant=isEnpassant
            
        
    def __eq__(self, other):
        if isinstance(other,Move):
            if self.startRow == other.startRow and self.startColumn == other.startColumn and self.endColumn == other.endColumn and self.endRow == other.endRow :
                return True
        return False
        
        
    def getChessNotation(self,gs):
        if len(gs.getLegalMoves())==0:
            if gs.inCheck:
                gs.checkMate=True
            else:
                gs.staleMate=True
        if self.movedPiece =="wK"or self.movedPiece == "bK":
            pieceName ="K"
            if self.isCastling:
                if self.endColumn-self.startColumn == 2:
                    return"O-O"
                else:
                    return"O-O-O"
        elif self.movedPiece =="wQ"or self.movedPiece == "bQ":
            pieceName = "Q"
        elif self.movedPiece =="wN"or self.movedPiece == "bN":              #SECTION - piece notation
            pieceName ="N"
        elif self.movedPiece =="wB"or self.movedPiece == "bB":
            pieceName = "B"
        elif self.movedPiece =="wR"or self.movedPiece == "bR":
            pieceName = "R"
            
            
        if self.capturedPiece != "--" or self.isEnpassant: #SECTION - capture logic
            if self.movedPiece =="wp"or self.movedPiece == "bp":
                if self.isPromotion:
                    if gs.checkMate:
                        return self.colToFile[self.startColumn]+"x"+self.getRankFile(self.endRow, self.endColumn)+"="+self.promotionPiece+"#"
                    if gs.inCheck:
                        return self.colToFile[self.startColumn]+"x"+self.getRankFile(self.endRow, self.endColumn)+"="+self.promotionPiece+"+"
                    return self.colToFile[self.startColumn]+"x"+self.getRankFile(self.endRow, self.endColumn)+"="+self.promotionPiece
                if gs.checkMate:
                    return self.colToFile[self.startColumn]+"x"+self.getRankFile(self.endRow, self.endColumn)+"#"
                if gs.inCheck:
                    return self.colToFile[self.startColumn]+"x"+self.getRankFile(self.endRow, self.endColumn)+"+"
                return self.colToFile[self.startColumn]+"x"+self.getRankFile(self.endRow, self.endColumn)
            pieceName = pieceName+"x"
            
            
        if self.movedPiece =="wp"or self.movedPiece == "bp": #NOTE - pawn moves are notated deferently
            if self.isPromotion:
                if gs.checkMate:
                    return self.getRankFile(self.endRow, self.endColumn)+"="+self.promotionPiece+"#"
                if gs.inCheck:
                    return self.getRankFile(self.endRow, self.endColumn)+"="+self.promotionPiece+"+"
                return self.getRankFile(self.endRow, self.endColumn)+"="+self.promotionPiece
            if gs.checkMate:
                return self.getRankFile(self.endRow, self.endColumn)+"#"
            if gs.inCheck:
                return self.getRankFile(self.endRow, self.endColumn)+"+"
            return self.getRankFile(self.endRow, self.endColumn)
        
        if gs.checkMate:
            return pieceName+self.getRankFile(self.endRow, self.endColumn)+"#"
        if gs.inCheck:
            return pieceName+self.getRankFile(self.endRow, self.endColumn)+"+"     
            
        return pieceName+self.getRankFile(self.endRow, self.endColumn)

        
    def getRankFile(self,r,c):
        return self.colToFile[c] + self.rowToRank[r]
    
class CastlingRights(): 
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs