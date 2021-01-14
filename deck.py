import random

ACE = 1
JACK = 11
QUEEN = 12
KING = 13
FACE_CARD = 10
ACE_SCORE = 11
MAX_SCORE = 21
CARD_IMG_PATH = 'img/cards/'
EXT = '.png'


class Card:
	def __init__(self, suit, val, score):
		self.suit = suit
		self.val = val
		self.img = CARD_IMG_PATH + val + suit[0] + EXT
		self.score = score



class Deck:
	def __init__(self):
		self.cards= []
		self.build()

	def build(self):
		'''
		Builds the deck of card, picking 13 cards of each suit.
		'''
		for suit in ["Spades", "Clubs", "Diamonds", "Hearts"]:
			for num in range(1,14):
				if (num == ACE):
					val = "A"
					score = ACE_SCORE
				elif (num == JACK):
					val = "J"
					score = FACE_CARD
				elif (num == QUEEN):
					val = "Q"
					score = FACE_CARD
				elif (num == KING):
					val = "K"
					score = FACE_CARD
				else:
					val = str(num)
					score = num

				self.cards.append(Card(suit, val, score))

	def shuffle_deck(self):
		'''
		Shuffles the deck into random order.
		'''
		random.shuffle(self.cards)

	def deal_card(self):
		'''
		Removes a card from the deck.
		:return: The card removed from the deck.
		'''
		return self.cards.pop(0)

class Hand:
	def __init__(self):
		self.cards = []
		self.score = 0
		self.num_aces = 0
		self.is_busted = False
		self.is_bj = False


	def update(self, score):
		'''
		Updates the score of the hand based on incoming parameter. If there are aces and the hand is busted,
		it will lower score so hand is not busted. Also checks for blackjacks.
		:param score: The score being added to the hand.
		'''
		self.score += score

		if (self.score > MAX_SCORE and self.num_aces > 0):
			while (self.num_aces > 0 and self.score > MAX_SCORE):
				self.num_aces -= 1
				self.score -= 10

		if (self.score > MAX_SCORE):
			self.is_busted = True

		if (self.score == MAX_SCORE and len(self.cards) == 2):
			self.is_bj = True	


	def add_card(self, card):
		'''
		Adds a card to the hand.
		:param card: The card being added to hand.
		'''
		self.cards.append(card)
		if card.val == "A":
			self.num_aces += 1

		self.update(card.score)

