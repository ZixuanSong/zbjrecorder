from enum import Enum


class Direction(Enum):
    FORWARD = 1,
    REVERSE = 2


class Wager:

    def __init__(self, amount: float, player: str, direction: Direction = Direction.FORWARD):
        self.direction = direction
        self.amount = amount
        self.player = player

    def get_winning(self, doubled: bool = False, bj: bool = False) -> float:
        amount = self.amount
        if doubled:
            amount *= 2

        if self.direction == Direction.FORWARD:
            if bj and self.amount >= 5:
                return amount / 5.0 * 6

        return amount

    def get_losses(self, doubled: bool = False, bj: bool = False) -> float:
        amount = self.amount
        if doubled:
            amount *= 2

        if self.direction == Direction.REVERSE:
            if bj and self.amount >= 5:
                return amount / 5.0 * 6

        return amount

    def __repr__(self):
        return f"Wager: [By: {self.player}, Amount: {self.amount}, Direction: {self.direction.name}]"
