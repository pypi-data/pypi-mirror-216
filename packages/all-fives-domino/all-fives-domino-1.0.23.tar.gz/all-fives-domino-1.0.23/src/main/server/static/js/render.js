class RenderError extends Error {}
const BLOCK_SIZE = 40;

let canvasPan = {x: 0, y: 0};
let persistentPan = {x: 0, y: 0};
let canvasMousedown = {x: null, y: null};
let canvasZoom = 1;

let DRAW_COUNT_DEBUG = 0;
const DRAW_LIMIT = 100;

function panStart(event) {
    canvasMousedown.x = event.clientX;
    canvasMousedown.y = event.clientY;
}

function pan(event) {
    if (canvasMousedown.x === null) { return; }

    const dx = event.clientX - canvasMousedown.x;
    const dy = event.clientY - canvasMousedown.y;

    const limX = window.innerWidth * 0.5;
    const limY = window.innerHeight * 0.5;

    const panX = Math.max(-limX, Math.min(persistentPan.x + dx, limX));
    const panY = Math.max(-limY, Math.min(persistentPan.y + dy, limY));

    canvasPan = {x: panX, y: panY};
    render();
}

function panEnd(event) {
    if (canvasMousedown.x === null) { return; }

    persistentPan.x = canvasPan.x;
    persistentPan.y = canvasPan.y;
    canvasMousedown = {x: null, y: null};
}

function getFaceImage(points, closed = false) {
    if (points < 0 || points > 6) {
        throw RenderError(`No domino face with ${points} points`);
    }

    if (closed) {
        return document.getElementById("closed");
    }

    return document.getElementById("domino" + points);
}

function rotatePieceOffset(offset, rotation) {
    rotation = rotation % 360;

    switch (rotation) {
        case 0: return {
            x: offset.x,
            y: offset.y,
            rotation: offset.rotation
        }

        case 180: return {
            x: -offset.x,
            y: offset.y,
            rotation: offset.rotation
        }

        case 90: return {
            x: offset.y,
            y: offset.x,
            rotation: offset.rotation
        }

        case 270: return {
            x: offset.y,
            y: -offset.x,
            rotation: offset.rotation
        }

        default: throw new Error("Invalid rotation:", rotation);
    }
}

function getPieceOffsetDirection(parent, child) {
    if (parent.double) {
        const slot = parent.linked.indexOf(child);

        if (slot === 0) {
            return {
                x: 1.5,
                y: 0,
                rotation: 0
            }
        } else if (slot === 1) {
            return {
                x: -1.5,
                y: 0,
                rotation: 180
            }
        } else if (slot === 2) {
            return {
                x: 0,
                y: 2,
                rotation: 90
            }
        } else {
            return {
                x: 0,
                y: -2,
                rotation: -90
            }
        }
    } else {
        const direction = child.sides.includes(parent.sides[0]) ? -1 : 1;
        const multiplier = child.sides[0] === child.sides[1] ? 1.5 : 2;
        return {
            x: direction * multiplier,
            y: 0,
            rotation: 0
        }
    }
}

function getPieceOffset(parent, child) {
    const offset = getPieceOffsetDirection(parent, child);
    offset.x *= BLOCK_SIZE
    offset.y *= BLOCK_SIZE
    return rotatePieceOffset(offset, parent.rotation);
}

class Piece {
    constructor(sides, closed, linked, x, y, rotation = 0) {
        this.sides = sides;
        this.closed = closed;
        this.linked = linked;
        this.double = sides[0] === sides[1];
        this.x = x;
        this.y = y;
        this.rotation = rotation;

        piecePositions[JSON.stringify(this.sides)] = {x: this.x, y: this.y};
    }

    render(ctx) {
        DRAW_COUNT_DEBUG++
        if (DRAW_COUNT_DEBUG > DRAW_LIMIT) {
            return;
        }

        ctx.save();

        ctx.translate(this.x, this.y);

        ctx.rotate(this.rotation / 180 * Math.PI);

        if (this.double) {
            ctx.rotate(90 / 180 * Math.PI);
        }

        // Background
        ctx.fillStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(-BLOCK_SIZE, -0.5 * BLOCK_SIZE, 2 * BLOCK_SIZE, BLOCK_SIZE, 5);
        ctx.fill();

        // Faces
        ctx.drawImage(getFaceImage(this.sides[0], this.closed), -BLOCK_SIZE, -0.5 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        ctx.drawImage(getFaceImage(this.sides[1], this.closed), 0, -0.5 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);

        // Separator line
        ctx.beginPath();
        ctx.moveTo(0, -0.5 * BLOCK_SIZE);
        ctx.lineTo(0, -0.5 * BLOCK_SIZE);
        ctx.stroke();

        ctx.restore();

        for (let i = 0; i < this.linked.length; ++i) {
            const linkedPiece = this.linked[i];

            // Flip the linked Piece if the default side does not match
            if (this.rotation - linkedPiece.rotation === 180) {
                if (!this.sides.includes(linkedPiece.sides[1])) {
                    linkedPiece.sides = [linkedPiece.sides[1], linkedPiece.sides[0]];
                }
            } else {
                if (!this.sides.includes(linkedPiece.sides[0])) {
                    linkedPiece.sides = [linkedPiece.sides[1], linkedPiece.sides[0]];
                }
            }

            const offset = getPieceOffset(this, linkedPiece);
            const attachedPiece = new Piece(
                linkedPiece.sides,
                linkedPiece.closed,
                linkedPiece.linked,
                this.x + offset.x,
                this.y + offset.y,
                this.rotation + offset.rotation
            )

            attachedPiece.render(ctx);
        }
    }
}

function render() {
    if (state.round === null) {
        return;
    }

    renderBoard();
    document.getElementById("drawpool-count").innerText = state.round.pool.length;

    renderOpponentHand();
    renderPlayerHand();
}

function renderBoard() {
    DRAW_COUNT_DEBUG = 0;
    piecePositions = {};

    const canvas = document.getElementById("board");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const ctx = document.getElementById("board").getContext("2d");
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

    ctx.save();

    ctx.translate(canvasPan.x, canvasPan.y);

    const data = state.round.board.origin;
    const piece = new Piece(data.sides, data.closed, data.linked, window.innerWidth * 0.5, window.innerHeight * 0.5);
    piece.render(ctx);

    ctx.restore();
}

function hiddenHandPiece() {
    const piece = document.createElement("div");
    piece.className = "hand-piece hidden";
    return piece;
}

function handPiece(data) {
    const piece = document.createElement("div");

    piece.id = "piece" + data.sides[0] + data.sides[1];
    piece.dataset.sides = data.sides;
    piece.className = "hand-piece player";

    piece.addEventListener("click", event => toggleSelect(event));

    for (const side of data.sides) {
        const face = document.createElement("img");
        face.src = getFaceImage(side).src;
        face.draggable = false;
        face.dataset.sides = data.sides;
        piece.appendChild(face);
    }

    return piece;
}

function renderOpponentHand() {
    if (previousState === undefined || JSON.stringify(state.player1.hand) !== JSON.stringify(previousState.player1.hand)) {
        const hand = document.getElementById("opponent-hand");
        hand.innerHTML = "";

        for (let i = 0; i < state.player1.hand.length; i++) {
            hand.appendChild(hiddenHandPiece());
        }
    }
}

function renderPlayerHand() {
    if (previousState === undefined || JSON.stringify(state.player2.hand) !== JSON.stringify(previousState.player2.hand)) {
        const hand = document.getElementById("player-hand");
        hand.innerHTML = "";

        for (const piece of state.player2.hand) {
            hand.appendChild(handPiece(piece));
        }
    }
}

function getHandPiece(sides) {
    return document.getElementById("piece" + sides[0] + sides[1]);
}