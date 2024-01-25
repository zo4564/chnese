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
    if board[moveFrom[0]][moveFrom[1]] == 1 and player == "player1":
        board[moveFrom[0]][moveFrom[1]] = 0
        board[moveTo[0][moveTo[1]]] = 1
        print("player 1")
    elif board[moveFrom[0]][moveFrom[1]] == 2 and player == "player2":
        board[moveFrom[0]][moveFrom[1]] = 0
        board[moveTo[0][moveTo[1]]] = 2
        print("player 2")
    else:
        print("invalid move")
if app.name == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
