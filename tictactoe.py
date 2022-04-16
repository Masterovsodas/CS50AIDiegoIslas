"""
Tic Tac Toe Player
"""

from asyncio.windows_events import INFINITE
from logging import exception
import math
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xamount = 0
    oamount = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                xamount += 1
            elif board[i][j] == "O":
                oamount += 1

    if xamount == oamount:
        return "X"
    else:
        return "O"



def actions(board):
    
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                act = (i,j)
                moves.append(act)
        
    return moves


def result(board, action):
    
    """""
    tempBor = copy.deepcopy(board)

    if tempBor[action[0]][action[1]] == EMPTY:
        tempBor[action[0]][action[1]] == player(tempBor)
        return tempBor
    else:
        raise Exception
    """""

    if action in actions(board):
        (i, j) = action
        current_player = player(board)
        new_board = copy.deepcopy(board)
        new_board[i][j] = current_player
        return new_board
    else:
        raise Exception
    


def winner(board):
    # ROWS
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == "X":
            return "X"
        elif board[i][0] == board[i][1] == board[i][2] == "O":
            return "O"
    # COLUMNS
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == "X":
            return "X"
        elif board[0][i] == board[1][i] == board[2][i] == "O":
            return "O"
 
    # Diagonals: bottom left to top right; top left to bottom right (in that order)
    if board[2][0] == board[1][1] == board[0][2] == "O":
        return board[2][0]
    elif board[0][0] == board[1][1] == board[2][2] == "O":
        return board[0][0]
    elif board[2][0] == board[1][1] == board[0][2] == "X":
        return board[2][0]
    elif board[0][0] == board[1][1] == board[2][2] == "X":
        return board[0][0]
    else:
        return None
   

def terminal(board):
    if(winner(board) == None):
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
        return True
    else:
        return True


def utility(board):
    if terminal(board) == True:
        win = winner(board)
        if win  == "X":
            return 1
        elif win  == "O":
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    
    plr = player(board)
    # output
    action = None
    # actions array
    act = actions(board)
    
    if plr == "X":
        paths = maxVal(board,  act, True)

        # each action index should correspond to a respective pathVal returned, compare the currentGreates number and store the index
        currentGreat = -INFINITE
        index = None
        print(paths)
        for i in range(len(paths)):
            if paths[i] > currentGreat:
                currentGreat = paths[i]
                index = i
            elif paths[i] == 1:
                break
        action = act[index]

        
    else:
        paths = minVal(board,  act, True)
        # each action index should correspond to a respective pathVal returned, compare the currentGreates number and store the index
        currentLow = INFINITE
        index = None
        for i in range(len(paths)):
            if paths[i] < currentLow:
                currentLow= paths[i]
                index = i
            
            if paths[i] == -1:
                break
        action =  act[index]

    return action





def minVal(board, acts, root):
    if terminal(board) == True:
        return utility(board)
    
    pathVals = []
    """
    # for every action recursively call the oppostie fucntion until utilities begin getting spit up, those utilities will begin to 
    be summed up to define the value of a state, that value will be retuned by each function to be placed in the PathVals array of the opposite, UNLESS
    that function is the original ROOT, in which case all of the summed up pathVals for each action will be returned for analysis. The index of the highest / lowest value
    is the one that will be take from the actions array.
    In order to win in as little steps as possible, somehow make terminal states that are closer worth less / more depending on your player. Empties attempts this
    """
    
    for act in acts:
        pathVals.append(maxVal(result(board,act), actions(result(board,act)), False))
    
    # sum the value of all paths and call it the state value, return that
    currLowest = INFINITE
    for i in pathVals:
        if i < currLowest:
            currLowest = i

    if not root:
        return currLowest * empties(board)
    else: 
        return pathVals


def maxVal(board, acts, root):
    # return max value of a state
    if terminal(board) == True:
        return utility(board)

    pathvals = []
    """
    # for every action recursively call the oppostie fucntion until utilities begin getting spit up, those utilities will begin to 
    anlyzed and the lowest will be chosen, being mutiplied by the return value of empties() which rewards lest steps. 
    that value will be retuned by each function to be placed in the PathVals array of the opposite, and then the oppostie function will analyze those
    values for its won purpose
    UNLESS
    that function is the original ROOT, in which case all of the summed up pathVals for each action will be returned for analysis. The index of the highest / lowest value
    is the one that will be take from the actions array.
    """
    for act in acts:
        pathvals.append(minVal(result(board,act), actions(result(board,act)), False))
    
    currGreatest = -INFINITE
    for i in pathvals:
        if i > currGreatest:
            currGreatest = i

    if not root:
        return currGreatest * empties(board)
    else: 
        return pathvals

def empties(board):
    amount = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                amount += 1

    return amount