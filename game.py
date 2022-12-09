import random
import time

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show_card(self):
        print(f"{self.value} of {self.suit}")

class Deck(Card):
    def __init__(self):
        self.deck = []
        self.build_deck()
        self.shuffle_deck()

    def build_deck(self):
        index = {1: "Ace", 8: "Jack", 9: "Queen", 10: "King"}
        for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            for i in range(1, 11):
                value = index.get(i, str(i))
                self.deck.append(Card(suit, value))

    def show_deck(self):
        for card in self.deck:
            card.show_card()
                
    def shuffle_deck(self):
        for i in range(len(self.deck) - 1, 0, -1):
            r = random.randint(0, i)
            self.deck[i], self.deck[r] = self.deck[r], self.deck[i]
            
    def draw_card(self):
        return self.deck.pop()

class Player():
    def __init__(self, name, team):
        self.name = name
        self.hand = []
        self.points = 0
        self.team = team

    def draw(self, deck):
        self.hand.append(deck.draw_card())
        return self.hand
    
    def show_hand(self):
        for card in self.hand:
            card.show_card()
    
    def discard(self, suit, value):
        for card in self.hand:
            if card.suit.lower() == suit and card.value.lower() == value:
                self.hand.remove(card)
                return self.hand
        return None
        
class Team():
    def __init__(self, teammate1, teammate2):
        self.t1 = teammate1
        self.t2 = teammate2
        self.team_points = 0

    def update_points(self):
        self.team_points = self.t1.points + self.t2.points

POINTS = {
    "ace": 11, 
    "7": 10, 
    "king": 4, 
    "jack": 3, 
    "queen": 2,
    }

NO_POINTS = {
    "6": 1.9,
    "5": 1.8,
    "4": 1.7,
    "3": 1.6,
    "2": 1.5,
}

# Goes around clockwise
def next_turn(turn):
    if turn == 4:
        return 1
    return turn + 1

    
def game():
    # Add 4 Players to the game, 2 per team
    p1 = Player(input("Player 1's Name: "), 1)
    p2 = Player(input("Player 2's Name: "), 2)
    p3 = Player(input("Player 3's Name: "), 1)
    p4 = Player(input("Player 4's Name: "), 2)

    players = {
        1: p1,
        2: p2, 
        3: p3, 
        4: p4
        }

    team1 = Team(p1, p3)
    team2 = Team(p2, p4)

    # Set dealer as p1, then it rotates p2 -> p3 -> p4 -> p1
    dealer = 1
    
    # Keep playing rounds until a team has earned 4 game points
    extra_point = False
    while max(team1.team_points, team2.team_points) < 4:
        # Update Points
        round_winner, game_pts = game_round(dealer, players)
        round_winner.points += game_pts
        if extra_point == True:
            round_winner.points += 1
            extra_point = False
        team1.update_points()
        team2.update_points()

        # Add a point for next game if 0 pts scored this round (meaining it was 60-60)
        if game_pts == 0:
            extra_point = True

        # Update dealer
        dealer = next_turn(dealer)
        print(f"\nGame points:\nTeam 1: {team1.team_points} | Team 2: {team2.team_points}")
    # Declare Winners
    if team1.team_points >= 4:
        print(f"{team1.t1.name} and {team1.t2.name} of team 1 won!")
    else:
        print(f"{team2.t1.name} and {team2.t2.name} of team 2 won!")

def game_round(dealer, players):    
    # Create a shuffled deck
    deck = Deck()
    print("Shuffling...")
    time.sleep(2)
    
    # Starting with the right of dealer, deal 10 cards
    turn = next_turn(dealer)
    for i in range(4):      # for each player
        currPlayer = players[turn]
        for _ in range(10):
            currPlayer.draw(deck)
        turn = next_turn(turn)
    # Trump Suit is the last card dealt (to dealer)
    trump_suit = currPlayer.hand[-1].suit.lower()
    print(f"Trump suit is {trump_suit.capitalize()}")
    # {team: round_points}
    team_scores = {1: 0, 2: 0}
    
    # Trick is played 10 times
    team1_wins = 0
    for i in range(10):
        trick_suit = None
        trick_total_pts = 0
        trick_highest_pt = 0
        trick_highest_pt_calculated = 0

        # Let each person make a move - starting with right of dealer
        time.sleep(1)
        currPlayer = players[turn]
        print(f"\n*{currPlayer.name} chooses the trick suit*")
        for _ in range(4):
            currPlayer = players[turn]
            suit, value = move(currPlayer, trick_suit, trump_suit)
            if value in POINTS:
                temp_calculated_pts = POINTS[value]
            else:
                temp_calculated_pts = NO_POINTS[value]

            # Set the trick_suit to first player's card
            if trick_suit is None:
                trick_suit = suit

            
            if suit == trump_suit:
                temp_calculated_pts += 24 
            elif suit == trick_suit:
                temp_calculated_pts += 12

            # If card that was just played is highest scorer, update variables
            if temp_calculated_pts > trick_highest_pt_calculated:
                trick_highest_pt = POINTS.get(value, 0)
                trick_highest_pt_calculated = temp_calculated_pts
                trick_winner = currPlayer
                trick_winning_card = (suit, value)
            trick_total_pts += POINTS.get(value, 0)

            print("------------------------------------")
            # Move to person on right
            turn = next_turn(turn)
        turn = next_turn(turn)
    

        # Add points won in trick (total of 4 cards) to the winner team's score
        team_scores[trick_winner.team] += trick_total_pts
        print(f"{trick_winner.name} won the trick with {trick_winning_card[1]} of {trick_winning_card[0]} gaining {trick_total_pts} points.")
        print(f"Team 1 pts: {team_scores[1]} | Team 2 pts: {team_scores[2]}")

    # Get winner of trick (round_winner = 1/2/3/4)
        round_winner = max(team_scores, key=team_scores.get)
        round_pts = team_scores[round_winner]
        if round_winner == 1:
            team1_wins += 1
    
    # If team1 wins 0, team2 won all tricks | If team1 wins 10, then won all tricks
    if team1_wins == 0 or team1_wins == 10:
        game_pts = 4
    elif round_pts > 60:
        game_pts = 1
    elif round_pts >= 91:
        game_pts = 2
    else:
        game_pts = 0

    print(f"{players[round_winner].name} won the round with {round_pts} points")
    return (players[round_winner], game_pts)

# The current turn's player decides on what card to play
def move(player, trick_suit, trump_suit):
    print(f"\n---{player.name}'s turn---")
    # Print cards avaliable to play except first player
    matches = 0
    print("Your hand is:")
    for card in player.hand:
        if card.suit.lower() == trump_suit and card.suit.lower() == trick_suit:
            print(f"{card.value} of {card.suit} - TRUMP + TRICK MATCH")
            matches += 1
        elif card.suit.lower() == trump_suit:
            print(f"{card.value} of {card.suit} - TRUMP MATCH")
        elif card.suit.lower() == trick_suit:
            print(f"{card.value} of {card.suit} - TRICK MATCH")
            matches += 1
        else:
            card.show_card()
    print("")

    # Ask for a card to discard
    card = input("Choose a card to play: ")
    temp = card.split(" ")
    try:
        suit, value = temp[2].lower(), temp[0].lower()
        valid = True
    except IndexError:
        valid = False
        suit = None
        value = None

    # Keep asking if:
    # 1. There is a match, and suit of chosen card doesn't match trick suit
    # 2. Card is not in player's hand
    while (suit != trick_suit and matches > 0) or player.discard(suit, value) is None or valid == False:
        print("<<Invalid Card!>>")
        card = input("Choose a valid card to play: ")
        temp = card.split(" ")
        try:
            suit, value = temp[2].lower(), temp[0].lower()
            valid = True
        except IndexError:
            valid = False

    # First persons card becomes the currend suit - wont run for other 3 players' turn
    if not trick_suit:
        trick_suit = suit
    return (suit, value)

game()
