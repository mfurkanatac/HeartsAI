from card import Card

class Table():
    def __init__(self, players):
        self.players = players
        self.current_round = 1
        self.current_player_index = 0
        self.last_winner = None
        self.current_trick = []
        self.hearts_broken = False

    def put_card(self, card, player_name):
        # Check if it's the first card in the trick
        if not self.current_trick:
            # First card in the trick
            self.current_trick.append((card, player_name))

            # Check special rules for the first card
            if self.current_round == 1:
                # First round rules
                if card.card_type == "c" and card.number == 2:
                    # Clubs 2 must be put in the first round
                    print(f"{player_name} puts Clubs 2 on the table.")
                    self.current_suit = "c"
                    self.hearts_broken = False
                elif card.card_type == "c":
                    # Clubs 2 wasn't put, invalid move
                    print("Invalid move. In the first round, you must put Clubs 2.")
                elif card.card_type == "h" or (card.card_type == "s" and card.number == 12):
                    # Hearts and Queen of Spades cannot be played in the first round
                    print("Invalid move. In the first round, you cannot play Hearts or Queen of Spades.")
                else:
                    print(f"{player_name} puts {card.number}{card.card_type} on the table.")
                    self.current_suit = card.card_type
            else:
                # Subsequent round rules
                if card.card_type == "h" and not self.hearts_broken:
                    # Hearts cannot be led until broken
                    print("Invalid move. Hearts cannot be led until they are broken.")
                elif card.card_type == "s" and card.number == 12 and not self.hearts_broken:
                    # Queen of Spades cannot be played as the first card
                    print("Invalid move. Queen of Spades cannot be played as the first card.")
                else:
                    print(f"{player_name} puts {card.number}{card.card_type} on the table.")
                    self.current_suit = card.card_type
                    if card.card_type == "h":
                        self.hearts_broken = True
        else:
            # Not the first card in the trick
            current_player = self.players[self.current_player_index]
            if current_player.name == player_name:
                # It's the player's turn to play
                if card.card_type == self.current_suit:
                    # Follow suit rule
                    self.current_trick.append((card, player_name))
                    print(f"{player_name} puts {card.number}{card.card_type} on the table.")
                else:
                    # Violated follow suit rule
                    print("Invalid move. Must follow suit.")
            else:
                # It's not the player's turn to play
                print("Invalid move. It's not your turn to play.")

        if len(self.current_trick) == len(self.players):
            # Determine trick winner
            self.determine_trick_winner()

    def determine_trick_winner(self):
        trick_cards = self.current_trick
        lead_suit_cards = [card for card, _ in trick_cards if card.card_type == self.current_suit]

        if lead_suit_cards:
            # If there are cards in the lead suit, determine the winner based on rank
            trick_winner = max(lead_suit_cards, key=lambda x: x.number)
        else:
            # If no cards in the lead suit, determine the winner based on any suit
            trick_winner = max(trick_cards, key=lambda x: x.number)

        winner_index = [index for index, (_, name) in enumerate(trick_cards) if name == trick_winner.card_type][0]
        winner_name = trick_cards[winner_index][1]

        print(f"{winner_name} takes the trick!")
        self.current_player_index = self.players.index(self.players[winner_index])
        self.players[self.current_player_index].stack.extend([card for card, _ in trick_cards])

        # Update round status after a trick is completed
        self.update_round_status()


    def start_round(self):
        if self.current_round == 1:
            # First round starts with the player having the Club 2
            self.current_player_index = self.find_starting_player_index("c", 2)
        else:
            # Subsequent rounds start with the player who took the last set
            self.current_player_index = self.players.index(self.last_winner)

    def find_starting_player_index(self, card_type, number):
        for i, player in enumerate(self.players):
            if Card(card_type, number) in player.hand:
                return i    
    
    def update_round_status(self):
        # Update the last winner and increment the round number
        self.last_winner = self.players[self.current_player_index]
        self.current_round += 1
        self.current_trick = []
    
    def print_table(self):
        print("Current table:")
        for card, player in self.current_trick:
            print(f"{player}: {card.number}{card.card_type}", end=" ")
        print()
    
    def update_game(self):
        # if the table ends (the current game ends)
        self.current_round = 1
