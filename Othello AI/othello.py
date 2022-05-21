#Library import
from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy

#Global Variables 
DEPTH = 4
MOVES = 0
AI_SCORE = 0
HUMAN_SCORE = 0


#GUI setup
root = Tk()
window = Canvas(root, width=500, height=600, background="#43c466")
root.maxsize(500,600)
root.minsize(500,600)
window.pack()

#Board Setup 

class othelloBoard:
    def __init__(self):
        #Black goes first (0 is White and Human player,1 is Black and computer(AI agent))
        self.player = 0
        self.won = False
        self.passed = False

        #Initializing an empty board of size 8*8
        self.board = []
        for x in range(8):
            self.board.append([])
            for y in range(8):
            	self.board[x].append(None)

        #Initializing center values
        self.board[3][3]="w"
        self.board[3][4]="b"    
        self.board[4][3]="b"
        self.board[4][4]="w"

        self.oldboard = self.board
       
    def updateBoard(self):
        window.delete("highlight")
        window.delete("tile")
        for x in range(8):
            for y in range(8):
                if self.oldboard[x][y]=="w":
                	window.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
                	window.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")
                
                elif self.oldboard[x][y]=="b":
                	window.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
                	window.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		
        
        window.update()
        for x in range(8):
            for y in range(8):
                if self.board[x][y]!=self.oldboard[x][y] and self.board[x][y]=="w":
                    window.delete("{0}-{1}".format(x,y))
					#Animation of discs 
                    for i in range(21):
                        window.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                        window.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                        sleep(0.005)
                        window.update()
                        window.delete("animated")
                    for i in reversed(range(21)):
                        window.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                        window.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                        sleep(0.005)
                        window.update()
                        window.delete("animated")
                    window.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
                    window.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
                    window.update()

                elif self.board[x][y]!=self.oldboard[x][y] and self.board[x][y]=="b":
                    window.delete("{0}-{1}".format(x,y))
					#Animation of discs 
                    for i in range(21):
                        window.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                        window.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                        sleep(0.005)
                        window.update()
                        window.delete("animated")
                    for i in reversed(range(21)):
                        window.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                        window.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                        sleep(0.005)
                        window.update()
                        window.delete("animated")
                        
                    window.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
                    window.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
                    window.update()

		#Showing valid moves to HUMAN player
        for x in range(8):
            for y in range(8):
                if self.player == 0:
                    if valid(self.board,self.player,x,y):
                        window.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#ffd39b",outline="#ffd39b")

        if not self.won:
            self.drawScoreBoard()
            window.update()
            if self.player == 1:
                self.oldboard = self.board
                alphaBetaResult = self.alphaBeta(self.board, DEPTH, -float("inf"), float("inf"), 1)
                self.board = alphaBetaResult[1]

                if len(alphaBetaResult) == 3:
                    position = alphaBetaResult[2]
                    self.oldboard[position[0]][position[1]] = "b"

                self.player = 1 - self.player
                sleep(1.3)
                self.passTest()
        else:
            if self.AI_SCORE < self.HUMAN_SCORE:
                window.create_text(250, 550, anchor="c", font=("Consolas", 15),
                                   text="You Won, with " + str(abs(self.AI_SCORE - self.HUMAN_SCORE)) + " Points!")
            elif self.AI_SCORE > self.HUMAN_SCORE:
                window.create_text(250, 550, anchor="c", font=("Consolas", 15),
                                   text="AI Won, with " + str(abs(self.AI_SCORE - self.HUMAN_SCORE)) + " Points!")

    # Moving board position
    def boardMove(self, x, y):
        self.oldboard = self.board
        self.oldboard[x][y] = "w"
        self.board = move(self.board, x, y)

        self.player = 1 - self.player
        self.updateBoard()

        self.passTest()
        self.updateBoard()

    # Test if player must pass: if they do, switch the player
    def passTest(self):
        mustPass = True
        for x in range(8):
            for y in range(8):
                if valid(self.board, self.player, x, y):
                    mustPass = False
        if mustPass:
            self.player = 1 - self.player
            if self.passed == True:
                self.won = True
            else:
                self.passed = True
            self.updateBoard()
        else:
            self.passed = False

    # AlphaBeta pruning on the minimax tree
    def alphaBeta(self, node, depth, alpha, beta, maximizing):
        boards = []
        choices = []

        for x in range(8):
            for y in range(8):
                if valid(self.board, self.player, x, y):
                    test = move(node, x, y)
                    boards.append(test)
                    choices.append([x, y])

        if depth == 0 or len(choices) == 0:
            return ([finalHeuristic(node, maximizing), node])

        if maximizing:
            v = -float("inf")
            bestBoard = []
            bestChoice = []
            for board in boards:
                boardValue = self.alphaBeta(board, depth - 1, alpha, beta, 0)[0]
                if boardValue > v:
                    v = boardValue
                    bestBoard = board
                    bestChoice = choices[boards.index(board)]
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return ([v, bestBoard, bestChoice])
        else:
            v = float("inf")
            bestBoard = []
            bestChoice = []
            for board in boards:
                boardValue = self.alphaBeta(board, depth - 1, alpha, beta, 1)[0]
                if boardValue < v:
                    v = boardValue
                    bestBoard = board
                    bestChoice = choices[boards.index(board)]
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return ([v, bestBoard, bestChoice])

    # Displaying scoreBoard on window
    def drawScoreBoard(self):
        global MOVES
        window.delete("score")
        player_score = 0
        computer_score = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == "w":
                    player_score += 1
                elif self.board[x][y] == "b":
                    computer_score += 1

        if self.player == 0:
            player_colour = "red"
            computer_colour = "gray"
        else:
            player_colour = "gray"
            computer_colour = "red"

        window.create_oval(30, 540, 50, 560, fill=player_colour, outline=player_colour)
        window.create_oval(400, 540, 420, 560, fill=computer_colour, outline=computer_colour)
        window.create_text(50, 550, anchor="w", tags="score", font=("Consolas", 35), fill="white", text=player_score)
        window.create_text(420, 550, anchor="w", tags="score", font=("Consolas", 35), fill="black", text=computer_score)

        MOVES = player_score + computer_score
        self.AI_SCORE = computer_score
        self.HUMAN_SCORE = player_score

# Checks if a move is valid for a given board.
def valid(board, player, x, y):
    if player == 0:
        colour = "w"
    else:
        colour = "b"

    if board[x][y] != None:
        return False

    else:
        neighbour = False
        neighbours = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if board[i][j] != None:
                    neighbour = True
                    neighbours.append([i, j])
        
        if not neighbour:
            return False
        else:
            valid = False
            for neighbour in neighbours:

                neighX = neighbour[0]
                neighY = neighbour[1]

                if board[neighX][neighY] == colour:
                    continue
                else:
                    deltaX = neighX - x
                    deltaY = neighY - y
                    tempX = neighX
                    tempY = neighY

                    while 0 <= tempX <= 7 and 0 <= tempY <= 7:
                        if board[tempX][tempY] == None:
                            break

                        if board[tempX][tempY] == colour:
                            valid = True
                            break
                        
                        tempX += deltaX
                        tempY += deltaY
            return valid


# Making valid move
def move(passedArray, x, y):
    array = deepcopy(passedArray)
    if board.player == 0:
        colour = "w"
    else:
        colour = "b"
    array[x][y] = colour

    neighbours = []
    for i in range(max(0, x - 1), min(x + 2, 8)):
        for j in range(max(0, y - 1), min(y + 2, 8)):
            if array[i][j] != None:
                neighbours.append([i, j])

    convert = []

    for neighbour in neighbours:
        neighX = neighbour[0]
        neighY = neighbour[1]
        if array[neighX][neighY] != colour:
            path = []
            
            deltaX = neighX - x
            deltaY = neighY - y

            tempX = neighX
            tempY = neighY

            while 0 <= tempX <= 7 and 0 <= tempY <= 7:
                path.append([tempX, tempY])
                value = array[tempX][tempY]
                if value == None:
                    break
                if value == colour:
                    for node in path:
                        convert.append(node)
                    break
                
                tempX += deltaX
                tempY += deltaY

    for node in convert:
        array[node[0]][node[1]] = colour

    return array

# Simple heuristic
def simpleHeuristicScore(array,player):
	score = 0
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"

	for x in range(8):
		for y in range(8):
			if array[x][y]==colour:
				score+=1
			elif array[x][y]==opponent:
				score-=1
	return score

# Slightly Less simple Heuristic
def HeuristicScore(array,player):
	score = 0
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	for x in range(8):
		for y in range(8):
			add = 1
			#Edge discs
			if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=3
			#Corner discs
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = 5
			
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score


# Decent Heuristic
def decentHeuristic(array, player):
    score = 0
    cornerVal = 25
    adjacentVal = 5
    sideVal = 5

    if player == 1:  
        colour = "b"
        opponent = "w"
    else:  
        colour = "w"
        opponent = "b"
    
    for x in range(8):
        for y in range(8):
            add = 1

            # Adjacent to corners
            if (x == 0 and y == 1) or (x == 1 and 0 <= y <= 1):
                if array[0][0] == colour:
                    add = sideVal
                else:
                    add = -adjacentVal

            elif (x == 0 and y == 6) or (x == 1 and 6 <= y <= 7):
                if array[7][0] == colour:
                    add = sideVal
                else:
                    add = -adjacentVal

            elif (x == 7 and y == 1) or (x == 6 and 0 <= y <= 1):
                if array[0][7] == colour:
                    add = sideVal
                else:
                    add = -adjacentVal

            elif (x == 7 and y == 6) or (x == 6 and 6 <= y <= 7):
                if array[7][7] == colour:
                    add = sideVal
                else:
                    add = -adjacentVal


            # Edge discs
            elif (x == 0 and 1 < y < 6) or (x == 7 and 1 < y < 6) or (y == 0 and 1 < x < 6) or (y == 7 and 1 < x < 6):
                add = sideVal
            
            # Corners discs
            elif (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                add = cornerVal

            if array[x][y] == colour:
                score += add
            elif array[x][y] == opponent:
                score -= add
    return score


# Final Heuristic
def finalHeuristic(array,player):
	if MOVES<=8:
		numMoves = 0
		for x in range(8):
			for y in range(8):
				if valid(array,player,x,y):
					numMoves += 1
		return numMoves+decentHeuristic(array,player)
	elif MOVES<=52:
		return decentHeuristic(array,player)
	elif MOVES<=58:
		return HeuristicScore(array,player)
	else:
		return simpleHeuristicScore(array,player)

# Drawing Lines
def drawGridBackground(outline=False):
    if outline:
        window.create_rectangle(50,50,450,450,outline="#111")
    for i in range(-1, 8):
        lineShift = 50+50*(i+1)
        window.create_line(50,lineShift,450,lineShift,fill="#111",width=1.5)
        window.create_line(lineShift,50,lineShift,450,fill="#111",width=1.5)
    window.update()

# When the user clicks, if it's a valid move, make the move
def clickHandle(event):
	global DEPTH
	xMouse = event.x
	yMouse = event.y
	if running:
		if xMouse>=450 and yMouse<=50:
			root.destroy()
		elif xMouse<=50 and yMouse<=50:
			playGame()
		else:
			if board.player==0:
				x = int((event.x-50)/50)
				y = int((event.y-50)/50)

				if 0<=x<=7 and 0<=y<=7:
					if valid(board.board,board.player,x,y):
						board.boardMove(x,y)
def create_buttons():
    window.create_arc(5,5,30,30,fill="#000088", width="2",style="arc",outline="white",extent=300)
    window.create_polygon(20,25,23,32,27,26,fill="white",outline="white")
		

def playGame():
	global board, running
	running = True
	window.delete(ALL)
	create_buttons()
	board = 0
	drawGridBackground()
	board = othelloBoard()
	board.updateBoard()


playGame()
window.bind("<Button-1>", clickHandle)
window.focus_set()
root.wm_title("Othello")
root.mainloop()