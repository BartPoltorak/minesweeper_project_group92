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

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	
	def printBoard(self) -> None:
		# Only for testing and debugging purposes
		print("=" * self.rowDimension)
		for row in self.board:
			print(' '.join(row))
		print("=" * self.rowDimension)


	def countNeighborsOfType(self, row: int, col: int, type: str):
		# Directions to check: up, down, left, right, and diagonals
		directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
		neighbor_count = 0
        
		for dir_row, dir_col in directions:
			r, c = row + dir_row, col + dir_col
			if 0 <= r < self.rowDimension and 0 <= c < self.colDimension and self.board[r][c] == type:
				neighbor_count += 1
        
		return neighbor_count
	
	def getFirstNeighborOfType(self, row: int, col: int, type: str):
		# Directions to check: up, down, left, right, and diagonals
		directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
		for dir_row, dir_col in directions:
			r, c = row + dir_row, col + dir_col
			if 0 <= r < self.rowDimension and 0 <= c < self.colDimension and self.board[r][c] == type:
				return c, self.colDimension-r-1
			
		return -1, -1
	
	def getNeighborsOfType(self, row: int, col: int, type: str):
		# Directions to check: up, down, left, right, and diagonals
		directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
		neighbors = []
        
		for dir_row, dir_col in directions:
			r, c = row + dir_row, col + dir_col
			if 0 <= r < self.rowDimension and 0 <= c < self.colDimension and self.board[r][c] == type:
				neighbors.append((c, self.colDimension-r-1))
			
		return neighbors
	

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		# update board with number
		self.board[self.colDimension-1-self.lastY][self.lastX] = str(number)

		# First we will uncover covered neigbours to '0'
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == '0' and self.countNeighborsOfType(row, col, '?') > 0:
					self.lastX, self.lastY = self.getFirstNeighborOfType(row, col, '?')
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)
				
		# from now on we will always first check if a tile has any covered neighbours to speed up search
		# Second we will flag neigbours to tiles with amount of covered tiles neighbouring equal to its number
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.countNeighborsOfType(row, col, '?') > 0 and self.board[row][col] == str(self.countNeighborsOfType(row, col, '?') + self.countNeighborsOfType(row, col, 'F')):
					bombs = self.getNeighborsOfType(row, col, '?')
					for bomb in bombs:
						x, y = bomb
						self.board[self.colDimension-1-y][x] = 'F'
					
					# self.lastX, self.lastY = self.getFirstNeighborOfType(row, col, '?')
					# return Action(AI.Action.FLAG, self.lastX, self.lastY)
				
		# Third, if number of flags (marked with number = -1) is same as tile's number, we'll uncover all its neigbours
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.countNeighborsOfType(row, col, '?') > 0 and self.board[row][col] == str(self.countNeighborsOfType(row, col, 'F')):
					self.lastX, self.lastY = self.getFirstNeighborOfType(row, col, '?')
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)
				
		# If the puzzle still hasn't been completed to this point, we'll start doing some probability and guessing
		# For now, I'm just choosing any first random tile xd
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == '?':
					self.lastX, self.lastY = row, col
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)


		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
