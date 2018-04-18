//METHODS ADAPTED FROM GAMEMANAGER FOR CLONED GRIDS

//Allow cloned grids to make moves 
//(adapted from GameManager.prototype.move -- gamestate modifications removed)
Grid.prototype.move = function (direction) {

  var self = this;

  var cell, tile;

  var vector     = this.getVector(direction);
  var traversals = this.buildTraversals(vector);
  var moved      = false;

//prepare all tiles (from GameManager.prototyp.prepareTiles)
  // self.eachCell(function (x, y, tile) {
  //   if (tile) {
  //     tile.mergedFrom = null;
  //     tile.savePosition();
  //   }
  // });

  self.prepareTiles();

  traversals.x.forEach(function (x) {
    traversals.y.forEach(function (y) {
      cell = { x: x, y: y };
      tile = self.cellContent(cell);

      if (tile) {
        var positions = self.findFarthestPosition(cell, vector);
        var next      = self.cellContent(positions.next);

        // Only one merger per row traversal?
        if (next && next.value === tile.value && !next.mergedFrom) {
          var merged = new Tile(positions.next, tile.value * 2);
          merged.mergedFrom = [tile, next];

          self.insertTile(merged);
          self.removeTile(tile);

          // Converge the two tiles' positions
          tile.updatePosition(positions.next);

          //removed score updates and 2048 endgame determination
        }
        else {
          self.moveTile(tile, positions.farthest);
        }

        if (!self.positionsEqual(cell, tile)) {
          moved = true; // The tile moved from its original cell!
        }
      }
    });
  });

  //return grid after movement for use in expectimax, *before* random tile insertion
  return moved;

  //remove random tile insertion, game over determination, GameManager actuate
};

//Allow cloned grids to access a vector 
//(adapted from GameManager.prototype.getVector)
Grid.prototype.getVector = function (direction) {
  // Vectors representing tile movement
  var map = {
    0: { x: 0,  y: -1 }, // Up
    1: { x: 1,  y: 0 },  // Right
    2: { x: 0,  y: 1 },  // Down
    3: { x: -1, y: 0 }   // Left
  };

  return map[direction];
};

//Allow cloned grids to build traversals
//(adapted from GameManager.prototype.buildTraversals)
Grid.prototype.buildTraversals = function (vector) {
  var traversals = { x: [], y: [] };

  for (var pos = 0; pos < this.size; pos++) {
    traversals.x.push(pos);
    traversals.y.push(pos);
  }

  // Always traverse from the farthest cell in the chosen direction
  if (vector.x === 1) traversals.x = traversals.x.reverse();
  if (vector.y === 1) traversals.y = traversals.y.reverse();

  return traversals;
};

//Allow cloned grids to prepare tiles 
//(adapted from GameManager.prototype.prepareTiles)
Grid.prototype.prepareTiles = function () {
  var self = this;
  self.eachCell(function (x, y, tile) {
    if (tile) {
      tile.mergedFrom = null;
      tile.savePosition();
    }
  });
};


//Allow cloned grids to find farthest position 
//(adapted from GameManager.prototype.findFarthestPosition)
Grid.prototype.findFarthestPosition = function (cell, vector) {
  var self = this;
  var previous;
  

  // Progress towards the vector direction until an obstacle is found
  do {
    previous = cell;
    cell     = { x: previous.x + vector.x, y: previous.y + vector.y };
  } while (self.withinBounds(cell) &&
           self.cellAvailable(cell));

  return {
    farthest: previous,
    next: cell // Used to check if a merge is required
  };
};

//Allow cloned grids to move a tile 
//(adapted from GameManager.prototype.moveTile)
Grid.prototype.moveTile = function (tile, cell) {
  var self = this;
  self.cells[tile.x][tile.y] = null;
  self.cells[cell.x][cell.y] = tile;
  tile.updatePosition(cell);

};

//Allow cloned grids to check if positions are equal 
//(adapted from GameManager.prototype.positionsEqual)
Grid.prototype.positionsEqual = function (first, second) {
  return first.x === second.x && first.y === second.y;
};


// OUR UTILITY METHODS FOR CLONED GRIDS

//deep clones a grid for expectimax algorithm
Grid.prototype.clone = function () {

  var currentGrid = this;
  var newGrid = new Grid(currentGrid.size, null);

  for (var i = 0; i < currentGrid.size; i++) {
    for (var j = 0; j < currentGrid.size; j++) {
      if (currentGrid.cells[i][j] === null) {
        newGrid.cells[i][j] = null;
      }
      else {
        var currentX = currentGrid.cells[i][j].x;
        var currentY = currentGrid.cells[i][j].y;
        var currentValue = currentGrid.cells[i][j].value;

        newGrid.cells[i][j] = new Tile({x: currentX, y: currentY}, currentValue);
      }
    }
  }
  return newGrid;
};

//Allows cloned grid score evaluation
Grid.prototype.getScore = function() {
  var self = this;

  var score = 0;
  var gridWeights = [[ 8,  4, 2, 1],
                     [ 16,  8,  4, 2],
                     [ 32,  16,  8,  4],
                     [ 64,  32,  16,  8]];

  this.eachCell(function(x, y, tile) {
    if (tile) {
      score = score + (gridWeights[x][y] * tile.value * tile.value);
    }
  });

  return score;
};


