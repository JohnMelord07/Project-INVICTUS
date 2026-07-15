'''

This file creates the graphical window and controls 
for a Connect 4 game using Pythons tkinter library.

It connects the visual buttons on the screen 
to the game logic stored in gameboard.py and player.py.

'''

import tkinter #creates windows and buttons
from sys import exit # stops the whole program
from tkinter import messagebox #displays pop-up messages
from tkinter import simpledialog #asks user questions in pop-up boxes
from gameboard import GameBoard #controls the Connect4 board and rules
from player import HumanPlayer #Represents a human
from player import ComputerPlayer #Repsnts the AI player

'''
The lines above bring the code from other places
'''


class GameGUI:
    #this class contains everything needed 
    # to create and control the graphical version 
    # of the game.
        
    def __init__(self): #runs when GameGUI object created.
        self.mw = tkinter.Tk()
        self.is_processing = False # Allows user to make click at start of game.


    def clicked_btn(self, x, y): #this function runs whenever the user clicks a board button.
        
        if self.is_processing: # currently false so interpreter oves onto the next code inside the function.
        
            return #However, the moment user clicks, return is active and so interpreter leaves this function :o
        
        p = self.players_lst[self.current_player_index] #players_lst contains 2 players.
        

        if not isinstance(p, HumanPlayer):
            return
        # if p is not human, the escape this function. If p is human, continue with this conditional flow. 

        

        button = self.buttons_2d_list[x][y]
        if button["text"] != " ": # if button is occupied, stop user cliking occupied space
            return
        

        self.is_processing = True # Move starts, right now busy, can't accept more clicks
        try:
            self.__process_move(y, p.get_player_symbol()) #sends the y coordinate ( selected column) to __process_move ( see the function down below). The y coordinate is used because the dosh falls down to the available space depending on the column chosen.
            
        
            if self.current_player_index < len(self.players_lst): #len will alweys be 2.
                next_player = self.players_lst[self.current_player_index]
                if isinstance(next_player, ComputerPlayer):
                    self.__run_ai_turn(next_player)
            'After human finishes, the program checks if next player is Comp. If it is AI runs it.'

        finally:
            self.is_processing = False
        # Runs whether the move succeeds or an error occurs. Makes human clicking available again.
    
    
    def __process_move(self, col, symbol): #processes the main steps of a turn.
       
        self.gboard.make_move(col, symbol) #Tells gameboard to place the symbol into the chosen column.
        self.update_button_text(col, symbol)
        self.mw.update()
        'The 2 lines above show the piece dropping into the selected column.'
        
        if self.gboard.check_winner(): #check for winnar
            win_messge = ("Player %s is the Winner!" % symbol)
            messagebox.showinfo("Winner Info ", win_messge)
            self.mw.destroy()
            exit()
        
        if self.gboard.is_board_full(): #check for draw
            messagebox.showinfo("Game Info", "The board is full. It's a draw!")
            self.mw.destroy()
            exit()
        
        
        # This keeps turn cycling between players :o
        self.current_player_index += 1
        if self.current_player_index >= len(self.players_lst): #len is alweys 2.
            self.current_player_index = 0 #if index is 3, it becomes 0.
        
        self.gboard.update_current_player_index(self.current_player_index) #useful for when saving the game.
    
    
    def __run_ai_turn(self, ai_player): # This method controls the AI's move.
        
        col = ai_player.choose_column_gui() #The AI chooses a column.
        if col is None or not self.gboard.is_space_free(0, col): # move is rejected if AI didn't choose a column or if column is full.
            return
        
        self.__process_move(col, ai_player.get_player_symbol())
        
       
        if self.current_player_index < len(self.players_lst):
            next_player = self.players_lst[self.current_player_index]
            if isinstance(next_player, ComputerPlayer):
                self.__run_ai_turn(next_player)
        'Checks if the next play is also a computer too'
    
    def update_button_text(self, col, element): #This method creates the visual effect of the piece falling down a column.
        target_row = -1 # initially means no available row has been found.
        
        for row in range(len(self.buttons_2d_list) - 1, -1, -1): #This loops from the bottom row upwards.
            if self.buttons_2d_list[row][col]["text"] == " ":
                target_row = row
                break
        
        if target_row == -1:
            return
        
        for row in range(target_row + 1): #The program moves down the column one row at a time.
            button = self.buttons_2d_list[row][col]
            button["text"] = element
            button.config(disabledforeground="black")
            self.mw.update()
            self.mw.after(100)
            'It temporarily places the symbol in each row and waits 100 milliseconds.'
            
            if row < target_row:
                button["text"] = " "
                self.mw.update()
                'these lines help to clear the previous positions where the dosh has passed through until it reaches the correct row'
        
        final_button = self.buttons_2d_list[target_row][col]
        final_button["text"] = element
        final_button.config(state="disabled", disabledforeground="black")
        # Once the piece lands, the button is disabled so it cannot be selected again.
    
    
    def restart_game(self):
        self.mw.destroy()
        new_game = GameGUI()
        new_game.initialise()

    '''
    closes the current window;
    creates a new game window;
    starts the setup process again.
    '''
    
    
    def save_clicked(self): # This method runs when the user clicks Save Game.
        self.gboard.update_current_player_index(self.current_player_index) # Stores whose turn it currently is.
        self.gboard.save_game() # The board saves the game data, probably into saved_game.txt.
        messagebox.showinfo("Save Game", "Game saved to saved_game.txt")
        #The message gives user confirmation that the game has been saved.'
    
    
    def load_clicked(self): # This method helps to rebuild the entire game when load is clicked.
        result = self.gboard.load_game()
        if result is None: # If no saved files exists, run this logic

            messagebox.showerror("Load Game", "No saved game found.")
            return
        
        loaded_board = self.gboard
        mode = result["mode"]
        difficulty = result["difficulty"]
        p1_symbol = result["p1_symbol"]
        p2_symbol = result["p2_symbol"]
        current_player_index = result["current_player_index"]

        '''
        The saved file contains information such as:
        the game mode
        AI Difficulty
        Player symbols
        Whose turn it is.
        '''

        self.mw.destroy() # close down the old window
        
        new_game = GameGUI() #new GUI is created for saved settings.
        new_game.mode = mode
        new_game.difficulty = difficulty
        new_game.p1_symbol = p1_symbol
        new_game.p2_symbol = p2_symbol
        
        # This is the section for creating the empty loaded game GUI
        new_game.buttons_2d_list = []
        for i in range(loaded_board.get_num_rows()): # This repeats once for every row in the saved board.
            row = [' '] * loaded_board.get_num_cols() # This creates one empty row with the correct number of columns.
            new_game.buttons_2d_list.append(row)
            
            'the line above adds that row into the full board structure.'

        # For example, if the loaded board is 6 rows by 7 columns, one row becomes:
        [' ', ' ', ' ', ' ', ' ', ' ', ' ']

        if mode == "1": # H v H
            p1 = HumanPlayer(p1_symbol, loaded_board)
            p2 = HumanPlayer(p2_symbol, loaded_board)
        elif mode == "2":
            p1 = HumanPlayer(p1_symbol, loaded_board)
            p2 = ComputerPlayer(p2_symbol, loaded_board, new_game.buttons_2d_list, difficulty, opponent_symbol=p1_symbol)
        else:
            p1 = ComputerPlayer(p1_symbol, loaded_board, new_game.buttons_2d_list, difficulty, opponent_symbol=p2_symbol)
            p2 = ComputerPlayer(p2_symbol, loaded_board, new_game.buttons_2d_list, difficulty, opponent_symbol=p1_symbol)
        
        players_lst = (p1, p2) #*
        
        new_game._GameGUI__initialise_game(loaded_board, players_lst, current_player_index) # This recreates the board window.
        
        # The code below is used to restore the symbols
        # The code checks every position on the loaded board.
        # If a position contains X or O, it places that symbol back onto the matching GUI button.
        for row in range(loaded_board.get_num_rows()):
            for col in range(loaded_board.get_num_cols()):
                symbol = loaded_board.get_symbol_at(row, col)
                button = new_game.buttons_2d_list[row][col]
                if symbol != " ":
                    button["text"] = symbol
                    button.config(state="disabled", disabledforeground="black")
        
        messagebox.showinfo("Load Game", "Game loaded from saved_game.txt")
        tkinter.mainloop()
    
    
    def __initialise_game(self, gboard, players_lst, current_player_index=0): # this method creates the actual Connect 4 buttons.
        self.gboard = gboard # stores
        self.players_lst = players_lst # important
        self.current_player_index = current_player_index # objects
        
        self.winner = False
        
        for row in range(gboard.get_num_rows()): # creates each board button in row and column, begins empty, fixed width and height, calls clicked_btn when clicked.
            for col in range(gboard.get_num_cols()):
                button = tkinter.Button(
                    self.mw,
                    text=" ",
                    width=4,
                    height=2,
                    command=lambda x=row, y=col: self.clicked_btn(x, y) 'stores the correct x and y positions for each button'
                )
                button.grid(row=row, column=col) # positions the button on the screen.
                self.buttons_2d_list[row][col] = button # Stores the button inside a 2-dimensional list.


        num_cols = gboard.get_num_cols()

        save_btn = tkinter.Button( # creates the control buttons
            self.mw,
            text="Save Game",
            width=15,
            height=2,
            command=self.save_clicked,
            bg="lightgreen"
        )
        save_btn.grid(row=gboard.get_num_rows(), column=0, columnspan=num_cols, sticky="ew")

        load_btn = tkinter.Button( # control buttons
            self.mw,
            text="Load Game",
            width=15,
            height=2,
            command=self.load_clicked,
            bg="lightyellow"
        )
        load_btn.grid(row=gboard.get_num_rows() + 1, column=0, columnspan=num_cols, sticky="ew")

        restart_btn = tkinter.Button( # control buttons
            self.mw,
            text="Restart Game",
            width=15,
            height=2,
            command=self.restart_game,
            bg="lightblue"
        )
        restart_btn.grid(row=gboard.get_num_rows() + 2, column=0, columnspan=num_cols, sticky="ew")
        
        self.gboard.update_current_player_index(self.current_player_index)
        
        
        current_player = self.players_lst[self.current_player_index] #Start the AI when necessary
        if isinstance(current_player, ComputerPlayer):
            self.is_processing = True
            try:
                self.__run_ai_turn(current_player)
            finally:
                self.is_processing = False
            # This is important for C v C matches
    
    
    def initialise(self): # setting up a new game #*#
        while True:
            num_rows = simpledialog.askinteger(
                "Grid Size",
                "Enter number of rows (4 to 9):",
                parent=self.mw,
                minvalue=4,
                maxvalue=9
            )
            if num_rows is None:
                num_rows = 6
            
            num_cols = simpledialog.askinteger(
                "Grid Size",
                "Enter number of columns (4 to 9):",
                parent=self.mw,
                minvalue=4,
                maxvalue=9
            )
            if num_cols is None:
                num_cols = 7
            
            if num_rows >= 4 and num_cols >= 4 and num_rows <= 9 and num_cols <= 9:
                break
            else:
                messagebox.showerror("Invalid Size", "Both rows and columns must be between 4 and 9.")


        gboard = GameBoard(num_rows, num_cols)
        
        self.buttons_2d_list = []
        for i in range(gboard.get_num_rows()):
            self.row = [' '] * gboard.get_num_cols()
            self.buttons_2d_list.append(self.row)
        
        
        mode = None
        while mode is None:
            mode_input = simpledialog.askstring(
                "Game Mode",
                "Choose mode:\n1. Human vs Human\n2. Human vs Computer\n3. Computer vs Computer",
                parent=self.mw
            )
            
            
            if mode_input is None:
                mode = "2"
                break
            
            cleaned = mode_input.strip()
            if cleaned in ["1", "2", "3"]:
                mode = cleaned
            else:
                messagebox.showerror(
                    "Invalid Mode",
                    "Please choose 1, 2, or 3."
                )

        
        difficulty = "medium"
        if mode in ["2", "3"]:
            diff = None
            while diff is None:
                diff_input = simpledialog.askstring(
                    "Difficulty",
                    "Choose computer difficulty:\n1. Easy (random)\n2. Medium (strategic)\n3. Advanced (lookahead)",
                    parent=self.mw
                )
                
                
                if diff_input is None:
                    diff = "medium"
                    break
                
                cleaned = diff_input.strip()
                if cleaned == "1":
                    diff = "easy"
                elif cleaned == "2":
                    diff = "medium"
                elif cleaned == "3":
                    diff = "advanced"
                else:
                    messagebox.showerror(
                        "Invalid Difficulty",
                        "Please choose 1, 2, or 3."
                    )
            
            difficulty = diff
        
        
        p1_symbol = None
        while p1_symbol is None:
            symbol_input = simpledialog.askstring(
                "Choose Symbol",
                "Player 1, choose your symbol (X or O):",
                parent=self.mw
            )
            
            if symbol_input is None:
                p1_symbol = "X"
                break
            
            cleaned = symbol_input.strip().upper()
            if cleaned == "X" or cleaned == "O":
                p1_symbol = cleaned
            else:
                messagebox.showerror(
                    "Invalid Symbol",
                    "Please choose either X or O."
                )
        
        p2_symbol = "O" if p1_symbol == "X" else "X"
        
        self.mode = mode
        self.difficulty = difficulty
        self.p1_symbol = p1_symbol
        self.p2_symbol = p2_symbol
        
        gboard.set_metadata(mode, difficulty, p1_symbol, p2_symbol, 0)
        
        if mode == "1":
            p1 = HumanPlayer(p1_symbol, gboard)
            p2 = HumanPlayer(p2_symbol, gboard)
        elif mode == "2":
            p1 = HumanPlayer(p1_symbol, gboard)
            p2 = ComputerPlayer(p2_symbol, gboard, self.buttons_2d_list, difficulty, opponent_symbol=p1_symbol)
        else:
            p1 = ComputerPlayer(p1_symbol, gboard, self.buttons_2d_list, difficulty, opponent_symbol=p2_symbol)
            p2 = ComputerPlayer(p2_symbol, gboard, self.buttons_2d_list, difficulty, opponent_symbol=p1_symbol)
        
        players_lst = (p1, p2)
        
        self._GameGUI__initialise_game(gboard, players_lst)
        
        tkinter.mainloop()


def main():
    b_gui = GameGUI()
    b_gui.initialise()
        
if __name__ == "__main__":
    main()