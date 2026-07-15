from gameboard import GameBoard
from player import HumanPlayer, ComputerPlayer
from gamegui import GameGUI

def main():
    
    print("Do you want to load a saved game? (y/n): ")
    load_choice = input().lower()
    
    loaded_data = None
    gboard = None
    
    if load_choice == "y":
        gboard = GameBoard()
        loaded_data = gboard.load_game()
        if loaded_data:
            print("Continuing from saved game.")
        else:
            print("Starting new game.")
            gboard = None
    

    if gboard is None:
        print("Choose grid size:")
        while True:
            try:
                num_rows = int(input("Enter number of rows (4 to 9): "))
                num_cols = int(input("Enter number of columns (4 to 9): "))
                if num_rows < 4 or num_cols < 4:
                    print("Both rows and columns must be at least 4. Try again.")
                    continue
                if num_rows > 9 or num_cols > 9:
                    print("Both rows and columns must be at most 9. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter whole numbers.")
        gboard = GameBoard(num_rows, num_cols)
        
    
    
    if loaded_data:
        mode = loaded_data["mode"]
        difficulty = loaded_data["difficulty"]
        p1_symbol = loaded_data["p1_symbol"]
        p2_symbol = loaded_data["p2_symbol"]
        
        print("Loaded mode: " + mode + ", difficulty: " + difficulty +
              ", P1: " + p1_symbol + ", P2: " + p2_symbol)
    else:
        
        
        
        print("Choose game mode:")
        print("\t 1. Human vs Human")
        print("\t 2. Human vs Computer")
        print("\t 3. Computer vs Computer")
        mode = input("Enter game mode (1, 2, or 3): ")
        while mode not in ["1", "2", "3"]:
            print("Invalid choice. Please enter 1, 2, or 3.")
            mode = input("Enter game mode (1, 2, or 3): ")
        
        
        difficulty = "medium"
        if mode in ["2", "3"]:
            print("Choose computer difficulty:")
            print("\t 1. Easy (random)")
            print("\t 2. Medium (strategic)")
            print("\t 3. Advanced (lookahead)")
            diff_input = input("Enter difficulty (1, 2, or 3): ")
            while diff_input not in ["1", "2", "3"]:
                print("Invalid choice. Please enter 1, 2, or 3.")
                diff_input = input("Enter difficulty (1, 2, or 3): ")
            
            if diff_input == "1":
                difficulty = "easy"
            elif diff_input == "2":
                difficulty = "medium"
            else:
                difficulty = "advanced"
        
        
        print("Player 1, choose your symbol (X or O): ")
        p1_symbol = input().upper()
        while p1_symbol not in ["X", "O"]:
            print("Invalid choice. Please choose X or O: ")
            p1_symbol = input().upper()
        
        p2_symbol = "O" if p1_symbol == "X" else "X"
    
    
    if mode == "1":
        print("Player 2 will be symbol: " + p2_symbol)
        p1 = HumanPlayer(p1_symbol, gboard)
        p2 = HumanPlayer(p2_symbol, gboard)
    elif mode == "2":
        print("Player 2 (Computer) will be symbol: " + p2_symbol)
        p1 = HumanPlayer(p1_symbol, gboard)
        p2 = ComputerPlayer(p2_symbol, gboard, [], difficulty, opponent_symbol=p1_symbol)
    else:
        print("Player 1 (Computer) will be symbol: " + p1_symbol)
        print("Player 2 (Computer) will be symbol: " + p2_symbol)
        p1 = ComputerPlayer(p1_symbol, gboard, [], difficulty, opponent_symbol=p2_symbol)
        p2 = ComputerPlayer(p2_symbol, gboard, [], difficulty, opponent_symbol=p1_symbol)
    
    
    players_lst = (p1, p2)
    
    winner = False
    
    gboard.show_board_dynamic()
    print("(Type 'save' anytime instead of a column number to save the game)")
    
    while winner == False:
        for p in players_lst:
            p.play()
            gboard.show_board_dynamic()
            
            winner = gboard.check_winner()
            
            if winner == True:
                print("Player " + p.get_player_symbol() + " wins!")
                break
            
            if gboard.is_board_full():
                print("It's a draw!")
                winner = True
                break


if __name__ == "__main__":
    print("Welcome to Connect4!")
    while True:
        print("Choose interface:")
        print("\t 1. Console")
        print("\t 2. GUI")
        choice = input("Enter number to choose interface or q to quit: ") # input turns things into a string
        if choice.lower() == "q":
            break
        if choice == "1":
            print("")
            main()
        elif choice == "2":
            b_gui = GameGUI()
            b_gui.initialise()
            break