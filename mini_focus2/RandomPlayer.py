import random

class RandomPlayer: 
    
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
		#a random element of the list         
    def get_random_empty_field(self, list):    
        return random.choice(list)
		
    #Args:
		#list: the board of the game
    #Returns:
		#a list with indexes where the on top piece belongs to the max player 
    def get_players_tower(self, list):
        list2 = []
        i = 0
        for x in list:
            if x is not None and len(x)>0:
                if x[-1] == "max":
                    list2.append(i)
            i += 1
            
        return list2    
    
	#This function returns all the possible moves that a tower has
	#Args:
		#index: the index of the tower
		#size_tower: the size of the tower
		#size_board: the size of the board
    #Returns:
		#a hash where the key i is the index and the value is the amount of pieces that can be moved
    def phasetwo_single_tower_move(self, index, size_tower,size_board):
        list = {}
        if index<size_board-1:
            for x in range(index+1, index+size_tower+1):
                if x >= 0:
                    list[x] = abs(x-index)
        if index>0:
            for y in range (index - 1, index - size_tower-1,-1):
                if y < size_board:
                    list[y] = abs(y-index)
        return list
             
    def phasetwo_decider(self,board):
        tower_index = random.choice(self.get_players_tower(board))
        tower= board[tower_index]
        move= self.phasetwo_single_tower_move(tower_index,len(tower),len(board))
        return [move,random.choice(move.keys()),tower_index]
    
   
    def utility(self, new_state, previous_state):
        p_number_of_max = 0
        p_number_of_min = 0
        n_number_of_max = 0
        n_number_of_min = 0
        for x in previous_state[1]:
            if len[x] > 0 and x is not None:
                if x[-1] == "max":
                    p_number_of_max += 1
                else:
                    p_number_of_min += 1
        for y in new_state[1]:
            if len[y] > 0 and y is not None:
                if y[-1] == "max":
                    n_number_of_max += 1
                else:
                    n_number_of_min += 1       
        
        if p_number_of_max < n_number_of_max:
            return 1
        elif p_number_of_max > n_number_of_max:
            return -1
        else:
            return 0
	
    #This function checks every piece that is on the top of a tower 
	#and if these pieces are of the same colour that means that the state is terminal 	
    #Args:
		#state: the state of the game which is the list 
	#Returns:
		#1 if the state is terminal(the game has finished) and 0 if the state is not terminal
    def terminal(self, state):
        min = 0
        max = 0
        for x in state[1]:
            if len[x] > 0 and x is not None:
                if x[-1] == "max":
                    max += 1
                else:
                    min += 1
        if min == 0 or max == 0:
            return 1
        else:
            return 0
        
    def alphabeta(self,node,depth,a,b,player):
        if depth == 0 or self.teminal==1:
            return "X0"
        
        tower= self.get_players_tower
        children = 
        
        if player == "max":
            return "max"
        else:
            return "minx"
        
        
    def move(self, state):        
        pieces = state[2]
        if pieces[0] > 0:
            hand_pieces = [(pieces[0]-1), pieces[1]]
            self.board  = state[1]
            self.board[self.get_random_empty_field(self.get_empty_fields(state[1]))] = ['max']
            return ("min", self.board, hand_pieces)
        else:
            if self.terminal == 1: #if there is no possible moves it will return the state it took
                return state
            
            self.board  = state[1]
            move = self.phasetwo_decider(self.board) 
            list_move_pieces = []
            if move[1]>move[2]:
                for x in range(move[2],move[1]):
                    list_move_pieces.append(self.board[x][-1])
                    del self.board[move[2]][-1] 
            else:
                for y in range(move[2],move[1],-1):
                    list_move_pieces.append(self.board[y][-1])
                    del self.board[move[2]][-1] 
            
            if isinstance(self.board[move[1]], list):
                self.board[move[1]].append(list_move_pieces)
            else:
                self.board[move[1]] = list_move_pieces
        return ('min',self.board,state[2])
            
        
          