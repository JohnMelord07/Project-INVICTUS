import random
import time

class Player:
    
    def __init__(self, symbol, board):
        self.__symbol = symbol
        self._gboard = board
        
    def get_player_symbol(self):
        return self.__symbol


class HumanPlayer(Player):
    
    def __init__(self, symbol, board):
        Player.__init__(self, symbol, board)
    
    def play(self):
        print("Player %s turn" % self.get_player_symbol())
        while True:
            col_input = input("Please enter column no (or 'save'): ")
            
            if col_input.lower() == "save":
                self._gboard.save_game()
                print("Game saved. Continue playing.")
                continue
            
            try:
                col = int(col_input)
            except ValueError:
                print("Invalid input. Please enter a number or 'save'.")
                continue
            
            if col < 0 or col >= self._gboard.get_num_cols():
                print("Invalid column. Please try again.")
                continue
        
            if not self._gboard.is_space_free(0, col):
                print("Column is full. Please try again.")
                continue
            
            self._gboard.make_move(col, self.get_player_symbol())
            break


class ComputerPlayer(Player):
    
    def __init__(self, symbol, board, buttons_2d_list=[], difficulty="medium", opponent_symbol=None):
        Player.__init__(self, symbol, board)
        self.buttons_2d_list = buttons_2d_list
        self.difficulty = difficulty
        self.opponent_symbol = opponent_symbol
    
    def play(self):
       
        if len(self.buttons_2d_list) > 0:
            self.__play_gui()
            return
        print("Player %s turn (Difficulty: %s)" % (self.get_player_symbol(), self.difficulty))
        time.sleep(2)
        col = self.__choose_column()
        self._gboard.make_move(col, self.get_player_symbol())
    
    def __play_gui(self):
        

        time.sleep(2)
        col = self.__choose_column()
        if self._gboard.is_space_free(0, col):
            for row in range(self._gboard.get_num_rows() - 1, -1, -1):
                button = self.buttons_2d_list[row][col]
                if button["text"] == " ":
                    button.invoke()
                    return
    
    def choose_column_gui(self):
        
        time.sleep(2)
        return self.__choose_column()
    
    def __get_opponent(self):
        if self.opponent_symbol is not None:
            return self.opponent_symbol
        for row in range(self._gboard.get_num_rows()):
            for col in range(self._gboard.get_num_cols()):
                sym = self._gboard.get_symbol_at(row, col)
                if sym != " " and sym != self.get_player_symbol():
                    return sym
        return "O" if self.get_player_symbol() == "X" else "X"
    
    def __choose_column(self):
        if self.difficulty == "easy":
            return self.__random_col()
        elif self.difficulty == "medium":
            return self.__find_strategic_col()
        elif self.difficulty == "advanced":
            return self.__find_advanced_col()
        else:
            return self.__random_col()
    
    def __random_col(self):
        num_cols = self._gboard.get_num_cols()
        while True:
            col = random.randint(0, num_cols - 1)
            if self._gboard.is_space_free(0, col):
                return col
    
    def __find_strategic_col(self):
        num_cols = self._gboard.get_num_cols()
        
        for col in range(num_cols):
            if self._gboard.is_space_free(0, col):
                if self._gboard.try_move(col, self.get_player_symbol()):
                    return col
        
        opponent = self.__get_opponent()
        for col in range(num_cols):
            if self._gboard.is_space_free(0, col):
                if self._gboard.try_move(col, opponent):
                    return col
        
        return self.__random_col()
    
    
    def __find_advanced_col(self):
        num_cols = self._gboard.get_num_cols()
        opponent = self.__get_opponent()
        
        for col in range(num_cols):
            if self._gboard.is_space_free(0, col):
                if self._gboard.try_move(col, self.get_player_symbol()):
                    return col
        for col in range(num_cols):
            if self._gboard.is_space_free(0, col):
                if self._gboard.try_move(col, opponent):
                    return col
        
        best_score = -999999
        best_col = -1
        centre_col = num_cols // 2
        
        for col in range(num_cols):
            if self._gboard.is_space_free(0, col):
                self._gboard.make_move(col, self.get_player_symbol())
                score = self.__minimax(3, False, opponent)
                self._gboard.undo_top_move(col)
                
                centre_bonus = (num_cols - abs(col - centre_col)) * 2
                score += centre_bonus
                
                if score > best_score:
                    best_score = score
                    best_col = col
        
        if best_col == -1:
            return self.__random_col()
        return best_col
    
    
    def __minimax(self, depth, is_maximizing, opponent):
        if self._gboard.check_winner():
            if is_maximizing:
                return -10000
            else:
                return 10000
        
        if self._gboard.is_board_full():
            return 0
        
        if depth == 0:
            return self.__score_position(opponent)
        
        num_cols = self._gboard.get_num_cols()
        
        if is_maximizing:
            best_score = -999999
            for col in range(num_cols):
                if self._gboard.is_space_free(0, col):
                    self._gboard.make_move(col, self.get_player_symbol())
                    score = self.__minimax(depth - 1, False, opponent)
                    self._gboard.undo_top_move(col)
                    if score > best_score:
                        best_score = score
            return best_score
        else:
            best_score = 999999
            for col in range(num_cols):
                if self._gboard.is_space_free(0, col):
                    self._gboard.make_move(col, opponent)
                    score = self.__minimax(depth - 1, True, opponent)
                    self._gboard.undo_top_move(col)
                    if score < best_score:
                        best_score = score
            return best_score
    
    
    def __score_position(self, opponent):
        score = 0
        my_sym = self.get_player_symbol()
        num_rows = self._gboard.get_num_rows()
        num_cols = self._gboard.get_num_cols()
        
        for row in range(num_rows):
            for col in range(num_cols - 3):
                window = [self._gboard.get_symbol_at(row, col + i) for i in range(4)]
                score += self.__score_window(window, my_sym, opponent)
        
        for col in range(num_cols):
            for row in range(num_rows - 3):
                window = [self._gboard.get_symbol_at(row + i, col) for i in range(4)]
                score += self.__score_window(window, my_sym, opponent)
        
        for row in range(num_rows - 3):
            for col in range(num_cols - 3):
                window = [self._gboard.get_symbol_at(row + i, col + i) for i in range(4)]
                score += self.__score_window(window, my_sym, opponent)
        
        for row in range(num_rows - 3):
            for col in range(3, num_cols):
                window = [self._gboard.get_symbol_at(row + i, col - i) for i in range(4)]
                score += self.__score_window(window, my_sym, opponent)
        
        return score
    
    
    def __score_window(self, window, my_sym, opponent):
        my_count = window.count(my_sym)
        opp_count = window.count(opponent)
        empty_count = window.count(" ")
        
        if my_count > 0 and opp_count > 0:
            return 0
        
        if my_count == 3 and empty_count == 1:
            return 50
        if my_count == 2 and empty_count == 2:
            return 10
        
        if opp_count == 3 and empty_count == 1:
            return -80
        if opp_count == 2 and empty_count == 2:
            return -10
        
        return 0
    


