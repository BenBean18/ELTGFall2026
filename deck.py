#!/usr/bin/env python3
from numpy.random import Generator, PCG64
from collections import defaultdict
import json, copy

CARDS = ["Del Rey", "Palms", "Downtown", "Pico-Robertson", "Expo Park", "Fairfax"]

class Deck:
    seed = 0x454c5447 # "ELTG" in ASCII

    rg = Generator(PCG64(seed))
    total_drawn = 0
    drawn = defaultdict(list)

    cards = []

    def set_state_json(self, state):
        state_dict = json.loads(state)
        self.SEED = state_dict["seed"]
        self.drawn = defaultdict(list, state_dict["drawn"])
        self.total_drawn = state_dict["total_drawn"]

        self.reset(draw=True)

    def reset(self, draw=True):
        self.rg = Generator(PCG64(self.seed))
        self.cards = copy.deepcopy(CARDS)
        self.rg.shuffle(self.cards)

        if draw:
            for _ in range(self.total_drawn):
                self.cards.pop(0)

    def draw(self, team):
        card = self.cards.pop(0)
        self.drawn[team].append(self.total_drawn)
        self.total_drawn += 1
        return card

    def get_state_json(self):
        return json.dumps({"seed": self.seed, "total_drawn": self.total_drawn, "drawn": self.drawn})

    def hand(self, team):
        self.reset(draw=False)
        hand = [self.cards[i] for i in self.drawn[team]]
        self.reset(draw=True)
        return hand

# if __name__ == '__main__':
#     team_cards = []

#     reset(draw=True)
#     # set_state_json(r'{"seed": 1162630215, "total_drawn": 3, "drawn": {"Team1": [0, 2], "Team2": [1]}}')

#     for i in range(3):
#         team = TEAMS[i % 2]
#         print(team, draw(TEAMS[i % 2]))
#         set_state_json(get_state_json())

#     print(hand(TEAMS[0]))
#     print(hand(TEAMS[1]))
#     print(get_state_json())