from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route('/checkers')
def home():
    # Representing the board with a 2D list
    # 1 for a hole, 0 for no hole
    board = [
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

if app.name == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
