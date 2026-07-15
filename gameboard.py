class GameBoard:
    
    def __init__(self, num_rows= 6, num_cols= 7):
        self.__space = ' '
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__board = []
            
        for i in range(self.__num_rows):
            row = [self.__space] * self.__num_cols
            self.__board.append(row)
        
        # Metadata for save/load — set by game setup via set_metadata()
        self.__mode = "2"
        self.__difficulty = "medium"
        self.__p1_symbol = "X"
        self.__p2_symbol = "O"
        self.__current_player_index = 0
    
    
    def get_num_rows(self):
        return self.__num_rows
    
    def get_num_cols(self):
        return self.__num_cols
    

    def set_metadata(self, mode, difficulty, p1_symbol, p2_symbol, current_player_index=0):
        
        self.__mode = mode
        self.__difficulty = difficulty
        self.__p1_symbol = p1_symbol
        self.__p2_symbol = p2_symbol
        self.__current_player_index = current_player_index
    
    
    def update_current_player_index(self, index):
       
        self.__current_player_index = index
    
    
    def is_board_full(self):
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.is_space_free(row, col):
                    return False
        return True
    
    
    def is_space_free(self, row, col):
        return self.__board[row][col] == self.__space
    
    def get_symbol_at(self, row, col):
        return self.__board[row][col]
    
    def try_move(self, col, element):
        
        for row in range(self.__num_rows - 1, -1, -1):
            if self.is_space_free(row, col):
                self.__board[row][col] = element
                won = self.check_winner()
                self.__board[row][col] = self.__space
                return won
        return False
    
    
    def make_move(self, col, element):
        for row in range(self.__num_rows - 1, -1, -1):
            if self.is_space_free(row, col):
                self.__board[row][col] = element
                return
            

    def undo_top_move(self, col):
        
        for row in range(self.__num_rows):
            if self.__board[row][col] != self.__space:
                self.__board[row][col] = self.__space
                return       
    

    def show_board_dynamic(self):
        for row in range(self.__num_rows):
            self.__print_horizontal_line()
            print("|", end="")
            for col in range(self.__num_cols):
                print(" " + self.__board[row][col] + " |", end="")
            print("")
        self.__print_horizontal_line()
        print(" ", end="")
        for col in range(self.__num_cols):
            print(" " + str(col) + "  ", end="")
        print("")
    
    
    def __print_horizontal_line(self):
        print("+", end="")
        for i in range(self.__num_cols):
            end = "+"
            print("---", end=end)
        print("")
    
    
    def check_winner(self):
        return self.__check_winner_hz() or self.__check_winner_vt() \
            or self.__check_winner_diag1() or self.__check_winner_diag2()
    
    
    def __check_winner_hz(self):
        for row in range(self.__num_rows):
            for col in range(self.__num_cols - 3):
                symbol = self.__board[row][col]
                if symbol != self.__space:
                    if (symbol == self.__board[row][col+1] and
                        symbol == self.__board[row][col+2] and
                        symbol == self.__board[row][col+3]):
                        return True
        return False
    
    
    def __check_winner_vt(self):
        for row in range(self.__num_rows - 3):
            for col in range(self.__num_cols):
                symbol = self.__board[row][col]
                if symbol != self.__space:
                    if (symbol == self.__board[row+1][col] and
                        symbol == self.__board[row+2][col] and
                        symbol == self.__board[row+3][col]):
                        return True
        return False
    
    
    def __check_winner_diag1(self):
        
        for row in range(self.__num_rows - 3):
            for col in range(self.__num_cols - 3):
                symbol = self.__board[row][col]
                if symbol != self.__space:
                    if (symbol == self.__board[row+1][col+1] and
                        symbol == self.__board[row+2][col+2] and
                        symbol == self.__board[row+3][col+3]):
                        return True
        return False
    
    
    def __check_winner_diag2(self):
        
        for row in range(self.__num_rows - 3):
            for col in range(3, self.__num_cols):
                symbol = self.__board[row][col]
                if symbol != self.__space:
                    if (symbol == self.__board[row+1][col-1] and
                        symbol == self.__board[row+2][col-2] and
                        symbol == self.__board[row+3][col-3]):
                        return True
        return False
    
    
    def save_game(self, filename="saved_game.txt"):
        
        with open(filename, "w") as f:
            
            f.write(str(self.__num_rows) + " " + str(self.__num_cols) + "\n")
            
            f.write(self.__mode + " " + self.__difficulty + " " +
                    self.__p1_symbol + " " + self.__p2_symbol + " " +
                    str(self.__current_player_index) + "\n")
            
            for row in range(self.__num_rows):
                line = ""
                for col in range(self.__num_cols):
                    line += self.__board[row][col]
                f.write(line + "\n")
        print("Game saved to " + filename)


    def load_game(self, filename="saved_game.txt"):
        
        try:
            with open(filename, "r") as f:
                
                first_line = f.readline().strip().split()
                self.__num_rows = int(first_line[0])
                self.__num_cols = int(first_line[1])
                
                
                meta_line = f.readline().strip().split()
                mode = meta_line[0]
                difficulty = meta_line[1]
                p1_symbol = meta_line[2]
                p2_symbol = meta_line[3]
                current_player_index = int(meta_line[4])
                
                
                self.__mode = mode
                self.__difficulty = difficulty
                self.__p1_symbol = p1_symbol
                self.__p2_symbol = p2_symbol
                self.__current_player_index = current_player_index
                
                
                self.__board = []
                for row in range(self.__num_rows):
                    line = f.readline().rstrip("\n")
                    line = line.ljust(self.__num_cols)
                    row_list = []
                    for col in range(self.__num_cols):
                        row_list.append(line[col])
                    self.__board.append(row_list)
            
            print("Game loaded from " + filename)
            return {
                "mode": mode,
                "difficulty": difficulty,
                "p1_symbol": p1_symbol,
                "p2_symbol": p2_symbol,
                "current_player_index": current_player_index
            }
        except FileNotFoundError:
            print("Save file not found: " + filename)
            return None
        except Exception as e:
            print("Error loading game: " + str(e))
            return None

        
        
        
        