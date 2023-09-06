import traceback

from hand import Hand
from wager import Wager, Direction
import copy

hands: list[Hand] = []


def add_hand(owner: str, amount: float, position: int = 0) -> None:
    hands.insert(position, Hand(Wager(amount, owner, Direction.FORWARD), owner))
    print(hands)


# completely delete the hand
def remove_hand_by_position(position: int) -> None:
    del hands[position]
    print(hands)


def remove_hand_by_player(player_name: str) -> None:
    global hands
    hands = [h for h in hands if h.owner != player_name]
    print(hands)


def add_wager(player_name: str, position: int, wager_amount: float, wager_direction: str = "f") -> None:
    if position < 0 or position >= len(hands):
        print("Invalid hand position: ", position)
        return

    hands[position].add_wager(
        Wager(wager_amount, player_name, Direction.FORWARD if wager_direction == "f" else Direction.REVERSE)
    )

    print(hands[position])


# simply remove additional side wagers on the hand
# optionally remove by player name and/or direction
def remove_side_wagers(position: int, player_name: str = None, direction: str = None) -> None:
    dir_enum = None
    if direction is not None:
        dir_enum = Direction.FORWARD if direction == "f" else Direction.REVERSE

    hands[position].remove_side_wagers(player_name, dir_enum)
    print(hands[position])


def start_round() -> None:
    idx = 0
    while idx < len(hands):
        hand = hands[idx]
        outcome = input(f"[{idx}] {hand.owner}: ").strip()
        if outcome == "s":
            # hand is split
            new_hand = copy.deepcopy(hand)
            new_hand.split = True
            hands.insert(idx + 1, new_hand)
            continue

        try:
            apply_hand_outcome(outcome, hand)
        except Exception as e:
            print(traceback.format_exception(e))
            continue

        idx += 1


def get_round_outcome() -> dict[str, int]:
    dealer_hand = Hand(Wager(0, "ZS"), "ZS")
    while True:
        try:
            apply_hand_outcome(input("ZSON: ").strip(), dealer_hand)
            break
        except Exception as e:
            print(traceback.format_exception(e))
            continue

    scores = {}
    dealer_score = get_effective_score(dealer_hand, True)
    for hand in hands:

        player_score = get_effective_score(hand)

        if player_score > dealer_score:
            # player wins

            # owning wager
            scores[hand.owner] = scores.get(hand.owner, 0) + hand.wager.get_winning(hand.doubled, hand.black_jack)

            # side wagers
            for wager in hand.side_wagers:
                curr_score = scores.get(wager.player, 0)
                if wager.direction == Direction.FORWARD:
                    scores[wager.player] = curr_score + wager.get_winning(hand.doubled, hand.black_jack)
                else:
                    scores[wager.player] = curr_score - wager.get_losses(hand.doubled, hand.black_jack)

        elif player_score < dealer_score:
            # dealer wins

            # owning wager
            scores[hand.owner] = scores.get(hand.owner, 0) - hand.wager.get_losses(hand.doubled)

            # side wagers
            for wager in hand.side_wagers:
                curr_score = scores.get(wager.player, 0)
                if wager.direction == Direction.FORWARD:
                    scores[wager.player] = curr_score - wager.get_losses(hand.doubled)
                else:
                    if dealer_hand.busted:
                        scores[wager.player] = curr_score - wager.get_losses(hand.doubled)
                    else:
                        scores[wager.player] = curr_score + wager.get_winning(hand.doubled)

    return scores


def get_effective_score(hand: Hand, dealer: bool = False) -> int:
    effective_score = hand.value
    if hand.busted:
        if dealer:
            effective_score = 0
        else:
            effective_score = -1
    elif hand.black_jack:
        effective_score = 22

    return effective_score


def apply_hand_outcome(outcome: str, hand: Hand) -> None:
    match outcome[0]:
        case 'b':
            hand.busted = True
            return
        case 'j':
            hand.black_jack = True
            return
        case 'd':
            hand.doubled = True
            hand.value = outcome[1]
        case _:
            hand.value = outcome[0]


def reset_hands() -> None:
    global hands
    hands = [h for h in hands if not h.split]
    for hand in hands:
        hand.reset()
