import game
import spreadsheet
import traceback


def exec_command(cmd: str) -> None:
    args = cmd.strip().split(' ')
    match args[0]:
        case "q" | "exit":
            exit(0)
        case "r" | "run":
            run()
        case "n" | "new":
            if len(args) <= 1:
                print("Missing args")
                return
            new(*args[1:])
        case "d" | "delete":
            if len(args) <= 1:
                print("Missing args")
                return
            delete(*args[1:])
        case "sr" | "startrow":
            try:
                spreadsheet.start_row = int(args[1])
                print("Spreadsheet starting row: ", spreadsheet.start_row)
            except ValueError:
                print("Cannot parse to int: ", args[1])
        case "p" | "dump":
            dump()
        case _:
            print("Unknown cmd: ", args[0])


def new(*args) -> None:
    match args[0]:
        case "h" | "hand":

            amount = float(args[2])
            if len(args) > 3:
                game.add_hand(args[1], amount, int(args[3]))
            else:
                game.add_hand(args[1], amount)
        case "w" | "wager":
            pos = int(args[2])
            amount = float(args[3])
            if len(args) > 4:
                game.add_wager(args[1], pos, amount, args[4])
            else:
                game.add_wager(args[1], pos, amount)
        case _:
            print("Unknown new arg: ", args[0])


def delete(*args) -> None:
    match args[0]:
        case "h" | "hand":
            try:
                pos = int(args[1])
                game.remove_hand_by_position(pos)
            except ValueError:
                game.remove_hand_by_player(args[1])
        case "w" | "wager":
            pos = int(args[1])

            if len(args) == 2:
                game.remove_side_wagers(pos)
            elif args[2] == "r" or args[2] == "f":
                game.remove_side_wagers(pos, None, args[2])
            else:
                game.remove_side_wagers(pos, *args[2:])


def is_setup() -> bool:
    if not game.hands:
        print("Hands empty")
        return False

    if not spreadsheet.start_row:
        print("Spreadsheet starting row is none")
        return False

    return True


def dump() -> None:
    print(f"Hands: {game.hands}\nStarting row: {spreadsheet.start_row}\nSheet name: {spreadsheet.SHEET_NAME}")


def run() -> None:
    if not is_setup():
        print("Setup incomplete, cannot run")
        return

    game.start_round()
    scores = game.get_round_outcome()
    # record
    print(scores)

    try:
        spreadsheet.write_result(scores)
    except:
        print("Error writing to spreadsheet")

    # reset hands
    game.reset_hands()


if __name__ == '__main__':
    while True:
        try:
            exec_command(input("> "))
        except Exception as e:
            print(traceback.format_exception(e))
