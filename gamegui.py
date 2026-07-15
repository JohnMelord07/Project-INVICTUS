import tkinter
from sys import exit
from tkinter import messagebox
from tkinter import simpledialog
from gameboard import GameBoard
from player import HumanPlayer
from player import ComputerPlayer


class GameGUI:
        
    def __init__(self):
        self.mw = tkinter.Tk()
        
        self.is_processing = False # at start game is free to accept clicks
    

    def clicked_btn(self, x, y):
        
        if self.is_processing:
            return
        

        p = self.players_lst[self.current_player_index]
        

        if not isinstance(p, HumanPlayer):
            return
        # if p is H, which is humanplayer, so its true
        #not flips it to false, if false, return do nothing - H can click
        

        button = self.buttons_2d_list[x][y]
        if button["text"] != " ": # if button is occupied, stop user cliking occupied space
            return
        

        self.is_processing = True # Move starts, right now busy, can't accept more clicks
        try:
            self.__process_move(y, p.get_player_symbol())
            
        
            if self.current_player_index < len(self.players_lst):
                next_player = self.players_lst[self.current_player_index]
                if isinstance(next_player, ComputerPlayer):
                    self.__run_ai_turn(next_player)
        finally:
            self.is_processing = False
    
    
    def __process_move(self, col, symbol):
       
        self.gboard.make_move(col, symbol)
        self.update_button_text(col, symbol)
        self.mw.update()
        
        if self.gboard.check_winner():
            win_messge = ("Player %s is the Winner!" % symbol)
            messagebox.showinfo("Winner Info ", win_messge)
            self.mw.destroy()
            exit()
        
        if self.gboard.is_board_full():
            messagebox.showinfo("Game Info", "The board is full. It's a draw!")
            self.mw.destroy()
            exit()
        
        
        # This keeps turn cycling between players
        self.current_player_index += 1
        if self.current_player_index >= len(self.players_lst):
            self.current_player_index = 0
        
        self.gboard.update_current_player_index(self.current_player_index)
    
    
    def __run_ai_turn(self, ai_player):
        
        col = ai_player.choose_column_gui()
        if col is None or not self.gboard.is_space_free(0, col):
            return
        
        self.__process_move(col, ai_player.get_player_symbol())
        
       
        if self.current_player_index < len(self.players_lst):
            next_player = self.players_lst[self.current_player_index]
            if isinstance(next_player, ComputerPlayer):
                self.__run_ai_turn(next_player)
    
    
    def update_button_text(self, col, element):
        target_row = -1
        for row in range(len(self.buttons_2d_list) - 1, -1, -1):
            if self.buttons_2d_list[row][col]["text"] == " ":
                target_row = row
                break
        
        if target_row == -1:
            return
        
        for row in range(target_row + 1):
            button = self.buttons_2d_list[row][col]
            button["text"] = element
            button.config(disabledforeground="black")
            self.mw.update()
            self.mw.after(100)
            
            if row < target_row:
                button["text"] = " "
                self.mw.update()
        
        final_button = self.buttons_2d_list[target_row][col]
        final_button["text"] = element
        final_button.config(state="disabled", disabledforeground="black")
    
    
    def restart_game(self):
        self.mw.destroy()
        new_game = GameGUI()
        new_game.initialise()
    
    
    def save_clicked(self):
        self.gboard.update_current_player_index(self.current_player_index)
        self.gboard.save_game()
        messagebox.showinfo("Save Game", "Game saved to saved_game.txt")
    
    
    def load_clicked(self):
        result = self.gboard.load_game()
        if result is None:
            messagebox.showerror("Load Game", "No saved game found.")
            return
        
        loaded_board = self.gboard
        mode = result["mode"]
        difficulty = result["difficulty"]
        p1_symbol = result["p1_symbol"]
        p2_symbol = result["p2_symbol"]
        current_player_index = result["current_player_index"]
        
        self.mw.destroy()
        
        new_game = GameGUI()
        new_game.mode = mode
        new_game.difficulty = difficulty
        new_game.p1_symbol = p1_symbol
        new_game.p2_symbol = p2_symbol
        
        new_game.buttons_2d_list = []
        for i in range(loaded_board.get_num_rows()):
            row = [' '] * loaded_board.get_num_cols()
            new_game.buttons_2d_list.append(row)
        
        if mode == "1":
            p1 = HumanPlayer(p1_symbol, loaded_board)
            p2 = HumanPlayer(p2_symbol, loaded_board)
        elif mode == "2":
            p1 = HumanPlayer(p1_symbol, loaded_board)
            p2 = ComputerPlayer(p2_symbol, loaded_board, new_game.buttons_2d_list, difficulty, opponent_symbol=p1_symbol)
        else:
            p1 = ComputerPlayer(p1_symbol, loaded_board, new_game.buttons_2d_list, difficulty, opponent_symbol=p2_symbol)
            p2 = ComputerPlayer(p2_symbol, loaded_board, new_game.buttons_2d_list, difficulty, opponent_symbol=p1_symbol)
        
        players_lst = (p1, p2)
        
        new_game._GameGUI__initialise_game(loaded_board, players_lst, current_player_index)
        
        for row in range(loaded_board.get_num_rows()):
            for col in range(loaded_board.get_num_cols()):
                symbol = loaded_board.get_symbol_at(row, col)
                button = new_game.buttons_2d_list[row][col]
                if symbol != " ":
                    button["text"] = symbol
                    button.config(state="disabled", disabledforeground="black")
        
        messagebox.showinfo("Load Game", "Game loaded from saved_game.txt")
        tkinter.mainloop()
    
    
    def __initialise_game(self, gboard, players_lst, current_player_index=0):
        self.gboard = gboard
        self.players_lst = players_lst
        self.current_player_index = current_player_index
        
        self.winner = False
        
        for row in range(gboard.get_num_rows()):
            for col in range(gboard.get_num_cols()):
                button = tkinter.Button(
                    self.mw,
                    text=" ",
                    width=4,
                    height=2,
                    command=lambda x=row, y=col: self.clicked_btn(x, y)
                )
                button.grid(row=row, column=col)
                self.buttons_2d_list[row][col] = button
        
        num_cols = gboard.get_num_cols()

        save_btn = tkinter.Button(
            self.mw,
            text="Save Game",
            width=15,
            height=2,
            command=self.save_clicked,
            bg="lightgreen"
        )
        save_btn.grid(row=gboard.get_num_rows(), column=0, columnspan=num_cols, sticky="ew")

        load_btn = tkinter.Button(
            self.mw,
            text="Load Game",
            width=15,
            height=2,
            command=self.load_clicked,
            bg="lightyellow"
        )
        load_btn.grid(row=gboard.get_num_rows() + 1, column=0, columnspan=num_cols, sticky="ew")

        restart_btn = tkinter.Button(
            self.mw,
            text="Restart Game",
            width=15,
            height=2,
            command=self.restart_game,
            bg="lightblue"
        )
        restart_btn.grid(row=gboard.get_num_rows() + 2, column=0, columnspan=num_cols, sticky="ew")
        
        self.gboard.update_current_player_index(self.current_player_index)
        
        
        current_player = self.players_lst[self.current_player_index]
        if isinstance(current_player, ComputerPlayer):
            self.is_processing = True
            try:
                self.__run_ai_turn(current_player)
            finally:
                self.is_processing = False
    
    
    def initialise(self):
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