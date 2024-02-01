import random


class Board:
    def __init__(self):
        self.board = [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 2, 2, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 2, 2, 2, -1, -1, -1, -1],
            [-1, -1, -1, 2, 2, 2, 2, -1, -1, -1, -1],
            [-1, -1, -1, 2, 2, 2, 2, 2, -1, -1, -1],
            [-1, -1, 0, 0, 0, 0, 0, 0, -1, -1, -1],
            [-1, -1, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, -1, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, -1, 0, 0, 0, 0, 0, 0, -1, -1, -1],
            [-1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1],
            [-1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 1, 1, 1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

    def randomizeBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == -1:
                    continue
                else:
                    self.board[i][j] = random.randint(0, 2)
        return self.board

    def print_board(self):
        for row in self.board:
            for cell in row:
                if cell == -1:
                    print(" ", end=" ")
                elif cell == 0:
                    print("O", end=" ")
                elif cell == 1:
                    print("1", end=" ")
                elif cell == 2:
                    print("2", end=" ")
            print()

    def makeMove(self, player, moveFrom, moveTo):
        toX = moveTo[1]
        toY = moveTo[0]
        fromX = moveFrom[1]
        fromY = moveFrom[0]
        if self.board[toX][toY] == 0:
            possibleMoves = self.getPossibleMoves(fromX, fromY)
            if tuple(moveTo) in possibleMoves[0] or tuple(moveTo) in possibleMoves[1]:
                if player == "player1" and self.board[fromX][fromY] == 1:
                    self.board[fromX][fromY] = 0
                    self.board[toX][toY] = 1
                    print("player 1 moved")
                elif player == "player2" and self.board[fromX][fromY] == 2:
                    self.board[fromX][fromY] = 0
                    self.board[toX][toY] = 2
                    print("player 2 moved")
        else:
            print("invalid move")
            assert False

    def countMarbles(self):
        ones = 0
        twos = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i <= 5 and self.board[i][j] == 1:
                    ones += 1
                if i >= 13 and self.board[i][j] == 2:
                    twos += 1
        return ones, twos

    def checkForWin(self, player):
        if player == 1:
            r = range(1, 6)
            enemy = 2
        else:
            r = range(13, 18)
            enemy = 1

        for i in r:
            for j in range(len(self.board[i])):
                if self.board[i][j] == enemy:
                    return False
        return True

    def getPossibleMoves(self, x, y):
        directions = [
            (-1, 0), (0, -1), (0, 1), (1, 0)
        ]
        if y % 2 == 0:
            directions.extend([(-1, -1), (-1, 1)])
        else:
            directions.extend([(1, -1), (1, 1)])

        possible_steps = []
        possible_jumps = []

        for direction in directions:
            searched_coords = (y - direction[0], x - direction[1])

            if searched_coords[1] % 2 == 0:
                searched_coords = (searched_coords[0] - 1, searched_coords[1])

            # Check if searched coordinates are within the board bounds
            if 0 <= searched_coords[1] < len(self.board) and 0 <= searched_coords[0] < len(self.board[0]):
                if self.board[searched_coords[1]][searched_coords[0]] == 0:
                    possible_steps.append(searched_coords)
                else:
                    next_coords = (y - (2 * direction[0]), x - (2 * direction[1]))

                    # Check if next coordinates are within the board bounds
                    if 0 <= next_coords[1] < len(self.board) and 0 <= next_coords[0] < len(self.board[0]):
                        if self.board[next_coords[1]][next_coords[0]] == 0:
                            possible_jumps.append(next_coords)

        return possible_steps, possible_jumps
