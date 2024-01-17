
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
shiftDivs();
magicButton.addEventListener('click', shiftDivs);
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
function holeClicked(element)
{
    let x = parseInt(element.getAttribute('x'));
    let y = parseInt(element.getAttribute('y'));


    if(previousElement === movingElement && element.classList.contains(currentPlayer))
    {
        highlightHole(element);
        clearHighlightedSteps();
        clearHighlightedJumps();
        findPossibleMoves(x, y);
        highlightSteps();
        highlightJumps();
        previousElement = element;
        movingElement = element;
    }
    if (Array.from(possibleSteps).includes(element)) {
        element.classList.add(currentPlayer);
        if(previousElement) previousElement.classList.remove(currentPlayer);
        highlightHole(element);
        endTurn();
        clearHighlightedSteps();
        clearHighlightedJumps();
    }
    if (Array.from(possibleJumps).includes(element)) {
        element.classList.add(currentPlayer);
        if(previousElement) previousElement.classList.remove(currentPlayer);
        highlightHole(element);
        findPossibleMoves(x, y);
        clearHighlightedSteps();
        highlightJumps();
        previousElement = element;

    }
}
