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
    var depth = 6;
    var movesWithScore = getMovesWithScores(grid, depth);

    var maxScore = Number.MIN_VALUE;
    var maxMove = null;

    movesWithScore.foreach(function(move) {
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
        var nextState = grid.clone();

        if (nextState.move(i)) {
            var score = expectimax(grid, depth - 1, BOARD);
            pairs.push({move: i, score: score});
        }
    }
    return pairs;
}

function expectimax(grid, depth, agent) {
    if (depth = 0) {
        return grid.getScore();
    }

    else if (agent == PLAYER) {
        var score = Number.MIN_VALUE;

        for (var i = 0; i < 4; i++) {
            var nextState = grid.clone();
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
        var cellCount = cells.length;

        for (var i = 0; i < cellCount; i++) {
            // if board inserts 4
            var nextState = grid.clone();
            nextState.insertTile(new Tile(cells[i], 4));
            var nextScore = expectimax(nextState, depth - 1, PLAYER);
            if (nextScore == Number.MIN_VALUE) {
                score = score + 0;
            }
            else {
                score = score + (nextScore * 0.1);
            }
            // if board inserts 2
            var nextState = grid.clone();
            nextState.insertTile(new Tile(cells[i], 2));
            nextScore = expectimax(nextState, depth - 1, PLAYER);
            if (nextScore == Number.MIN_VALUE) {
                score = score + 0;
            }
            else {
                score = score + (nextScore * 0.9);
            }
        }
        score = score / cellCount;
        return score;
    }
}