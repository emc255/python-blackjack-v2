import os

from commons import Rank, Suit


class Card:

    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        self.width = 80
        self.height = 100
        root_dir = os.path.dirname(os.path.abspath(__file__))

        if any(rank == r for r in [Rank.ACE, Rank.JACK, Rank.QUEEN, Rank.KING]):
            self.front_image_path = os.path.join(root_dir, 'resource', 'images', "cards",
                                                 f"{rank.name.lower()}_of_{suit.name.lower()}.png")

            # self.image_path = f"resource/images/cards/{rank.name.lower()}_of_{suit.name.lower()}.png"
        else:
            # getting the full absolute path
            self.front_image_path = os.path.join(root_dir, 'resource', 'images', "cards",
                                                 f"{rank.value}_of_{suit.name.lower()}.png")
            # relative path is not working
            # self.image_path = f"resource/images/cards/{rank.value}_of_{suit.name.lower()}.png"

        self.back_image_path = os.path.join(root_dir, 'resource', 'images', "cards", "back.png")

    def __str__(self):
        return f"{self.rank.name} of {self.suit.name}"
