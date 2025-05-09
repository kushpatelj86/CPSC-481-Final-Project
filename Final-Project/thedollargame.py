import copy
import itertools
import random
from collections import namedtuple
import tkinter as tk
from tkinter import messagebox
import tkinter
import numpy as np




#used the ai algorithm you provided for Programming Project 2

def alpha_beta_search(state, game):
    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if game.terminal_test(state) or depth >= 10:
            return game.utility(state, player)
        v = -np.inf
        for a in sorted(game.actions(state), reverse=True):  # prioritize bigger moves
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if game.terminal_test(state) or depth >= 10:
            return game.utility(state, player)
        v = np.inf
        for a in sorted(game.actions(state), reverse=True):  # prioritize bigger moves

            v = min(v, max_value(game.result(state, a), alpha, beta,depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in sorted(game.actions(state), reverse=True):
        v = min_value(game.result(state, a), best_score, beta,depth=0)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action



#This is for the terminals

def query_player1(game, state):
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move





#This is for the gui


def query_player2(game, state, button):
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    move = None
    if game.actions(state):
        move_string = button
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move


def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)

#this is the game class you provided for programming project 2

class Game:
    def actions(self, state):
        raise NotImplementedError

    def result(self, state, move):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError

    def terminal_test(self, state):
        return not self.actions(state)

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


#this is the game class you provided for programming project 2

GameState = namedtuple('GameState', 'to_move, utility, board, coin_list, moves')



#this is the game class you provided for programming project 2

class RaceToDollar(Game):

    def __init__(self, target=1):
        allowed_moves=[0.01, 0.05, 0.10, 0.25]
        self.coin_types = {
            0.01 : "Penny",
            0.05 : "Nickel",
            0.10 : "Dime",
            0.25 : "Quarter",

        }
        self.target = target
        self.allowed_moves = [x for x in allowed_moves  if x <= target]
        coin_list={
            'Player 1': [], 
            'Player 2': []
            }
        
        self.initial = GameState(to_move='Player 1', utility=0, board={'Player 1': 0, 'Player 2': 0},coin_list=coin_list, moves=self.allowed_moves)

   
    def actions(self, state):
        return state.moves

    def result(self, state, move):
        """Apply move and return new state."""

        if move not in state.moves:
            return state
        


        current_player = state.to_move
        new_sum = state.board[current_player] + move
        new_board = state.board.copy()
        new_board[current_player] = round(new_sum,2)
        diff = self.target - new_board[current_player]
        diff = round(diff,2)
        print("diff ",diff)

        print("current_player ",current_player)
        print("current amount ",new_board[current_player])
        print("self.allowed_moves ",self.allowed_moves)



        new_moves =  [m for m in state.moves if m <= diff]
        print("new_moves ",new_moves)

        if current_player == 'Player 2': 
            next_player = 'Player 1'
        else:
            next_player = 'Player 2'


        next_player_diff = self.target - new_board[next_player]
        next_player_diff = round(next_player_diff,2)



        new_moves =  [m for m in state.moves if m <= next_player_diff]
        print("new_moves ",new_moves)


        new_coin_list = state.coin_list.copy()

        new_coin_list['Player 1'] = list(new_coin_list['Player 1'])
        new_coin_list['Player 2'] = list(new_coin_list['Player 2'])

        coin = self.coin_types[move]
        new_coin_list[current_player].append(coin)


        
        
        return GameState(
            to_move=next_player,
            utility=self.compute_utility(state) ,
            board=new_board,
            coin_list=new_coin_list,
            moves=new_moves
        )

    def compute_utility(self, state):
        if state.board['Player 1'] >= self.target:
            return +1 if state.to_move == 'Player 1' else -1

        else:
            return 0  
        

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'Player 1' else -state.utility


    def terminal_test(self, state):
        """Check if the game has reached a terminal state (a player has won)."""
        if state.utility != 0 or len(state.moves) == 0:
            return True
        else:
            return False



    def check_target(self, current_amount):
        return current_amount >= self.target_amount
    
    
    def display(self, state):
        print(f"Player 1's coin list: {state.coin_list['Player 1']} ")
        print(f"Player 2's coin list: {state.coin_list['Player 2']} ")

        print(f"Player 1's sum: {state.board['Player 1']}, Player 2's sum: {state.board['Player 2']}, Possible moves for {state.to_move}: {state.moves}")



#this is the main game

class GameGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Race to Dollar Game")
        self.geometry("400x300")
        self.state = self.game.initial

        self.player1_label = tk.Label(self, text="Player 1: $0.00")
        self.player1_label.pack()

        self.player2_label = tk.Label(self, text="Player 2: $0.00")
        self.player2_label.pack()

        self.player1_coin_label = tk.Label(self, text="Player 1 coins: []")
        self.player1_coin_label.pack()

        self.player2_coin_label = tk.Label(self, text="Player 2 coins: []")
        self.player2_coin_label.pack()
        

        self.current_player_label = tk.Label(self, text="Current Player: Player 1")
        self.current_player_label.pack()


        self.valid_moves = tk.Label(self, text=f"Valid moves: {self.state.moves}")
        self.valid_moves.pack()




        self.status_label = tk.Label(self, text="Game in progress...")
        self.status_label.pack()

        # Create a button for each allowed move
        self.move_buttons = []
        for move in self.game.allowed_moves:
            button = tk.Button(self, text=f"Take ${move:.2f}", command=lambda move=move: self.human_move(move))
            self.move_buttons.append(button)

        # Initially, hide the buttons until Player 2's turn
        for button in self.move_buttons:
            button.pack_forget()

        self.coin_type = {
            0.01: "Penny",
            0.05: "Nickel",
            0.10: "Dime",
            0.25: "Quarter",
        }

        self.after(5000, self.check_next_move)  # Start AI move checking

    def update_display(self):
        self.player1_label.config(text=f"Player 1: ${self.state.board['Player 1']:.2f}")
        self.player2_label.config(text=f"Player 2: ${self.state.board['Player 2']:.2f}")
        self.player1_coin_label.config(text=f"Player 1 coins: {self.state.coin_list['Player 1']}")
        self.player2_coin_label.config(text=f"Player 2 coins: {self.state.coin_list['Player 2']}")

        self.current_player_label.config(text=f"Current Player: {self.state.to_move}")
        self.valid_moves.config(text=f"Valid moves: {self.state.moves}")

        if self.game.terminal_test(self.state):
            if self.state.board['Player 1'] >= self.game.target:
                    winner = 'Player 1'
            else: 
                    winner = 'Player 2'
            self.status_label.config(text=f"{winner} won the game by reaching $ {self.state.board[winner]:.2f}!")
            messagebox.showinfo("Game Over", f"{winner} won the game by reaching $ {self.state.board[winner]:.2f}! with these  coins {self.state.coin_list[winner]}")
            
            self.quit()  
            self.destroy()  
        else:
            self.toggle_move_buttons()

    def toggle_move_buttons(self):
        if self.state.to_move == 'Player 1':
            for button in self.move_buttons:
                button.pack()
        else:
            for button in self.move_buttons:
                button.pack_forget()

    def check_next_move(self):
        if not self.game.terminal_test(self.state):
            if self.state.to_move == 'Player 2': 
                self.ai_move()
            else:
                self.toggle_move_buttons()
            self.after(5000, self.check_next_move)  # Keep checking turns

    def ai_move(self):
        try:
            if self.state.to_move == 'Player 2':
                move = alpha_beta_player(self.game, self.state)
                self.state = self.game.result(self.state, move)
                self.update_display()
        except tkinter.TclError as e:
                print(f"Error during AI move (Tkinter): {e}")

    def human_move(self, move):
        try:
            if self.state.to_move == 'Player 1':  # Human plays for Player 1
                self.state = self.game.result(self.state, move)
                self.update_display()
                
                for button in self.move_buttons:
                    if button.winfo_exists():  # Ensure button exists before hiding
                        button.pack_forget()

        except tkinter.TclError as e:
            print(f"Error: {e} - The window or widget might have been destroyed.")


if __name__ == "__main__":
    game = RaceToDollar(target=0.45)
    gui = GameGUI(game)
    gui.mainloop()
    


