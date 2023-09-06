from wager import Wager, Direction


class Hand:
    def __init__(self, wager: Wager, owner: str):
        self.doubled: bool = False
        self.busted: bool = False
        self.black_jack: bool = False
        self.split: bool = False  # Whether this hand resulted from splitting
        self.__val: int = 0
        self.__owner = owner
        self.__wager = wager
        self.__side_wagers = {}

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def value(self) -> int:
        return self.__val

    @property
    def wager(self) -> Wager:
        return self.__wager

    # 7, 8, 9 -> 17, 18, 19
    # 0, 1 -> 20, 21
    @value.setter
    def value(self, val: str) -> None:
        num = int(val)
        match num:
            case 7 | 8 | 9:
                self.__val = num + 10
            case 0 | 1:
                self.__val = num + 20
            case _:
                self.__val = 1

    def add_wager(self, new_wager: Wager) -> None:
        # combine with main wager if possible
        if new_wager.player == self.__owner and new_wager.direction == Direction.FORWARD:
            self.__wager.amount += new_wager.amount
            return

        # combine with side wager if possible
        for k in self.__side_wagers.keys():
            if k[0] == new_wager.player and k[1] == new_wager.direction:
                self.__side_wagers[k].amount += new_wager.amount
                return

        self.__side_wagers[(new_wager.player, new_wager.direction)] = new_wager

    @property
    def side_wagers(self) -> list[Wager]:
        return list(self.__side_wagers.values())

    def remove_side_wagers(self, player: str = None, direction: Direction = None) -> None:

        if player is None and direction is None:
            self.__side_wagers.clear()
            return

        if player is not None and direction is None:
            self.__side_wagers = {k: v for (k, v) in self.__side_wagers.items() if k[0] != player}
            return

        if direction is not None and player is None:
            self.__side_wagers = {k: v for (k, v) in self.__side_wagers.items() if k[1] != direction}
            return

        del self.__side_wagers[(player, direction)]

    def reset(self):
        self.doubled = False
        self.busted = False
        self.black_jack = False
        self.__val = 0

    def __repr__(self):
        return f"\nHand: [Owner: {self.owner}, {self.__wager}\nSide wagers: {self.__side_wagers.values()}]\n"
