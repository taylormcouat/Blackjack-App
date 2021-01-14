from deck import Hand

class Player:
	def __init__(self, balance):
		self.balance = balance
		self.hand = Hand()
		self.is_user = False

	def new_hand(self):
		'''
		Resets the players current hand.
		'''
		self.hand = Hand()

	def update_balance(self, amount):
		'''
		Updates the players balance by amount.
		:param amount: The amount balance is being updated by.
		'''
		self.balance += amount



