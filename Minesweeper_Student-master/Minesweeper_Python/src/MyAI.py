# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.lastX = startX
		self.lastY = startY

		self.board = [['?' for _ in range(colDimension)] for _ in range(rowDimension)]
		self.mines_remaining = totalMines
		self.actionQueue = []

		

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def printBoard(self) -> None:
		# Only for testing and debugging purposes
		print("=" * self.rowDimension)
		for row in self.board:
			print(' '.join(row))
		print("=" * self.rowDimension)
	
	def getNeighborsOfType(self, row: int, col: int, type: str):
		# Directions to check: up, down, left, right, and diagonals
		directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
		neighbors = []
        
		for dir_row, dir_col in directions:
			r, c = row + dir_row, col + dir_col
			if 0 <= r < self.rowDimension and 0 <= c < self.colDimension and self.board[r][c] == type:
				neighbors.append((c, self.rowDimension-r-1))
			
		return neighbors
	
	def confirm_121_pattern(self, row: int, col: int):
		if row+1 < self.rowDimension and row-1 >= 0 and self.board[row-1][col] == '1' and self.board[row+1][col] == '1':
			if col+1 < self.colDimension and self.board[row+1][col+1] == '?' and self.board[row][col+1] == '?' and self.board[row-1][col+1] == '?':
				if not (col-1 >= 0 and self.board[row][col-1] == '?'):
					self.board[row+1][col+1] = 'F'
					self.board[row-1][col+1] = 'F'
					self.actionQueue.append(Action(AI.Action.UNCOVER, col+1, self.rowDimension-row-1))

		return 0

	
	def runQueuedActions(self):
		action = self.actionQueue.pop(0)
		self.lastX = action.getX()
		self.lastY = action.getY()
		return action

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		print(self.rowDimension)
		print(self.colDimension)
		print(self.totalMines)
		print(self.lastX)
		print(self.lastY)
		print(self.board)
		print(self.mines_remaining)
		print(self.actionQueue)
		# FOR DEBUGGING
		if number == -1:
			number = 'F'
		
		# update board with number
		self.board[self.rowDimension-1-self.lastY][self.lastX] = str(number)

		if self.actionQueue:
			print('is this ran')
			return self.runQueuedActions()

		# First we will uncover covered neigbours to '0'
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == '0' and len(self.getNeighborsOfType(row, col, '?')) > 0:
					print("########")
					print(self.getNeighborsOfType(row, col, '?'))
					print("########")
					self.lastX, self.lastY = self.getNeighborsOfType(row, col, '?')[0]
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)
				
		# from now on we will always first check if a tile has any covered neighbours to speed up search
		# Second we will flag neigbours to tiles with amount of covered tiles neighbouring equal to its number
		# MARKING BOMBS
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] != '?' and self.board[row][col] != '0' and len(self.getNeighborsOfType(row, col, '?')) > 0 and self.board[row][col] == str(len(self.getNeighborsOfType(row, col, '?')) + len(self.getNeighborsOfType(row, col, 'F'))):
					# FOR OPTIMIZATION
					bombs = self.getNeighborsOfType(row, col, '?')
					for bomb in bombs:
						x, y = bomb
						self.board[self.rowDimension-1-y][x] = 'F'
					
					# FOR DEBUG
					# self.lastX, self.lastY = self.getNeighborsOfType(row, col, '?')[0]
					# return Action(AI.Action.FLAG, self.lastX, self.lastY)
				
		# Third, if number of flags (marked with F) is same as tile's number, we'll uncover all its neigbours
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == str(len(self.getNeighborsOfType(row, col, 'F'))) and len(self.getNeighborsOfType(row, col, '?')) > 0:
					self.lastX, self.lastY = self.getNeighborsOfType(row, col, '?')[0]
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)
		"""
		# Fourth, 1-2-1 pattern
		print("got to fourth")
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				# Not sure if these extra conditions are neccessary (they are only here to make it more efficient)
				if self.board[row][col] == '2' and len(self.getNeighborsOfType(row, col, '1')) >= 2 and len(self.getNeighborsOfType(row, col, '?')) == 3:
					self.confirm_121_pattern(row, col)

		if self.actionQueue:
			return self.runQueuedActions()
		"""
		


		# Fifth, 1-2-2-1 pattern

		
		# need to work on 3-4-3 pattern for expert worlds here
		
		
		# If the puzzle still hasn't been completed to this point, we'll start doing some probability and guessing
		# For now, I'm just choosing any first random tile xd
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == '?':
					self.lastX, self.lastY = col, self.rowDimension-row-1
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)


		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
