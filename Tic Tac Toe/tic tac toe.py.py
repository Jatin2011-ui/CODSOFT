import numpy as np
from tkinter import Tk, Canvas

# Global variables
size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#0492CF'
symbol_O_color = '#EE4035'
Green_color = '#7BC043'
#EE4035
#0492CF

class Tic_Tac_Toe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)   

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def initialize_board(self):
         
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)
        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def click(self, event):
         
        if self.gameover or not self.player_X_turns:
            if self.reset_board:
                self.play_again()
            return

        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.is_grid_occupied(logical_position):
            self.draw_X(logical_position)
            self.board_status[logical_position[0]][logical_position[1]] = -1
            self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()
            else:
                 
                self.window.after(1000, self.ai_move)  

    def ai_move(self):
         
        best_score = -float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board_status[i][j] == 0:  # If the cell is empty
                    self.board_status[i][j] = 1   
                    score = self.minimax(depth=0, is_maximizing=False)
                    self.board_status[i][j] = 0   
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.draw_O(best_move)
            self.board_status[best_move[0]][best_move[1]] = 1
            self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()

    def minimax(self, depth, is_maximizing):
        if self.check_winner(1):  # AI wins
            return 1
        if self.check_winner(-1):  # Player wins
            return -1
        if self.is_tie():  # Tie
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board_status[i][j] == 0:
                        self.board_status[i][j] = 1
                        score = self.minimax(depth + 1, is_maximizing=False)
                        self.board_status[i][j] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board_status[i][j] == 0:
                        self.board_status[i][j] = -1
                        score = self.minimax(depth + 1, is_maximizing=True)
                        self.board_status[i][j] = 0
                        best_score = min(score, best_score)
            return best_score

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def is_gameover(self):
        self.X_wins = self.check_winner(-1)
        self.O_wins = self.check_winner(1)
        self.tie = not np.any(self.board_status == 0) and not self.X_wins and not self.O_wins
        self.gameover = self.X_wins or self.O_wins or self.tie
        return self.gameover

    def check_winner(self, player):
        for i in range(3):
            if all(self.board_status[i, :] == player) or all(self.board_status[:, i] == player):
                return True
        if self.board_status[0, 0] == self.board_status[1, 1] == self.board_status[2, 2] == player:
            return True
        if self.board_status[0, 2] == self.board_status[1, 1] == self.board_status[2, 0] == player:
            return True
        return False

    def is_tie(self):
        return not np.any(self.board_status == 0)

    def display_gameover(self):
        if self.X_wins:
            text = 'Player X Wins!'
            color = symbol_X_color
        elif self.O_wins:
            text = 'Player O Wins!'
            color = symbol_O_color
        else:
            text = 'It\'s a Tie!'
            color = 'gray'

        # Overlay the game-over message on the board
        self.canvas.create_rectangle(0, size_of_board / 3 - 50, size_of_board, size_of_board / 3 + 50, fill='white', outline='white')
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 40 bold", fill=color, text=text)

        # Add a "play again" prompt
        self.canvas.create_text(size_of_board / 2, size_of_board / 2 + 100, font="cmr 20 bold", fill="gray",
                                text="Click anywhere to play again")

        # Set the reset flag to true
        self.reset_board = True

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_turns = True
        self.reset_board = False
        self.gameover = False

    def mainloop(self):
        self.window.mainloop()


# Create and run the game instance
game_instance = Tic_Tac_Toe()
game_instance.mainloop()
