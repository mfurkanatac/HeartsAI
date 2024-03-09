class Card:
    def __init__(self, card_type, number):
        self.number = number
        self.card_type = card_type

    def get_number(self):
        return self.number

    def get_card_type(self):
        return self.card_type

    def __str__(self):
        return f"{self._number}{self._card_type}"
    