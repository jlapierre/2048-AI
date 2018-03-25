const BOARD = "board";
const PLAYER = "player";

function getRandomMove(grid) {
    return Math.floor(Math.random() * 4);
}

// returns the optimal move from the given state
function getBestMove(grid) {
    /*
    up: 0
    right: 1
    down: 2
    left: 3
     */
    var depth = 1;
    var movesWithScore = getMovesWithScores(grid, depth);

    var maxScore = Number.MIN_VALUE;
    var maxMove = null;

    movesWithScore.forEach(function(move) {
       if (move.score > maxScore) {
           maxScore = move.score;
           maxMove = move.move;
       }
    });

    //return move that matches best score
    return maxMove;
}

function getMovesWithScores(grid, depth) {
    var pairs = [];
    for (var i = 0; i < 4; i++) {
        var nextState = cloneGrid(grid);

        if (nextState.move(i)) {
            var score = expectimax(nextState, depth - 1, BOARD);
            pairs.push({move: i, score: score});
        }
    }
    return pairs;
}

function expectimax(grid, depth, agent) {
    if (depth = 0) {
        return evaluate(grid);
    }

    else if (agent == PLAYER) {
        var score = Number.MIN_VALUE;

        for (var i = 0; i < 4; i++) {
            var nextState = cloneGrid(grid);
            if (nextState.move(i)) {
                var nextScore = expectimax(nextState, depth - 1, BOARD);

                if (nextScore > score) {
                    score = nextScore;
                }
            }

        }
        return score;
    }
    else if (agent = BOARD) {
        var score = Number.MIN_VALUE;
        var availableCells = grid.availableCells();
        var cellCount = availableCells.length;

        for (var i = 0; i < cellCount; i++) {
            // if board inserts 4
            var nextState = cloneGrid(grid);
            nextState.insertTile(new Tile(availableCells[i], 4));
            var nextScore = expectimax(nextState, depth - 1, PLAYER);
            if (nextScore != Number.MIN_VALUE) {
                score = score + (nextScore * 0.1);
            }
            // if board inserts 2
            var nextState = cloneGrid(grid);
            nextState.insertTile(new Tile(availableCells[i], 2));
            nextScore = expectimax(nextState, depth - 1, PLAYER);
            if (nextScore != Number.MIN_VALUE) {
                score = score + (nextScore * 0.9);
            }
        }
        score = score / cellCount;
        return score;
    }
}

function cloneGrid(grid) {
    var clone = new Grid(grid.size, null);
    for(var x in grid.cells){
        for (var y in x) {
            var cell = grid.cells[x][y];
            if (cell == null){
                clone.cells[x][y] = null;
            }
            else {
                var position = {x: cell.x, y: cell.y};
                clone.cells[x][y] = new Tile(position, cell.value);
            }
        }
    }
    return clone;
}

function simepleClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

// evaluation function
function evaluate(grid) {
    // stub for now
    return 2;
}