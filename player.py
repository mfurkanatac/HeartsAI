class Player():
    def __init__(self, name, hand=None, stack=None, points=0):
        if hand is None:
            hand = []
        if stack is None:
            stack = []
        self.name = name
        self.hand = hand
        self.stack = stack
        self.points = points

    def display_hand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            print(f"{card.number}{card.card_type}", end=" ")  # Print each card in the hand
        print()  # Print a newline for readability
        self.card_list()
    
    def card_list(self):
        return [f"{card.get_number()}{card.get_card_type()}" for card in self.hand]
    
    def remove_card(self, card):
        card_type = card[-1]
        number = int(card[:-1])
        print(f"Removing {card_type} {number}")
        for c in self.hand:
            if c.get_card_type() == card_type and c.get_number() == number:
                self.hand.remove(c)
                return
        print(f"Error: {self.name}'s hand does not contain the card {card}")
