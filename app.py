from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

board = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
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

possibleSteps = []
possibleJumps = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/checkers')
def game():
    global board
    #board = randomizeBoard(board)
    return render_template('chinese_checkers.html', board=board)


def randomizeBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == -1:
                continue
            else:
                board[i][j] = random.randint(0, 2)
    return board


@app.route('/update_board', methods=['POST'])
def update_board():
    global board
    data = request.get_json()
    player = data['player']
    moveTo = data['moveTo']
    moveFrom = data['moveFrom']

    makeMove(board, player, moveFrom, moveTo)
    response = {'message': "data send"}
    return jsonify(response)



def makeMove(board, player, moveFrom, moveTo):
    toX = moveTo[1]
    toY = moveTo[0]
    fromX = moveFrom[1]
    fromY = moveFrom[0]
    if board[toX][toY] == 0:
        possibleMoves= getPossibleMoves(board, fromX, fromY)
        print(moveTo)
        if tuple(moveTo) in possibleMoves[0] or tuple(moveTo) in possibleMoves[1]:
            if player == "player1" and board[fromX][fromY] == 1:
                board[fromX][fromY] = 0
                board[toX][toY] = 1
                print("player 1 moved")
            elif player == "player2" and board[fromX][fromY] == 2:
                board[fromX][fromY] = 0
                board[toX][toY] = 2
                print("player 2 moved")
    else:
        print("invalid move")
        assert False

def getPossibleMoves(board, x, y):

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
        if 0 <= searched_coords[1] < len(board) and 0 <= searched_coords[0] < len(board[0]):
            if board[searched_coords[1]][searched_coords[0]] == 0:
                possible_steps.append(searched_coords)
            else:
                next_coords = (y - (2 * direction[0]), x - (2 * direction[1]))

                # Check if next coordinates are within the board bounds
                if 0 <= next_coords[1] < len(board) and 0 <= next_coords[0] < len(board[0]):
                    if board[next_coords[1]][next_coords[0]] == 0:
                        possible_jumps.append(next_coords)

    return possible_steps, possible_jumps


if app.name == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
