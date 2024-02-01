from flask import Flask, render_template, request, jsonify
from board import Board

app = Flask(__name__)

gameBoard = Board()

possibleSteps = []
possibleJumps = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/checkers')
def game():
    global gameBoard
    print(gameBoard)
    #gameBoard = gameBoard.randomizeBoard()
    return render_template('chinese_checkers.html', board=gameBoard.board)


@app.route('/update_board', methods=['POST'])
def update_board():
    global gameBoard
    data = request.get_json()
    player = data['player']
    moveTo = data['moveTo']
    moveFrom = data['moveFrom']

    gameBoard.makeMove(player, moveFrom, moveTo)
    gameBoard.print_board()
    print(gameBoard.countMarbles())
    if gameBoard.checkForWin(1):
        print("player 1 won")
    elif gameBoard.checkForWin(2):
        print("player 2 won")
    response = {'message': "data send"}
    return jsonify(response)

if app.name == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
