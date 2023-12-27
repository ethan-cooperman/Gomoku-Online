import pygame
from enum import Enum

import json
import sys
import tkinter


class Player(str, Enum):
    WHITE_PLAYER = 'white'
    BLACK_PLAYER = 'black'


class Intersection:

    def __init__(self, row, column, state=None):
        """constructor for an Intersection

        :param row: the row number of the intersection
        :param column: the column number of the intersection
        :param state: the state of the intersection (None, Player.WHITE_PLAYER, Player.BLACK_PLAYER), defaults to None
        """
        self.row = row
        self.column = column
        self.state = state


class Game:
    def __init__(self, id):
        self.turn = 0
        self.id = id
        self.connected = False
        self.game_board = []
        for i in range(1, 16):
            self.game_board.append([])
            for j in range(1, 16):
                self.game_board[i - 1].append(Intersection(i, j))

    def check_win(self):
        """checks if there is a winner on the board

        :return: returns the player that won (Player.WHITE_PLAYER or Player.BLACK_PLAYER) or None if there is no winner
        """
        # check row wins
        for row in self.game_board:
            for col in range(len(self.game_board) - 4):
                if row[col].state == row[col + 1].state and row[col].state == row[col + 2].state and row[col].state == row[col + 3].state and row[col].state == row[col + 4].state and row[col].state != None:
                    return row[col].state
        # check column wins
        for row in range(len(self.game_board) - 4):
            for col in range(len(self.game_board)):
                if self.game_board[row][col].state == self.game_board[row + 1][col].state and self.game_board[row][col].state == self.game_board[row + 2][col].state and self.game_board[row][col].state == self.game_board[row + 3][col].state and self.game_board[row][col].state == self.game_board[row + 4][col].state and self.game_board[row][col].state != None:
                    return self.game_board[row][col].state
        # check northeast wins
        for row in range(len(self.game_board) - 4):
            for col in range(len(self.game_board) - 4):
                if self.game_board[row][col].state == self.game_board[row + 1][col + 1].state and self.game_board[row][col].state == self.game_board[row + 2][col + 2].state and self.game_board[row][col].state == self.game_board[row + 3][col + 3].state and self.game_board[row][col].state == self.game_board[row + 4][col + 4].state and self.game_board[row][col].state != None:
                    return self.game_board[row][col].state
        # check southeast wins
        for row in range(len(self.game_board) - 4):
            for col in range(4, len(self.game_board)):
                if self.game_board[row][col].state == self.game_board[row + 1][col - 1].state and self.game_board[row][col].state == self.game_board[row + 2][col - 2].state and self.game_board[row][col].state == self.game_board[row + 3][col - 3].state and self.game_board[row][col].state == self.game_board[row + 4][col - 4].state and self.game_board[row][col].state != None:
                    return self.game_board[row][col].state
        return None

    def check_draw(self):
        """checks if the game is a draw
        """
        for row in self.game_board:
            for intersection in row:
                if intersection.state == None:
                    return False
        return True

    def reset(self):
        """resets the game board
        """
        self.turn = 0
        self.game_board = []
        for i in range(1, 16):
            self.game_board.append([])
            for j in range(1, 16):
                self.game_board[i - 1].append(Intersection(i, j))

    def winner(self):
        """returns the winner of the game if there is one

        :return: a number representing the winner of the game (0 if white, 1 if black, -1 if draw, None if no winner)
        """
        if self.check_win() == Player.WHITE_PLAYER:
            return 0
        elif self.check_win() == Player.BLACK_PLAYER:
            return 1
        elif self.check_draw():
            return -1
        else:
            return None

    def make_move(self, row, col):
        """method to make a move on the game board

        :param row: the row of the intersection to place a piece on
        :param col: the column of the intersection to place a piece on
        """
        player_piece = None
        if self.turn == 0:
            player_piece = Player.WHITE_PLAYER
        else:
            player_piece = Player.BLACK_PLAYER
        self.game_board[row - 1][col - 1].state = player_piece
        self.turn ^= 1
