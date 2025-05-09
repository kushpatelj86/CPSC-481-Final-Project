Race to Dollar Game
This project implements a two-player game called "Race to Dollar" using both a terminal interface and a GUI built with Tkinter. One player is a human and the other is an AI using the Alpha-Beta Pruning algorithm. 
The goal is to be the first to collect coins that add up to exactly $1.00.


Features
Turn-based coin collection game.

AI opponent using Alpha-Beta pruning.

Graphical user interface using Tkinter.

Supports Penny ($0.01), Nickel ($0.05), Dime ($0.10), and Quarter ($0.25).

Displays running totals and selected coins.

Game Rules
Players take turns selecting a coin.

Valid coins are ones that do not push the player's total above $1.00.

First player to reach exactly $1.00 or any target amount wins.

If no valid moves are left, the game ends.

AI Algorithm

The AI is the alpha beta pruning algorithm that you provided in class but I made a slight modification and adjustment to it by adding a depth tracker, 
and if it reaches a depth of 10 then the algorithm stops searching because without the depth tracker if there is move that is equally good or if they aren't 
sure what move to make it would keep searching and the depth tracker stops the ai for infinently searching and choose the best decision based on the highest value

Game Class
The game class is the game class that you provided for Programming Project 2 

How to Run

thedollargame.py
To run the game you must run "python3 thedollargame.py", when you run that command it takes you to a GUI window which was written in TKinter
Make sure Python 3 is installed.

Ensure the following libraries are available: tkinter, numpy.

Run the script:
python3 thedollargame.py


Terminal Play (Alternative)
game = RaceToDollar()
game.play_game(query_player1, alpha_beta_player)






Sources
https://github.com/aimacode/aima-python
https://www.geeksforgeeks.org/python-tkinter-tutorial/?ref=outindfooter
