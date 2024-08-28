import random
from player import Player
from table import Table
from card import Card

card_types = ["h", "s", "d", "c"]
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # 11 for J, 12 for Q, 13 for K, and 14 for A

class HeartsGame():
    def __init__(self, players):
        self.table = Table(players)
        self.game_round = 1

    def play_game(self):
        while not self.is_game_over():
            self.table = Table(self.table.players)
            self.reset_cards()
            self.draw_cards()     
            self.pass_cards()
            self.play_round()
    
    def draw_cards(self):
        deck = [Card(card_type, number) for card_type in card_types for number in cards]
        random.shuffle(deck)
        for i, player in enumerate(self.table.players):
            player.hand = deck[i*13:(i+1)*13]
            player.hand.sort(key=lambda x: (x.card_type, x.number))

    def play_round(self):
        self.table.start_round()
        for _ in range(len(self.table.players[0].hand)):
            self.play_card()

        # Check if a player attempts to shoot the moon
        for player in self.table.players:
            if self.is_shooting_the_moon(player):
                self.handle_shooting_the_moon(player)

        # Print round results
        self.print_round_results()

    def is_shooting_the_moon(self, player):
        # Check if the player has collected all penalty cards (hearts and Queen of Spades)
        collected_penalty_cards = [card for card in player.stack if card.card_type == "h" or (card.card_type == "s" and card.number == 12)]
        return len(collected_penalty_cards) == 14

    def handle_shooting_the_moon(self, player):
        # Give each opponent penalty points
        for opponent in self.table.players:
            if opponent != player:
                opponent.points += 26  # Each opponent receives 26 penalty points for a successful shoot the moon

    def pass_cards(self):
        # Determine the passing direction based on the current round
        pass_direction = (self.table.current_round) % 4
        pass_list = []

        for i, player in enumerate(self.table.players):
            # Determine the target player to pass cards to
            target_index = (i + pass_direction) % len(self.table.players)
            target_player = self.table.players[target_index]

            # Prompt the current player to select three cards to pass
            passed_cards = self.get_passed_cards(player)
            pass_list.append(passed_cards)
            print(f"{player.name} passes {passed_cards[0]} {passed_cards[1]} {passed_cards[2]} to {target_player.name}.")
        
        for i, player in enumerate(self.table.players):
            target_index = (i + pass_direction) % len(self.table.players)
            target_player = self.table.players[target_index]
            passed_cards = pass_list[i]
            target_player.hand.extend(passed_cards)
    
    def reset_cards(self):
        for player in self.table.players:
            player.hand = []
            player.stack = []
        

    def get_passed_cards(self, player):
        passed_cards = []

        for _ in range(3):
            while True:
                # Prompt the player to input the card they want to pass
                player.display_hand()
                card_input = input(f"Select a card to pass ({_ + 1}/3): ")

                if card_input in player.card_list():
                    # find the card object remove it from the player and add it to the passed cards
                    card_type = card_input[-1]
                    number = int(card_input[:-1])
                    for card in player.hand:
                        if card.card_type == card_type and card.number == number:
                            passed_cards.append(card)
                            player.hand.remove(card)
                    break
                else:
                    print("You don't have that card in your hand. Please select again.")
        return passed_cards

    def play_card(self):
        print(self.table.current_player_index)
        current_player = self.table.players[self.table.current_player_index]
        print(f"{current_player.name}'s turn.")
        print(f"Current table: {self.table.card1.number}{self.table.card1.card_type} {self.table.card2.number}{self.table.card2.card_type} {self.table.card3.number}{self.table.card3.card_type} {self.table.card4.number}{self.table.card4.card_type}")

        playable_cards = current_player.get_playable_cards(self.table)

        if not playable_cards:
            # No playable cards, choose any card
            played_card = random.choice(current_player.hand)
        else:
            # Choose a playable card
            played_card = random.choice(playable_cards)

        current_player.hand.remove(played_card)
        self.table.put_card(played_card, current_player.name)

    def get_playable_cards(self, table):
        if table.current_round == 1 and table.current_player_index == 0:
            # First round, first player, must play Clubs 2
            return [card for card in self.hand if card.card_type == "c" and card.number == 2]
        elif table.current_round == 1 and any(card.card_type == "c" for card in table.players[0].stack):
            # First round, someone played Clubs, play anything except Hearts or Queen of Spades
            return [card for card in self.hand if card.card_type != "h" and card.number != 12]
        elif table.current_round > 1 and table.players[0].stack:
            # Hearts are unlocked, play anything
            return self.hand
        elif table.current_round > 1 and not table.players[0].stack:
            # Hearts are not unlocked, play anything except Hearts or Queen of Spades
            return [card for card in self.hand if card.card_type != "h" and card.number != 12]
        else:
            # Default case, play anything
            return self.hand

    def is_game_over(self):
        points = [player.points for player in self.table.players]
        points.sort()
        if points[0] >= 100:
            if points[-1] != points[-2]:
                print(f"Game over! {self.table.players[0].name} won!", "With points: ", points)
                return True
            return False
        
    def print_round_results(self):
        print("Round Results:")
        for player in self.table.players:
            print(f"{player.name}: {player.points} points")
        self.game_round += 1

# Example usage:
player1 = Player("Player 1")
player2 = Player("Player 2")
player3 = Player("Player 3")
player4 = Player("Player 4")

players = [player1, player2, player3, player4]

hearts_game = HeartsGame(players)
hearts_game.play_game()
