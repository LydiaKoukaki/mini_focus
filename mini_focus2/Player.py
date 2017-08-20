import random

class Player: 
    
    def __init__(self, name): 
        self.name = name
        self.board = None
	
    #This function is for the phase one of the game
    #Args:
	#list: the board of the game
    #Returns: 
        #a list with indexes of the fields that have none value 
    def get_empty_fields(self, list):      
        list2 = []
        i = 0
        for x in list:
            if x == None:
                list2.append(i)
            i += 1
            
        return list2    
		
    #Args:
	#list: a list with the empty fields of the board
    #Returns: 
	#a random choice of the list         
    def get_random_empty_field(self, list):    
        return random.choice(list)
		
    #Args:
	#list: the board of the game
        #player:
    #Returns:
	#a list with indexes where the on top piece belongs to the max player 
    def get_players_tower(self, list, player):
        list2 = []
        i = 0
        for x in list:
            if x is not None and len(x)>0:
                if x[-1] == player:
                    list2.append(i)
            i += 1
            
        return list2    
    
    #This function returns all the possible moves that a tower has
    #Args:
	#index: the index of the tower
	#size_tower: the size of the tower
	#size_board: the size of the board
    #Returns:
	#a list where the first element is the number of pieces that will be moved
        #the second element is in which index the pieces will be moved
        #and the third element is from which index the pieces will be moved
    def phasetwo_single_tower_move(self, index, size_tower,size_board):
        list = []
        if index<size_board-1:
            for x in range(index+1, index+size_tower+1):
                if x >= 0:
                    list.append([abs(x-index),x,index])
        if index>0:
            for y in range (index - 1, index - size_tower-1,-1):
                if y < size_board:#maybe a problem not going until the end
                   list.append([abs(y-index),y,index])
        return list
    
    #This function returns all the possible moves that a player can do
    #Args:        
        #board: the board of the game
        #player: max or min
    #Returns: a list from the function phasetwo_single_tower_move 
    def all_moves(self,board,player):
        list = []
        towers=self.get_players_tower(board,player);
        for x in towers:
            arr=self.phasetwo_single_tower_move(x,len(board[x]),len(board))
            list.append(arr[0])
            if len(arr)>1:
                list.append(arr[1])
        return list
    
    #This function takes the board of the game and a move in order to append 
    #the board according to this move
    #Args: 
        #move: a list where the first element is the number of pieces that will be moved
        #the second element is in which index the pieces will be moved
        #and the third element is from which index the pieces will be moved
        #player: min or max
        #board: the board of the game
    #Returns: the state of the game
    def phase_two_state(self,move,player,board):
        if move[1]>move[2]:
            i=1
            while i<=move[0]:
                i+=1
                if board[move[1]] is not None:
                    board[move[1]].append(player)
                else:
                    board[move[1]]=[player]
                del board[move[2]][-1] 
                
        else:
            j=move[0]
            while j>0:
                j-=1
                if board[move[1]] is not None:
                    board[move[1]].append(player)
                else:
                    board[move[1]]=[player]
                del board[move[2]][-1] 
        if player == "max":
            return ("min",board,[0,0])
        else:
            return ("max",board,[0,0])
    
    #This function takes all the possible moves and returns all the possible states 
    #Args: 
        #possible_moves: an array of possible moves
        #player: min or max
        #board: the board of the game
    #Returns: a list of states
    def get_list_of_possible_states(self,possible_moves,player,board):
        list = []
        for x in possible_moves:
            list.append(self.phase_two_state(x,player,board))
        return list
    
    #This function takes a state, looks how many more pieces max has from min and 
    #returns the state
    #Args: 
        #state: the state of the game
    #Returns: an integer that defines how good is the state
    def utility(self, state):
        number_of_max = 0
        number_of_min = 0
        for x in state[1]:
            if x is not None:
                if x[-1] == "max":
                    number_of_max += 1
                else:
                    number_of_min += 1    
        return number_of_max - number_of_min 
	
    #This function checks every piece that is on the top of a tower and if these pieces are of the same colour that means that the state is terminal 	
    #Args:
        #state: the state of the game which is the list 
    #Returns:
        #1 if the state is terminal(the game has finished) and 0 if the state is not terminal
    def terminal(self, state):
        min = 0
        max = 0
        for x in state[1]:
            if x is not None:
                if len(x) > 0:
                    if x[-1] == "max":
                        max += 1
                    else:
                        min += 1
        if min == 0 or max == 0:
            return 1
        else:
            return 0
     
    #This function uses minimax with alpha-beta pruning	
    #Args:   
        #state: the state of the game
        #depth: the depth of the search tree
        #alpha: the plus infinity
        #beta: the minus infinity
        #player: min or max
    #Returns: how good a move is
    def alphabeta(self,state,depth,alpha,beta,player):
        if depth == 0 or self.terminal(state)==1:
            return self.utility(state)
        if player== "max":
            possible_moves=self.all_moves(state[1],"max")
            for child in self.get_list_of_possible_states(possible_moves,"max",state[1]):
                alpha = max(a,self.alphabeta(child,depth-1,alpha,beta,"min"))
                if alpha>=beta:
                    break;
            return alpha
        else:
            possible_moves=self.all_moves(state[1],"max")
            for child in self.get_list_of_possible_states(possible_moves,"max",state[1]):
                beta = min(beta,self.alphabeta(child,depth-1,alpha,beta,"max"))
                if alpha>=beta:
                    break;
            return beta
    
    #This function takes a state of the game, calculates the most correct move 
    #and returns the new state with the new move
    #Args:
        #state: the state of the game
    #Returns: the new state
    def move(self, state):        
        pieces = state[2]
        if pieces[0] > 0:#check if it is the phase one of the game
            hand_pieces = [(pieces[0]-1), pieces[1]]
            self.board  = state[1]
            self.board[self.get_random_empty_field(self.get_empty_fields(state[1]))] = ['max']
            return ("min", self.board, hand_pieces)
        else:#phase 2 of the game
            if self.terminal == 1: #if there are no possible moves it will return the state it took
                return state
            possible_moves=self.all_moves(state[1],"max")
            possiblestate=self.get_list_of_possible_states(possible_moves,"max",state[1])
            i=0;
            max=self.alphabeta(possiblestate[0],4,999999,-99999,"max")
            #calculate the best possible state by using the alphabeta algorithm
            for x in range(1,len(possiblestate)):
                temp=self.alphabeta(possiblestate[x],4,999999,-99999,"max")
                if temp>max:
                    i=x
                    max=temp
        return possiblestate[i]
            
        
                 
          