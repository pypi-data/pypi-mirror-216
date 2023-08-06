let state;
let previousState;

let selectedPiece = null;
let piecePositions = {};

const refreshState = () => {
    fetch("/status")
        .then(r => r.json())
        .then(newState => {
            previousState = state;
            state = newState;
            render();
        });
}

const makeMove = (index) => {
    fetch("/play/" + index.toString())
        .then(console.log)
        .then(refreshState);
}

const startGame = () => {
    fetch("/start");
}

function toggleSelect(event) {
    const sides = event.target.dataset.sides.split(",").map(str => Number(str));

    // If this piece was already selected, unselect it
    if (selectedPiece !== null && selectedPiece[0] === sides[0] && selectedPiece[1] === sides[1]) {
        getHandPiece(selectedPiece).classList.remove("selected");
        selectedPiece = null;
        return;
    }

    if (selectedPiece !== null) {
        getHandPiece(selectedPiece).classList.remove("selected");
    }

    selectedPiece = sides;
    getHandPiece(selectedPiece).classList.add("selected");
}

function attemptPlay(event) {
    // If there's no selected piece, nothing can be played
    if (selectedPiece === null) {
        return;
    }

    let closestPiece = null;
    let minDistance = BLOCK_SIZE;

    for (const key of Object.keys(piecePositions)) {
        const pieceSides = JSON.parse(key);
        const pieceX = piecePositions[key].x;
        const pieceY = piecePositions[key].y;

        const x = event.clientX - canvasPan.x;
        const y = event.clientY - canvasPan.y;

        const dx = pieceX - x;
        const dy = pieceY - y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < minDistance) {
            minDistance = distance;
            closestPiece = pieceSides;
        }
    }

    if (closestPiece === null || selectedPiece === null) {
        return;
    }

    for (let i = 0; i < state.round.options.length; i++) {
        const option = state.round.options[i];

        if (JSON.stringify(option.origin.sort()) === JSON.stringify(closestPiece.sort())
            && JSON.stringify(option.piece.sort()) === JSON.stringify(selectedPiece.sort())) {
            makeMove(i);
            selectedPiece = null;
            return;
        }
    }
}

setInterval(refreshState, 200);