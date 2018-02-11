# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #Factors that influence how good a move is: ghosts, food, and capsules
        # We want to reward distance from ghosts if normal, nearness if scared (and not about to change)
        # We want to reward proximity to food and capsules
        currentFood = currentGameState.getFood();
        currentCapsules = currentGameState.getCapsules();

        stateEvaluation = 0

        # distance from ghosts in a gamestate
        for ghost in newGhostStates:
        	mDistance = manhattanDistance(ghost.getPosition(), newPos)

        	if (ghost.scaredTimer != 0 and mDistance <= 1):
        		stateEvaluation = stateEvaluation + 2000
    		elif (mDistance <= 1):
    			stateEvaluation = stateEvaluation - 200

		# distance from food in a gamestate	
		for x in range(currentFood.width):
			for y in range(currentFood.height):
				if(currentFood[x][y]):
					mDistance = manhattanDistance((x,y), newPos)
					if (mDistance == 0):
						stateEvaluation = stateEvaluation + 100
					else:
						stateEvaluation = stateEvaluation + 1.0 / (mDistance * mDistance)

		#distance from capsules in a gamestate
		for capsule in currentCapsules:
			mDistance = manhattanDistance(capsule, newPos)
			if (mDistance == 0):
				stateEvaluation = stateEvaluation + 100
			else:
				stateEvaluation = stateEvaluation + 10/mDistance

        return stateEvaluation

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        #Run minimaxMax to cycle between the full minimax algorithm
        bestScore, bestAction = self.minimaxMax(gameState, self.depth)
        return bestAction

    #Evaluates max option given a set of mins
    def minimaxMax(self, gameState, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), ''

        mins = []
        legalActions = gameState.getLegalActions()
        for action in legalActions:
        	actionMin = self.minimaxMin(gameState.generateSuccessor(self.index, action), 1, depth)
        	mins.append(actionMin)
    	bestMin = max(mins)

       	bestMoves = []
        for action in range(len(mins)):
       		if mins[action] == bestMin:
       			bestMoves.append(action)

        return bestMin, legalActions[bestMoves[0]]

     #Evaluates the min option given a set of maxes
    def minimaxMin(self, gameState, agentIndex, depth):  
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), ''

        legalActions = gameState.getLegalActions(agentIndex)
        scores = []
        if(agentIndex != gameState.getNumAgents() - 1):
        	for action in legalActions:
        		score = self.minimaxMin(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth)
        		scores.append(score)
        else:
        	for action in legalActions:
        		result = self.minimaxMax(gameState.generateSuccessor(agentIndex, action),(depth - 1))
        		score = result[0]
        		scores.append(score)
        minScore = min(scores)

        bestMoves = []
        for action in range(len(scores)):
       		if scores[action] == minScore:
       			bestMoves.append(action)

        return minScore, legalActions[bestMoves[0]]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0)
        expectimaxAction = ''
        expectimaxScore = -999999

        for action in legalActions:
            successorState = gameState.generateSuccessor(0,action)
            score = self.expectimaxGhosts(successorState, 0, 1)

            if score > expectimaxScore:
                expectimaxAction = action
                expectimaxScore = score

        return expectimaxAction

    #pacman's maximizer action
    def expectimaxMax(self, gameState, depth):
    	nextLevel = depth + 1
        if self.depth == nextLevel or gameState.isWin() or gameState.isLose():  
        	return self.evaluationFunction(gameState)

        maxScore = -999999
        legalActions = gameState.getLegalActions(0)

        for action in legalActions:
        	successor= gameState.generateSuccessor(0, action)
        	maxScore = max(maxScore, self.expectimaxGhosts(successor, nextLevel, 1))

        return maxScore
        
    #expectimax action for ghosts
    def expectimaxGhosts(self, gameState,depth, agentIndex):
        if gameState.isWin() or gameState.isLose():  
        	return self.evaluationFunction(gameState)

       	legalActions = gameState.getLegalActions(agentIndex)
        expectimaxTotal = 0
        actionCount = len(legalActions)

        for action in legalActions:
            successor= gameState.generateSuccessor(agentIndex, action)

            if agentIndex == (gameState.getNumAgents() - 1):
                expectimaxValue = self.expectimaxMax(successor, depth)
            else:
                expectimaxValue = self.expectimaxGhosts(successor, depth, agentIndex + 1)
            expectimaxTotal = expectimaxTotal + expectimaxValue

        if actionCount == 0:
            return  0
        else:
        	return float(expectimaxTotal) / float(actionCount)




def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 

      I care about evaluating the closest piece of food, the proximity of ghosts in a given state,
      and the amount of food and capsules remaining in a given state. Also I want to maximize score.
      It's just a lot of tinkering to figure out which matters how much.
    """
    "*** YOUR CODE HERE ***"
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentGhosts = currentGameState.getGhostPositions()
    evaluation = 0

	#evaluate food distance
    closestFoodDistance = 999999999
    closestFoodFound = False

    for food in currentFood:
        mDistance = manhattanDistance(currentPos, food)
        if mDistance < closestFoodDistance:
            closestFoodDistance = mDistance
            closestFoodFound = True
    if closestFoodFound:
        evaluation = evaluation + closestFoodDistance
    
    #evaluate ghost proximity
    for ghost in currentGhosts:
        mDistance = manhattanDistance(currentPos, ghost)
        if mDistance < 2:
            evaluation = 999999999

    #evaluate scores and remaining food and capsules
    evaluation = evaluation - currentGameState.getScore() * 10
    evaluation = evaluation + currentGameState.getNumFood() * 1000
    evaluation = evaluation + len(currentGameState.getCapsules()) * 10

    #invert the value to prioritize correctly (kinda like reciprocal of values)
    return -evaluation

# Abbreviation
better = betterEvaluationFunction

