import tkinter as tk
from tkinter import font
import PIL
from game import Game

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
DEFAULT_BALANCE = 50
DEFAULT_MSG = "Let's Play!"
START_BET = 5
BACKGROUND = '#00b300'

class Application:
	def __init__(self, root):
		self.root = root
		canvas = tk.Canvas(root, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
		canvas.pack()	

		frame = tk.Frame(root, bg='#00b300', bd=5)
		frame.place(relwidth=1, relheight=1)
		outcome_frame = tk.Frame(root, highlightbackground='white', highlightthickness=2, bg=BACKGROUND)
		outcome_frame.place(rely=0.3, relx=0.25, relwidth=0.75, relheight=0.4)

		outcome_label = tk.Label(outcome_frame, text=DEFAULT_MSG, font=('Courier', 18), bg=BACKGROUND)
		outcome_label.place(rely=0.5, relx=0.5, anchor='n')


		#Deal Button
		deal_button = tk.Button(outcome_frame, text='DEAL', font=('Courier', 18), bg='orange', fg='white')
		deal_button.place(rely=0.65, relx=0.5, anchor='n')

		#Player Score
		player_score_label = tk.Label(outcome_frame, text='Player score:', font=('Courier', 14), bg=BACKGROUND)
		player_score_label.place(rely=0, relx=0.15, anchor='n')


		#Dealer Score
		dealer_score_label = tk.Label(outcome_frame, text='Dealer score:', font=('Courier', 14), bg=BACKGROUND)
		dealer_score_label.place(rely=0, relx=0.75, anchor='n')

		##################
		#  Player Frame  #
		##################

		player_frame = tk.Frame(root, highlightbackground='white', highlightthickness=2, bg=BACKGROUND)
		player_frame.place(rely = 0.7, relx=0.5, relwidth=1, relheight=0.3, anchor='n')


		##################
		#  Dealer Frame  #
		##################

		dealer_frame = tk.Frame(root, highlightbackground='white', highlightthickness=2, bg=BACKGROUND)
		dealer_frame.place(rely = 0, relx=0.5, relwidth=1, relheight=0.3, anchor='n')


		#Balance
		balance_frame = tk.Frame(root, highlightbackground='white', highlightthickness=2, bg=BACKGROUND)
		balance_frame.place(relx=0, rely=0.6, relheight=0.4, relwidth=0.25)

		balance_label= tk.Label(balance_frame, text='CURRENT BALANCE', font=('Courier', 14), bg=BACKGROUND)
		balance_label.place(relx=0.5, rely=0.0, anchor='n')

		current_balance_label = tk.Label(balance_frame, bg='white', text= '$' + str(DEFAULT_BALANCE), font=('Courier', 12), highlightbackground='black', highlightthickness=5)
		current_balance_label.place(relx=0.5, rely=0.1, relheight=0.1, relwidth=0.5, anchor='n')


		#Bet Info
		bet_label = tk.Label(balance_frame, text='BET TOTAL', font=('Courier', 14), bg=BACKGROUND)
		bet_label.place(relx=0.5, rely=0.35, anchor='n')

		#Current Bet Info
		current_bet_label = tk.Label(balance_frame, bg='white', text= '$' + str(START_BET), font=('Courier New', 12), highlightbackground='black', highlightthickness=5)
		current_bet_label.place(relx=0.5, rely=0.45, relheight=0.1, relwidth=0.5, anchor='n')

		#Up-Down Buttons
		bet_up_button = tk.Button(balance_frame, bg='green', text='+$1', fg='white')
		bet_up_button.place(relx=0.5, rely=0.6, relheight=0.1, relwidth=0.5, anchor='n')

		bet_down_button = tk.Button(balance_frame, bg='red', text='-$1', fg='white')
		bet_down_button.place(relx=0.5, rely=0.72, relheight=0.1, relwidth=0.5, anchor='n')


		#Player Options
		button_frame = tk.Frame(root, highlightbackground='white', highlightthickness=2, bg=BACKGROUND)
		button_frame.place(relx=0, rely=0, relheight=0.60, relwidth=0.25)

		hit_button = tk.Button(button_frame, bg='green', text='HIT', fg='white', state='disabled')
		hit_button.place(relx=0.1, rely=0.05, relheight=0.20, relwidth=0.8)

		stand_button = tk.Button(button_frame, bg='red', text='STAND', fg='white', state='disabled')
		stand_button.place(relx= 0.1, rely=0.3, relheight=0.2, relwidth=0.8)

		double_button = tk.Button(button_frame, bg='purple', text='DOUBLE', fg='white', state='disabled')
		double_button.place(relx= 0.1, rely=0.55, relheight=0.2, relwidth=0.8)

		split_button = tk.Button(button_frame, bg='blue', text='SPLIT', fg='white', state='disabled')
		split_button.place(relx=0.1, rely=0.8, relheight=0.2, relwidth=0.8)

		self.game = Game(root = self.root,
		hit_button = hit_button, 
		stand_button = stand_button, 
		double_button = double_button,
		split_button = split_button, 
		bet_up_button = bet_up_button,
		bet_down_button = bet_down_button, 
		deal_button = deal_button, 
		current_bet_label = current_bet_label, 
		current_balance_label = current_balance_label, 
		player_score_label = player_score_label,
		dealer_score_label = dealer_score_label, 
		player_frame = player_frame,
		dealer_frame = dealer_frame, 
		outcome_label = outcome_label, 
		DEFAULT_BALANCE = DEFAULT_BALANCE)




if __name__ == "__main__":
	root = tk.Tk()
	root.title('BLACKJACK BABY!')
	root.iconbitmap('img/icon/icon.ico')

	BlackJackApp = Application(root)

	root.mainloop()