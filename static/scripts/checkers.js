
const evenDivs = document.querySelectorAll('[y]:nth-child(odd)');
const magicButton = document.getElementById('magicButton');
const endTurnButton = document.getElementById('endTurnButton');
const currentPlayerMarker = document.getElementById('playerMarker');
let divsShifted = false;
let selectedElement = null;
let previousElement = null;
let movingElement = null;
let possibleSteps = [];
let possibleJumps = [];
let currentPlayer = 'player1';
const move = {
    "moveFrom": [],
    "moveTo": [],
    "player": currentPlayer
}
shiftDivs();
let boardDataElement = document.getElementById("board-data");
boardData = JSON.parse(boardDataElement.dataset.board);
magicButton.addEventListener('click', shiftDivs);
document.addEventListener('keyup', (e) => {
    if (e.key === 's')
        shiftDivs();
})

endTurnButton.addEventListener('click', endTurn);
function shiftDivs() {
        if (!divsShifted) {
            evenDivs.forEach(function (div) {
                div.insertAdjacentHTML('afterbegin', '<div class="hole empty"></div> <div class="void"></div>');
            });
            divsShifted = true;
            magicButton.innerText = ' < ';
        } else {
            evenDivs.forEach(function (div) {
                div.innerHTML = div.innerHTML.replace('<div class="hole empty"></div> <div class="void"></div>', '');
            });

            divsShifted = false;
            magicButton.innerText = ' > ';
        }
    }
function highlightHole(element)
{
    if (selectedElement) {
        selectedElement.style.border = '';
        selectedElement.style.boxSizing = '';
        }

    selectedElement = element;
    selectedElement.style.border = "solid white";
    selectedElement.style.boxSizing = "border-box"
    if (previousElement) {
        previousElement.style.border = '';
        previousElement.style.boxSizing = '';
        }
    }
function clearHighlightedSteps()
{
    possibleSteps.forEach(function (div) {
            div.style.border = '';
            div.style.boxSizing = '';
        })
    possibleSteps = [];
}
function clearHighlightedJumps()
{
    possibleJumps.forEach(function (div) {
            div.style.border = '';
            div.style.boxSizing = '';
        })
    possibleJumps = [];
}
function highlightSteps(){
    possibleSteps.forEach(function (div) {
        div.style.border = "solid #578A93";
        div.style.boxSizing = "border-box"
        })
}
function highlightJumps(){
    possibleJumps.forEach(function (div) {
        div.style.border = "solid #578A93";
        div.style.boxSizing = "border-box"
        })
}

function findPossibleMoves(x, y)
{

    const directions = [
        [-1, 0], [0, -1], [0, 1], [1, 0]
    ]
    if (y % 2 === 0) {
        directions.push([-1, -1]);
        directions.push([-1, 1]);
    }
    else {
        directions.push([1, -1]);
        directions.push([1, 1]);
    }

    directions.forEach(function (direction) {
            console.log("check direction: " + direction);
        const searchedCoords = [x - direction[0], y - direction[1]];
        const searchedSquare = document.querySelectorAll(`[x="${searchedCoords[0]}"][y="${searchedCoords[1]}"]`).item(0);

        if (searchedSquare) {
            if (!(searchedSquare.classList.contains('player1') || searchedSquare.classList.contains('player2'))) {
                possibleSteps.push(searchedSquare);
            }
            else {
                let nextCoords = [x - (2 * direction[0]), y - (2 * direction[1])];
                let nextSquare = document.querySelectorAll(`[x="${nextCoords[0]}"][y="${nextCoords[1]}"]`).item(0);

                if (nextSquare)
                {
                    if(nextCoords[1] % 2 === 0)
                        {
                            if(direction[1] !== 0)
                            nextCoords[0] -= 1;
                        }
                        else if(direction[1] !== 0) nextCoords[0] += 1;
                        nextSquare = document.querySelectorAll(`[x="${nextCoords[0]}"][y="${nextCoords[1]}"]`).item(0);
                        if (nextSquare){
                            if (!(nextSquare.classList.contains('player1') || nextSquare.classList.contains('player2'))) {
                            possibleJumps.push(nextSquare);
                            console.log("added jump: " + nextCoords[0] + ", " + nextCoords[1]+ "from dir: "+2 * direction[0] + ", "+2 * direction[1]);
                        }
                    }
                }
            }
        }
        else {
            console.log("[debug] square (" + searchedCoords[0] + ", " + searchedCoords[1] + ") doesn't exist")
        }
    })
}
function endTurn()
{
    clearHighlightedSteps();
    clearHighlightedJumps();
    movingElement = null;
    previousElement = null;
    if(currentPlayer === 'player1')
    {
        currentPlayer = 'player2';
        currentPlayerMarker.style.backgroundColor = '#45F0DF';
    }
    else
    {
        currentPlayer = 'player1';
        currentPlayerMarker.style.backgroundColor = '#F7ACCF';
    }
    if (selectedElement) {
        selectedElement.style.border = '';
        selectedElement.style.boxSizing = '';
        }

}
function holeClicked(element) {
    let x = parseInt(element.getAttribute('x'));
    let y = parseInt(element.getAttribute('y'));


    if (!movingElement && element.classList.contains(currentPlayer)) {
        highlightHole(element);
        clearHighlightedSteps();
        clearHighlightedJumps();
        findPossibleMoves(x, y);
        highlightSteps();
        highlightJumps();
        movingElement = element;
        previousElement = element;
    } else if (Array.from(possibleSteps).includes(element)) {
        saveMove(element);
        movePiece(element);
        endTurn();
        sendData(move);
    } else if (Array.from(possibleJumps).includes(element)) {
        saveMove(element);
        sendData(move);
        movePiece(element);
        highlightHole(element);
        findPossibleMoves(x, y);
        clearHighlightedSteps();
        highlightJumps();
        previousElement = element;

    }
}
    function movePiece(element) {
    element.classList.add(currentPlayer);
    if (previousElement) previousElement.classList.remove(currentPlayer);
    highlightHole(element);
    clearHighlightedSteps();
    clearHighlightedJumps();
}
function saveMove(element)
{
    selectedElement = element;
    move.player = currentPlayer;
    if(previousElement && selectedElement)
    {
        move.moveTo[0] = parseInt(selectedElement.getAttribute('x'));
        move.moveTo[1] = parseInt(selectedElement.getAttribute('y'));
        move.moveFrom[0] = parseInt(previousElement.getAttribute('x'));
        move.moveFrom[1] = parseInt(previousElement.getAttribute('y'));
        console.log(move.moveTo[0])
        console.log(move.moveTo[1])
        console.log(move.moveFrom[0])
        console.log(move.moveFrom[1])
    }
    else console.log("move doesn't exist");

}
function sendData(move){

    fetch('/update_board', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(move)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // You can perform additional actions or handle the response if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });

}


