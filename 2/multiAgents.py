# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        dist2ghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
        dist2food = newFood and min([manhattanDistance(newPos, food) for food in newFood]) or 0
        scaredScore = sum(newScaredTimes)
        dist2food = (1.0/dist2food) if (dist2food) else dist2food

        return successorGameState.getScore() + dist2food * dist2ghost + scaredScore


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
      Your minimax agent (question 2)
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
        return self.Minimax(gameState, 0)[0]

    def Minimax(self, gameState, depth):
        if self.Terminal(gameState, depth):
            return (None, self.evaluationFunction(gameState))

        if depth % gameState.getNumAgents() is 0:
            return self.Maxturn(gameState, depth)
        else:
            return self.Minturn(gameState, depth)

    def Maxturn(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        if len(actions) is 0:
            return (None, self.evaluationFunction(gameState))

        v = (None, -float("inf"))
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            move, val = self.Minimax(successor, depth + 1)
            if val > v[1]:
                v = (action, val)
        return v

    def Minturn(self, gameState, depth):
        ghost = depth % gameState.getNumAgents()
        actions = gameState.getLegalActions(ghost)

        if len(actions) is 0:
            return (None, self.evaluationFunction(gameState))

        v = (None, float("inf"))
        for action in actions:
            successor = gameState.generateSuccessor(ghost, action)
            move, val = self.Minimax(successor, depth + 1)
            if val < v[1]:
                v = (action, val)
        return v

    def Terminal(self, gameState, depth):
        return depth is self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.Prune(gameState, 0, -float("inf"), float("inf"))[0]

    def Prune(self, gameState, depth, alpha, beta):
        if self.Terminal(gameState, depth):
            return (None, self.evaluationFunction(gameState))

        if depth % gameState.getNumAgents() is 0:
            return self.Maxturn(gameState, depth, alpha, beta)
        else:
            return self.Minturn(gameState, depth, alpha, beta)

    def Maxturn(self, gameState, depth, alpha, beta):
        actions = gameState.getLegalActions(0)
        if len(actions) is 0:
            return (None, self.evaluationFunction(gameState))

        v = (None, -float("inf"))
        for action in actions: 
            successor = gameState.generateSuccessor(0, action)
            move, val = self.Prune(successor, depth + 1, alpha, beta)
            if val > v[1]:
                v = (action, val)

            if v[1] > beta:
                return v

            alpha = max(alpha, v[1])

        return v


    def Minturn(self, gameState, depth, alpha, beta):
        ghost = depth % gameState.getNumAgents()
        actions = gameState.getLegalActions(ghost)
        if len(actions) is 0:
            return (None, self.evaluationFunction(gameState))

        v = (None, float("inf"))
        for action in actions:
            successor = gameState.generateSuccessor(ghost, action)
            move, val = self.Prune(successor, depth + 1, alpha, beta)
            if val < v[1]:
                v = (action, val)

            if v[1] < alpha:
                return v

            beta = min(beta, v[1])

        return v

    def Terminal(self, gameState, depth):
        return depth is self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose()

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
        return self.Expmax(gameState, 0)[0]


    def Expmax(self, gameState, depth):
        if self.Terminal(gameState, depth):
            return (None, self.evaluationFunction(gameState))

        if depth % gameState.getNumAgents() is 0:
            return self.Maxturn(gameState, depth)
        else:
            return self.Expturn(gameState, depth)


    def Maxturn(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        if len(actions) is 0:
            return (None, self.evaluationFunction(gameState))

        v = (None, -float("inf"))
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            move, val = self.Expmax(successor, depth + 1)
            if val > v[1]:
                v = (action, val)

        return v

    def Expturn(self, gameState, depth):
        ghost = depth % gameState.getNumAgents()
        actions = gameState.getLegalActions(ghost)
        if len(actions) is 0:
            return (None, self.evaluationFunction(gameState))

        p = 1./len(actions)
        v = 0
        for action in actions:
            successor = gameState.generateSuccessor(ghost, action)
            move, val = self.Expmax(successor, depth + 1)
            v += val * p

        return (None, v)

    def Terminal(self, gameState, depth):
        return depth is self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsules = currentGameState.getCapsules()
    score = currentGameState.getScore()
    scared = sum(newScaredTimes)

    dist2food = 100

    if len(newFood) > 0:
        dist2food = min(dist2food, min([manhattanDistance(newPos, food) for food in newFood]))

    dist2food = 1.0/dist2food


    dist2cap = 100

    if len(newCapsules) > 0:
        dist2cap = min(dist2cap, min([manhattanDistance(newPos, cap) for cap in newCapsules]))

    dist2cap = 1.0/dist2cap

    return score + dist2food + dist2cap + scared

# Abbreviation
better = betterEvaluationFunction

