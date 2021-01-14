import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font, PhotoImage
from player import Player
from deck import Deck, Hand
from tkinter import messagebox


MAX_SCORE = 21
HIT_SCORE = 16
SOFT_SCORE = 17
START_BET = 5
WIN_PAY_RATE = 2
BJ_PAY_RATE = 2.5
DOUBLE_RATE = 4
PLAYER_WIN_MSG = "Player wins!"
BUST_MSG = "Bust... you lose!"
BJ_MSG = "BLACKJACK! Player wins!"
DEALER_WINS_MSG = "Dealer wins!"
PUSH_MSG = "Push!"
GAME_MSG = "Game in progress..."
CARD_HEIGHT = 150  
CARD_WIDTH = 98

class Game:
	def __init__(self, root, hit_button, 
		stand_button, double_button,
		split_button, bet_up_button,
		bet_down_button, deal_button, current_bet_label,
		current_balance_label, player_score_label,
		dealer_score_label, player_frame,
		dealer_frame, outcome_label, 
		DEFAULT_BALANCE):

		self.root = root
		self.hit_button = hit_button 						#Player option to hit
		self.stand_button = stand_button 					#Player option to stand
		self.double_button = double_button					#Player option to double down
		self.split_button = split_button 					#Player option to split (if valid)
		self.bet_up_button = bet_up_button 					#Player option to increase bet by $1
		self.bet_down_button = bet_down_button 				#Player option to decrease bet by $1
		self.deal_button = deal_button 						#Player option to deal (start new game)
		self.current_bet_label = current_bet_label 			#Label that displays current bet
		self.current_balance_label = current_balance_label	#Label that displays current balance
		self.player_score_label = player_score_label		#Label that displays players current score
		self.dealer_score_label = dealer_score_label		#Label that displays dealers current score
		self.player_frame = player_frame					#Frame that shows the player's current cards
		self.dealer_frame = dealer_frame					#Frame that shows the dealer's current cards
		self.outcome_label = outcome_label					#Frame that displays the outcome of the game
		self.dealer = Player(0)								#The dealer being played against (doesn't require balance)
		self.user = Player(DEFAULT_BALANCE)					#The instance for the user
		self.deck = None

		self.deal_button.configure(command = lambda: self.start_round())
		self.bet_up_button.configure(command = lambda: self.adjust_bet(1))
		self.bet_down_button.configure(command = lambda: self.adjust_bet(-1))
		self.hit_button.configure(command = lambda: self.hit())
		self.stand_button.configure(command = lambda: self.dealer_next_move())
		self.double_button.configure(command = lambda: self.double_down())
		self.current_bet = START_BET



	def check_bet_insufficent(self):
		'''
		Checks if the current submitted bet is above the users current balance and
		flashes a warning message warning it is invalid.
		:return: True if bet is above users current balance, False if bet is below
		users current balance.
		'''

		if (self.current_bet > self.user.balance):
			messagebox.showwarning("Insufficent Funds", "You don't have enough money to place that bet. Try again with a smaller amount!")
			return True
		else:
			return False

	def check_bet_zero(self, adjustment):
		'''
		Checks if the current submitted bet is below zero and flashes warning message.
		:return: True if bet is below 0, False if bet is above 0
		'''

		if (self.current_bet + adjustment < 0):
			messagebox.showwarning("Negative Bet", "You can't bet below $0.")
			return True
		else:
			return False

	def add_card_frame(self, card, player):
		'''
		Adds cards to the players frame to be displayed on the application.
		:param card: The card being added to the current frame.
		:param player: The player whose frame is being modified.
		'''

		if player == self.user:
			frame = self.player_frame
		else:
			frame = self.dealer_frame

		img = Image.open(card.img)
		img = img.resize((CARD_WIDTH, CARD_HEIGHT), Image.ANTIALIAS)
		card_img = ImageTk.PhotoImage(img)
		card_label = tk.Label(frame, image = card_img, bg='#00b300')
		card_label.pack(side='right')
		card_label.image = card_img

	@staticmethod
	def clear_frame(frame):
		'''
		Deletes all children in the parent frame.
		:param frame: The frame being modified.
		'''

		for child in frame.winfo_children():
			child.destroy()


	def adjust_bet(self, amount):
		'''
		Adjusts self.current_bet by the passed in amount and displays new bet.
		:param amount: The amount to adjust the bet by.
		'''

		if not self.check_bet_zero(amount):
			self.current_bet += amount
			self.current_bet_label.configure(text="${}".format(self.current_bet))

	def adjust_balance(self, amount):
		'''
		Adjusts users balance by the passed in amount and displays new balance.
		:param amount: The amount to adjust the bet by.
		'''

		self.user.update_balance(amount)
		self.current_balance_label.configure(text="${}".format(self.user.balance))


	def check_zero(self):
		'''
		Checks if the user balance is 0 or lower. Displays a message if true.
		'''

		if (user.balance <= 0):
			self.player_lost = True
			messagebox.showwarning("No Money", "You lost all your money... New game will restart with initial balance")


	def update_score_label(self):
		'''
		Updates the score label for both the Dealer and the Player.
		'''

		self.dealer_score_label.configure(text= "Dealer Score: {}".format(self.dealer.hand.score))
		self.player_score_label.configure(text= "Player Score: {}".format(self.user.hand.score))


	def start_round(self):
		'''
		The function that initiates a start of round. Will clear both the
		player and dealer frames, reset the dealer and player hands, 
		change the outcome label, give a new deck, enable/disable buttons
		and deal the initial cards.
		'''

		if not self.check_bet_insufficent():
			self.clear_frame(self.dealer_frame)
			self.clear_frame(self.player_frame)
			self.dealer.new_hand()
			self.user.new_hand()
			self.adjust_outcome_label(msg=GAME_MSG)	
			self.deck = Deck()
			self.deck.shuffle_deck()
			buttons_disable = [self.bet_up_button, self.bet_down_button, self.deal_button]
			buttons_enable = [self.hit_button, self.stand_button]
			self.config_buttons(state='disabled', buttons= buttons_disable)
			self.config_buttons(state='normal', buttons= buttons_enable)

			self.adjust_balance(-self.current_bet)

			self.initial_deal()

	
	@staticmethod
	def config_buttons(state, buttons):
		'''
		Configures the state for multiple buttons.
		:param state: The new state for the buttons.
		:param buttons: A list of buttons to be configured.
		'''

		for button in buttons:
			button.configure(state=state)


	def initial_deal(self):
		'''
		The initial deal to the user and the dealer. Enables the double button 
		so users can double down and checks for Blackjacks.
		'''

		self.hit()
		self.hit()
		self.config_buttons(state='normal', buttons=[self.double_button])
		if (self.user.hand.is_bj):
			self.end_game(winner="PLAYER")
		else:
			self.hit_dealer()

	def hit(self):
		'''
		The function for adding a new card to for the user. It disables double button
		if it is enabled, adds a new card from self.deck to the user's hand, checks for
		busts, and if the score is 21 will start the dealers turn.
		'''

		if (self.double_button['state'] == 'normal'):
			self.config_buttons(state='disabled', buttons=[self.double_button])
		card = self.deck.deal_card()
		self.user.hand.add_card(card)
		self.add_card_frame(card, self.user)
		if (self.user.hand.is_busted):
			self.end_game(winner="DEALER")
		self.update_score_label()
		if (self.user.hand.score == MAX_SCORE):
			self.dealer_next_move()

	def hit_dealer(self):
		'''
		Simulates the dealer getting a new card from the deck and updates the dealers
		score frame.
		'''

		card = self.deck.deal_card()
		self.dealer.hand.add_card(card)
		self.add_card_frame(card=card, player=self.dealer)
		self.update_score_label()


	def check_winner(self):
		'''
		Determines the winner based on final scores only (not including busts).
		'''

		if self.user.hand.score > self.dealer.hand.score:
			return "PLAYER"
		elif self.user.hand.score == self.dealer.hand.score:
			return "PUSH"
		else:
			return "DEALER"

	def dealer_next_move(self):
		'''
		Function that simulates the next moves for the dealer. It first disables buttons for betting, then continously draws
		cards until it is either at a hard 17 or a soft 18. After it checks who won and ends the game.
		'''

		buttons_disable = [self.double_button, self.hit_button, self.stand_button, self.split_button]
		self.config_buttons(buttons = buttons_disable, state = 'disabled')
		dealers_turn = True
		while dealers_turn:
			if (self.dealer.hand.score == SOFT_SCORE and self.dealer.hand.num_aces > 0) or (self.dealer.hand.score < SOFT_SCORE):
				self.hit_dealer()
			else:
				dealers_turn = False

		if (self.dealer.hand.is_busted):
			self.end_game("PLAYER")
		else:
			self.end_game(self.check_winner())



	def end_game(self, winner):
		'''
		Function that deals with ending the game. It enables/disables buttons for the next game, configures
		the message for winning/losing/pushing and pays out the player.
		'''

		buttons_enable = [self.deal_button, self.bet_down_button, self.bet_up_button]
		self.config_buttons(state='normal', buttons= buttons_enable)

		buttons_disable = [self.hit_button, self.stand_button, self.double_button, self.split_button]
		self.config_buttons(state='disabled', buttons=buttons_disable)

		if (winner == "PLAYER"):
			if (self.user.hand.is_bj):
				pay_rate = BJ_PAY_RATE
				msg = BJ_MSG
			else:
				pay_rate = WIN_PAY_RATE
				msg = PLAYER_WIN_MSG
		elif (winner == "PUSH"):
			pay_rate = 1
			msg = PUSH_MSG
		else:
			pay_rate = 0
			if (self.user.hand.is_busted):
				msg = BUST_MSG
			else:
				msg = DEALER_WINS_MSG

		self.adjust_balance(self.current_bet*pay_rate)
		self.adjust_outcome_label(msg=msg)

	def double_down(self):
		'''
		Activated when the player doubles down, it doubles the current bet and draws one card for the player.
		It then allows the dealer to finish their moves.
		'''

		self.adjust_bet(amount=self.current_bet)
		self.adjust_balance(amount=-self.current_bet)
		self.hit()
		if (self.user.hand.score < MAX_SCORE):
			self.dealer_next_move()

	def adjust_outcome_label(self, msg):
		'''
		Adjusts the outcome message being displayed based on msg.
		:param msg: The new message to be displayed.
		'''

		self.outcome_label.configure(text=msg)



		










