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

		self.debug = False
		self.strong_debug = False

		

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
	
	def find_pattern_121(self):
		# Helper function to check for the pattern in a line
		def check_line(line, start_index):
			for i in range(len(line) - 2):
				if line[i] == '1' and line[i+1] == '2' and line[i+2] == '1':
					return (start_index + i + 1)
			return None
		
		# Check rows
		for row_index, row in enumerate(self.board):
			col_index = check_line(row, 0)
			if col_index is not None:
				return (row_index, col_index, 'horizontal')
		
		# Check columns
		for col in range(self.colDimension):
			column = [self.board[row][col] for row in range(self.rowDimension)]
			row_index = check_line(column, 0)
			if row_index is not None:
				return (row_index, col, 'vertical')
		
		return None
	
	def check_121_pattern(self, row: int, col: int, orientation: str):
		if orientation == 'horizontal':
			# META: is this neccessary?
			# check if row+1 and row-1 are in bound
			# doesn't fit the pattern if there are '?' on both sides of 2
			if row+1 < self.rowDimension and row-1 >= 0 and self.board[row-1][col] == '?' and self.board[row+1][col] == '?':
				return None
			# check 'up'
			if row+1 < self.rowDimension and self.board[row+1][col] == '?' and self.board[row+1][col-1] == '?' and self.board[row+1][col+1] == '?':
				self.actionQueue.append(Action(AI.Action.UNCOVER, col, self.rowDimension-row))
				self.board[row+1][col-1] = 'F'
				self.board[row+1][col+1] = 'F'
				return None
			
			# check 'down'
			if row-1 >= 0 and self.board[row-1][col] == '?' and self.board[row-1][col-1] == '?' and self.board[row-1][col+1] == '?':
				self.actionQueue.append(Action(AI.Action.UNCOVER, col, self.rowDimension-row-2))
				self.board[row-1][col-1] = 'F'
				self.board[row-1][col+1] = 'F'
				return None

		elif orientation == 'vertical':
			# META: is this neccessary?
			# check if col+1 and col-1 are in bound
			# doesn't fit the pattern if there are '?' on both sides of 2
			if col+1 < self.colDimension and col-1 >= 0 and self.board[row][col-1] == '?' and self.board[row][col+1] == '?':
				return None
			# check 'right'
			if col+1 < self.colDimension and self.board[row][col+1] == '?' and self.board[row-1][col+1] == '?' and self.board[row+1][col+1] == '?':
				self.actionQueue.append(Action(AI.Action.UNCOVER, col+1, self.rowDimension-row-1))
				self.board[row-1][col+1] = 'F'
				self.board[row+1][col+1] = 'F'
				return None
			
			# check 'left'
			if col-1 >= 0 and self.board[row][col-1] == '?' and self.board[row-1][col-1] == '?' and self.board[row+1][col-1] == '?':
				self.actionQueue.append(Action(AI.Action.UNCOVER, col-1, self.rowDimension-row-1))
				self.board[row-1][col-1] = 'F'
				self.board[row+1][col-1] = 'F'
				return None

		return None

	
	def runQueuedActions(self):
		action = self.actionQueue.pop(0)
		while len(self.actionQueue) >= 1 and self.board[self.rowDimension-1-action.getY()][action.getX()] != '?':
			action = self.actionQueue.pop(0)
		if len(self.actionQueue) == 0 and self.board[self.rowDimension-1-action.getY()][action.getX()] != '?':
			return None
		self.lastX = action.getX()
		self.lastY = action.getY()
		return action

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
		# debugging
		if self.strong_debug:
			print('rowDimension: ', self.rowDimension)
			print('colDimension: ', self.colDimension)
			

		# FOR DEBUGGING: changing external bomb marker '-1' to internal flag 'F'
		if number == -1:
			number = 'F'
		
		# update board with number
		self.board[self.rowDimension-1-self.lastY][self.lastX] = str(number)

		if self.actionQueue:
			action = self.runQueuedActions()
			if action:
				return action

		# First we will uncover covered neigbours to '0'
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == '0' and len(self.getNeighborsOfType(row, col, '?')) > 0:
					self.lastX, self.lastY = self.getNeighborsOfType(row, col, '?')[0]
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)
				
		# from now on we will always first check if a tile has any covered neighbours to speed up search
		# Second we will flag neigbours to tiles with amount of covered tiles neighbouring equal to its number
		# MARKING BOMBS
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] != '?' and self.board[row][col] != '0' and len(self.getNeighborsOfType(row, col, '?')) > 0 and self.board[row][col] == str(len(self.getNeighborsOfType(row, col, '?')) + len(self.getNeighborsOfType(row, col, 'F'))):
					# FOR OPTIMIZATION
					if not self.debug:
						bombs = self.getNeighborsOfType(row, col, '?')
						for bomb in bombs:
							x, y = bomb
							self.board[self.rowDimension-1-y][x] = 'F'
					
					# FOR DEBUG
					if self.debug:
						self.lastX, self.lastY = self.getNeighborsOfType(row, col, '?')[0]
						return Action(AI.Action.FLAG, self.lastX, self.lastY)
				
		# Third, if number of flags (marked with F) is same as tile's number, we'll uncover all its neigbours
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == str(len(self.getNeighborsOfType(row, col, 'F'))) and len(self.getNeighborsOfType(row, col, '?')) > 0:
					self.lastX, self.lastY = self.getNeighborsOfType(row, col, '?')[0]
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)
		
		# Fourth, 1-2-1 pattern
		pos = self.find_pattern_121()
		if pos:
			self.check_121_pattern(pos[0], pos[1], pos[2])


		if self.actionQueue:
			action = self.runQueuedActions()
			if self.debug:
					print('considering actionQueue after 1-2-1')
			if action:
				if self.debug:
					print('executing actionQueue after 1-2-1')
				return action
		
		


		# Fifth, 1-2-2-1 pattern

		
		# need to work on 3-4-3 pattern for expert worlds here


		# Running the probabilistic model
		

		# NOW, THIS JUST MAKES THE FIRST POSSIBLE MOVE
		# RANDOM MOVE HERE

		# If the puzzle still hasn't been completed to this point, we'll start doing some probability and guessing
		# For now, I'm just choosing any first random tile xd
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				if self.board[row][col] == '?':
					if self.debug:
						print('making a random move...')
					self.lastX, self.lastY = col, self.rowDimension-row-1
					return Action(AI.Action.UNCOVER, self.lastX, self.lastY)


		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
