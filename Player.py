# Finnegan Damore Johann
# 1611018
# fdamorej@ucsc.edu
# fdamorej



import numpy as np

#Check Final. Used to calculate the heuristic values of each set of 4 spaces. Called by Evaluation.
def CheckFinal(values, player):
    other = 2 / player
    otherPlayerVisible = (other in values)
    playerVisible = (player in values)
    if otherPlayerVisible == True and playerVisible == True:
        return 0
    elif otherPlayerVisible == True:
        temp =  (sum(values) / other)
        if temp == 4:
            return -10000
        else:
            return (temp ** 2) * -1
    elif playerVisible == True:
        temp =  sum(values)/ player
        if temp == 4:
            return 10000
        else:
            return temp ** 2
    return 0


class AIPlayer:
    ## Initializes AIP Player, added self.board which tracks new board used for alpha beta pruning and expectimax. diagonal board is used to create lists which hold the values of each diagonal on the board. Top number is used for pruning in alpha beta
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.board = []
        self.depth = 3
        self.diagonalBoard = []
        self.TopNumber = None
        self.quickChoose = None
        
    ## Checks to see if win condition is reached for a player based off of their number
    def game_completed(self, player_num, Board):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        board = Board
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        val =  (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))
        return val
    
    #Initialized and sets self.diagonal board to values holding each diagonal row of the board. Used to calculate heuristic costs
    def Diagonal(self, board):
        diagonalBoard = []
        tempBoard = []
        for l in range (3,6):
            x = 0
            for i in range(0, l+1):
                tempBoard.append(board[l-x][i])
                x += 1
            diagonalBoard.append(tempBoard[:])
            tempBoard[:] = []
        
        for l in range (1,4):
            x = 0
            for i in range(l, 7):
                tempBoard.append(board[5 - x][i])
                x += 1
            diagonalBoard.append(tempBoard[:])
            tempBoard[:] = []
        
        for l in range (0,3):
            x = 0
            for i in range(0, 6-l):
                tempBoard.append(board[l + x][i])
                x += 1
            diagonalBoard.append(tempBoard[:])
            tempBoard[:] = []
        
        for l in range (1,4):
            x = 0
            for i in range(l, 7):
                tempBoard.append(board[0 + x][i])
                x += 1
            diagonalBoard.append(tempBoard[:])
            tempBoard[:] = []
        return diagonalBoard
        

    #Player's Turn. Used to calculate the max value of different options. If not at deepest depth calls CombatBoard and for each possible position and takes the max value. If win condition is found when position is played, returns 1000
    def PlayerBoard(self , board, depth):
    
        if self.quickVictoryCheck(board, self.player_number) == True:
            return 1000
        
        evaluation = 0
        largestValues = []
        depth = depth + 1
        if depth < self.depth:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, self.player_number) != 1:
                    #if self.game_completed(self.player_number, self.board) == 1:
                        #return 1000
                    pathValue = self.CombatBoard(self.board, depth)
                    if pathValue != None:
                        largestValues.append(pathValue)
            if not largestValues:
                evaluation = 1
        if depth >= self.depth or evaluation == 1:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, self.player_number) != 1:
                    #if self.game_completed(self.player_number, self.board) == 1:
                       # return 1000
                    largestValues.append(self.evaluation_function( self.board))
            if not largestValues:
                return None
        return max(largestValues)
        
    #Player's Turn. Used to calculate the min value of different options. If not at deepest depth calls PlayerBoard and for each possible position and takes the min value. If loose condition is found when position is played, returns -1000
    def CombatBoard(self , board, depth):
    
        if self.quickVictoryCheck(board, int(2 /self.player_number)) == True:
            return -1000
            
        lowestValues = []
        depth = depth + 1
        evaluation = 0
        if depth < self.depth:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, 2 / self.player_number) != 1:
                   # if self.game_completed(int(2 / self.player_number), self.board) == True:
                        #return -1000
                    pathValue = self.PlayerBoard(self.board, depth)
                    if pathValue != None:
                        if self.TopNumber != None:
                            if pathValue < self.TopNumber:
                                return pathValue
                        lowestValues.append(pathValue)
            if not lowestValues:
                evaluation = 1
        if depth >= self.depth or evaluation == 1:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, 2 /self.player_number) != 1:
                    #if self.game_completed(int(2 / self.player_number), self.board) == True:
                        #return -1000
                    e = self.evaluation_function(self.board)
                    lowestValues.append(e)
            if not lowestValues:
                return None
            returningValue = min(lowestValues)
        return min(lowestValues)

    #Player's Turn. Used to calculate the max value of different options. If not at deepest depth calls CombatBoardRandom and for each possible position and takes the max value. If win condition is found when position is played, returns 1000
    def PlayerBoardRandom(self , board, depth):
        largestValues = []
        depth = depth + 1
        if depth < self.depth:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, self.player_number) != 1:
                    if self.game_completed(self.player_number, self.board) == 1:
                        return 1000
                    pathValue = self.CombatBoardRandom(self.board, depth)
                    if pathValue != None:
                        largestValues.append(pathValue)
            return max(largestValues)
        else:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, self.player_number) != 1:
                    if self.game_completed(self.player_number, self.board) == 1:
                        return 1000
                    largestValues.append(self.evaluation_function(self.board))
            return max(largestValues)
        
    #Player's Turn. Used to calculate the weighted average value of different options. If not at deepest depth calls playerBoardRandom and for each possible position and takes the weighted average value.
    def CombatBoardRandom(self , board, depth):
        lowestValues = []
        finalValue = 0
        depth = depth + 1
        if depth < self.depth:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, 2 / self.player_number) != 1:
                    pathValue = self.PlayerBoardRandom(self.board, depth)
                    lowestValues.append(pathValue)
            for i in range(len(lowestValues)):
                finalValue = finalValue + (lowestValues[i] / len(lowestValues))
            return finalValue
        else:
            for i in range(7):
                self.board = board.copy()
                if self.update_board(i, 2 /self.player_number) != 1:
                    e = self.evaluation_function(self.board)
                    lowestValues.append(e)
            for i in range(len(lowestValues)):
                finalValue = finalValue + (lowestValues[i] / len(lowestValues))
            return finalValue
       
    def update_board(self, move, player_num):
        if 0 in self.board[:,move]:
            update_row = -1
            for row in range(1, self.board.shape[0]):
                update_row = -1
                if self.board[row, move] > 0 and self.board[row-1, move] == 0:
                    update_row = row-1
                elif row==self.board.shape[0]-1 and self.board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    self.board[update_row, move] = player_num
                    break
        else:
            return 1
            raise Exception(err)
    
    def quickVictoryCheck(self,board,player):
        for i in range(7):
            self.board = board.copy()
            if self.update_board(i, player) != 1:
                if self.game_completed(player, self.board) == 1:
                    self.quickChoose = i
                    return True
                    
        return False
    
    
    #Function call of alpha beta algorithm
    def get_alpha_beta_move(self, board):
        values = []
        location = []
        print('alpha beta move')
        
        if self.quickVictoryCheck(board, self.player_number) == True:
            return self.quickChoose
            
        for i in range(7):
            print('.')
            self.board = board.copy()
            if self.update_board(i, self.player_number) != 1:
                if self.game_completed(self.player_number, self.board) == 1:
                    return i
                pathValue = self.CombatBoard(self.board, 0)
                if pathValue != None:
                    values.append(pathValue)
                    location.append(i)
                #Sets top number value to help prune within CombatBoard
                if self.TopNumber == None:
                    self.TopNumber = pathValue
                else:
                    if self.TopNumber <= pathValue:
                        self.TopNumber = pathValue
        print(values)
        print(location)
        value = location[values.index(max(values))]
        print(value)
        self.board = board.copy()
        self.update_board(value, self.player_number)
        print('placing in spot : ' , value)
        print('score of board is : ', self.evaluation_function(self.board))
        self.Diagonal(self.board)
        return value
        
        raise NotImplementedError('Whoops I don\'t know what to do')
        
    #Function call for expecimax algorithm
    def get_expectimax_move(self, board):
        values = []
        location = []
        for i in range(7):
            self.board = board.copy()
            if self.update_board(i, self.player_number) != 1:
                if self.game_completed(self.player_number, self.board) == 1:
                    return i
                pathValue = self.CombatBoardRandom(self.board, 0)
                if pathValue != None:
                    values.append(pathValue)
                    location.append(i)
        print(values)
        print(location)
        value = location[values.index(max(values))]
        print(value)
        return value
        raise NotImplementedError('Whoops I don\'t know what to do')



    #Evaluation Function. Used to calculate heuristic values of the board
    def evaluation_function(self, board):
        player = self.player_number
        curValue = 0
        tempValue = 0
        value = 0
        for l in range(6):
            Row = board[l]
            curValue = 0
            for i in range(4):
                curValue += CheckFinal(Row[i:i+4], self.player_number)
            value += curValue
        for l in range(7):
            Col = board[:,l]
            curValue = 0
            for i in range(3):
                curValue += CheckFinal(Col[i:i+4], self.player_number)
            value += curValue
    
        diagonalBoard = self.Diagonal(self.board)
        for i in range(len(diagonalBoard)):
            Diag = diagonalBoard[i]
            curValue = 0
            for l in range((len(diagonalBoard[i]) - 3)):
                curValue += CheckFinal(Diag[l:l+4], self.player_number)
            value += curValue
        return value
       
        return 0


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:


    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)
        self.board = []

    def get_move(self, board):
                
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

