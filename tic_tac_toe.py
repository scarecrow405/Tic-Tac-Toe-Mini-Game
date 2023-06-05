from collections import deque


def check_for_win(full_board):
    check_diagonal_one = 0
    check_diagonal_reverse = 0
    row_wins = []
    col_wins = []
    col_wins_count = 0

    for r in range(ROWS):
        if full_board[r][r] == current_player_symbol:
            check_diagonal_one += 1
    if check_diagonal_one == 3:
        check_diagonal_one = True
    else:
        check_diagonal_one = False

    for r in range(ROWS):
        if full_board[r][-1 - r] == current_player_symbol:
            check_diagonal_reverse += 1
    if check_diagonal_reverse == 3:
        check_diagonal_reverse = True
    else:
        check_diagonal_reverse = False

    find_symbol_idx = []
    for r in full_board:
        if current_player_symbol not in r:
            continue
        find_symbol_idx = r.index(current_player_symbol)

        row_wins = r.count(r[find_symbol_idx]) == len(r)
        if row_wins:
            row_wins = True
            break
        else:
            row_wins = False

    for r in range(ROWS):
        for c in range(COLS):
            if full_board[c][r] == current_player_symbol:
                col_wins_count += 1
        if col_wins_count == 3:
            col_wins = True
        else:
            col_wins_count = 0

    if any([col_wins, row_wins, check_diagonal_one, check_diagonal_reverse]):
        return True
    return False


def print_board(field):
    temp_result = []
    temp_as_matrix = []

    position_symbol_x = {"X": []}
    position_symbol_o = {"O": []}

    for idx_row, cur_row in enumerate(field):
        for idx_col, col in enumerate(cur_row):
            temp_result.append(" ")

            if not col:
                continue
            else:
                if col == "X":
                    position_symbol_x[col].append([idx_row, idx_col])
                elif col == "O":
                    position_symbol_o[col].append([idx_row, idx_col])

    for i in range(0, len(temp_result), 3):
        temp_as_matrix.append([temp_result[i], temp_result[i + 1], temp_result[i + 2]])

    for symbol, value in position_symbol_x.items():
        for r, c in value:
            temp_as_matrix[r][c] = symbol
    for symbol, value in position_symbol_o.items():
        for r, c in value:
            temp_as_matrix[r][c] = symbol

    temp_string = ""
    for i, rows in enumerate(temp_as_matrix):
        temp_string += f"|  {rows[0]}  |  {rows[1]}  |  {rows[2]}  |" + "\n"
    print(temp_string)


def check_position(position):
    current_row = 0
    current_col = 0

    if position in [0, 1, 2]:
        current_row = 0
        if position == 0:
            current_col = 0
        elif position == 1:
            current_col = 1
        else:
            current_col = 2
    elif position in [3, 4, 5]:
        current_row = 1
        if position == 3:
            current_col = 0
        elif position == 4:
            current_col = 1
        else:
            current_col = 2
    elif position in [6, 7, 8]:
        current_row = 2
        if position == 6:
            current_col = 0
        elif position == 7:
            current_col = 1
        else:
            current_col = 2

    if not empty_board[current_row][current_col]:
        return [True, current_row, current_col]
    return False


player_one_name = input("Player one name: ")
player_two_name = input("Player two name: ")

players_names_and_symbols = deque([[player_one_name], [player_two_name]])
player_symbols = input(f"{players_names_and_symbols[0][0]} would you like to play with 'X' or 'O'? ").upper()

while player_symbols not in ["X", "O"]:
    print("Please chose 'X' or 'O' as your symbol!")
    player_symbols = input(f"{players_names_and_symbols[0][0]} would you like to play with 'X' or 'O'? ").upper()

if player_symbols == "X":
    players_names_and_symbols[0].append(player_symbols)
    players_names_and_symbols[1].append("O")
else:
    players_names_and_symbols[0].append("0")
    players_names_and_symbols[1].append(player_symbols)

win = False
ROWS, COLS = 3, 3

board = []

for row in range(ROWS):
    result = f"|  {str(row + 1 + row + row)}  |  {str(row + 2 + row + row)}  |  {str(row + 3 + row + row)}  |"
    board.append([result])

print("This is the numeration of the board:")
for row in board:
    print(*row)

print(f"{players_names_and_symbols[0][0]} starts first!")

empty_board = [[[], [], []],
               [[], [], []],
               [[], [], []]]

DRAW_COUNTER = 0

while not win:
    current_player_name, current_player_symbol = players_names_and_symbols[0]

    try:
        current_position = int(input(f"{current_player_name} choose a free position [1-9]: ")) - 1
        if not 0 <= current_position < 9:
            continue

        result_check_position = check_position(current_position)

        if not result_check_position:
            print("Please choose a valid position, the one you chose was not empty!")
            continue
        else:
            current_row_player, current_col_player = result_check_position[1], result_check_position[2]
            empty_board[current_row_player][current_col_player] = current_player_symbol

            print_board(empty_board)

    except ValueError:
        print("That was not a number! Please choose again.")

    DRAW_COUNTER += 1
    result = check_for_win(empty_board)

    if result:
        print(f"{current_player_name} won!!!")
        raise SystemExit

    if DRAW_COUNTER == 9:
        print("DRAW!")
        raise SystemExit

    players_names_and_symbols.rotate()

