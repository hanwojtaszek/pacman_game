import random
import math
import copy


def read_board(text_file):
    """
            Read game board from text file and remove special characters to display it later.

            Parameters: text_file (str) : Text file with game board in a format name.txt
            Returns: board (list) : Game board
    """
    with open(text_file, "r") as pacman_board:
        board_file = pacman_board.readlines()
    board = []
    for row in board_file:
        row = row.replace("\n", "")
        board.append(list(row))
    return board


def display_board(board):
    """
            Display game board

            Parameters: board (list) : Game board
            Returns: N/A
    """
    for row in enumerate(board):
        for col in enumerate(board):
            board[row[0]][col[0]] = str(board[row[0]][col[0]])
    for row in enumerate(board):
        print("".join(board[row[0]]))


def update_board_pacman(board, last_pacman_position, new_pacman_position):
    """
            Update Pacman position on board after its move.

            Parameters: board (list) : Game board
                        last_pacman_position (list) : Previous position of Pacman on the board
                        new_pacman_position (list) : Current position of Pacman after its move
            Returns: board (list) : Game board after Pacman's move
    """
    board[last_pacman_position[0]][last_pacman_position[1]] = " "
    board[new_pacman_position[0]][new_pacman_position[1]] = "G"
    return board


def get_next_place_in_board(board, log_board, new_ghosts_positions, last_ghosts_positions):
    """
            Return characters on positions to which ghosts are moving. Needed for game board update.

            Parameters: board (list) : Game board
                        log_board (list) : List of booleans marking if Pacman has visited chosen place in a game board
                        new_ghosts_positions (list) : New positions of Ghosts after their moves
                        last_ghosts_positions (list) : Last positions of Ghosts
            Returns: next_places (list) : List characters on positions to which ghosts are moving.
    """
    next_places = []
    for i in range(0, len(new_ghosts_positions)):
        if board[new_ghosts_positions[i][0]][new_ghosts_positions[i][1]] == "G":
            next_places.append(" ")
        elif board[new_ghosts_positions[i][0]][new_ghosts_positions[i][1]] == "X":
            if log_board[last_ghosts_positions[i][0]][last_ghosts_positions[i][1]]:
                next_places.append(" ")
            else:
                next_places.append(".")
        else:
            next_places.append(board[new_ghosts_positions[i][0]][new_ghosts_positions[i][1]])
    return next_places


def update_board_characters(board, last_ghosts_positions, next_places):
    """
            Update previous ghosts' positions after their move.

            Parameters: board (list) : Game board
                        last_ghosts_positions (list) : Last positions of Ghosts
                        next_places (list) : List characters on positions to which ghosts are moving.
            Returns: board (list) : Game board after update
    """
    board[last_ghosts_positions[0][0]][last_ghosts_positions[0][1]] = next_places[0]
    board[last_ghosts_positions[1][0]][last_ghosts_positions[1][1]] = next_places[1]
    board[last_ghosts_positions[2][0]][last_ghosts_positions[2][1]] = next_places[2]
    return board


def update_board_ghosts(board, new_ghosts_positions):
    """
            Update game board after Ghosts' moves.

            Parameters: board (list) : Game board
                        new_ghosts_positions (list) : New positions of Ghosts on the board
            Returns: board (list) : Game board after update
    """
    for ghost_position in new_ghosts_positions:
        board[ghost_position[0]][ghost_position[1]] = "X"
    return board


def count_dots(board):
    """
            Count dots on the board.

            Parameters: board (list) : Game board
            Returns: dots_count (int) : Number of dots on the board.
    """
    dots_count = 0
    for row in board:
        dots_count += row.count(".")
    print(f"Dots left to catch: {dots_count}\n")
    return dots_count


def recount_dots(board, pacman_position, dots_counter):
    """
            Recount dots on the board after Pacman's move. Needed to claim victory - if the counter is = 0, Pacman wins.

            Parameters: board (list) : Game board
                        pacman_position (list) : Pacman position on board after its move
                        dots_counter (int) : Counter of dots on the board
            Returns: dots_counter (int) : Counter of dots on the board
    """
    if board[pacman_position[0]][pacman_position[1]] == ".":
        dots_counter -= 1
    print(f"Dots left to catch: {dots_counter}\n")
    return dots_counter


def check_victory(dots_counter):
    """
            Check if Pacman won the game and ate all dots.

            Parameters: dots_counter (int) : Counter of dots on the board
            Returns: victory (bool) : Boolean value defining if winning conditions are met.
    """
    if dots_counter == 0:
        print("\n\n\n----- Pacman wins! -----\n\n\n")
        victory = True
    else:
        victory = False
    return victory


def check_defeat(pacman_position, ghosts_positions):
    """
            Check if Pacman lost the game and was caught by one of the Ghosts.

            Parameters: pacman_position (list) : Current Pacman's position
                        ghosts_positions (list) : Current Ghosts' positions
            Returns: defeat (bool) : Boolean value defining if loosing conditions are met.
    """
    if pacman_position in ghosts_positions:
        print("\n\n\n----- Ghosts win! -----\n\n\n")
        defeat = True
    else:
        defeat = False
    return defeat


def get_position(hero, board):
    """
            Read position of Pacman (G) or Ghosts (X) on the board.

            Parameters: hero (str) : Name of the hero - Pacman or Ghost
                        board (list) : Game board
            Returns: [row_number, row.index("G")]/ ghosts_positions (list) : Hero's position on the board
    """
    row_number = 0
    if hero == "pacman":
        for row in board:
            if "G" in row:
                return [row_number, row.index("G")]
            row_number += 1
    if hero == "ghost":
        ghosts_positions = []
        for row in board:
            counter = row.count("X")
            start = 0
            while counter >= 1:
                ghosts_positions.append([row_number, row.index("X", start)])
                start = row.index("X") + 1
                counter -= 1
            row_number += 1
        return ghosts_positions


def log_pacman_moves(log_board, pacman_position):
    """
            Log places visited by Pacman on a game board.

            Parameters: log_board (list) : Board to log Pacman's positions
                        pacman_position (list) : Current Pacman's position
            Returns: log_board (list) : Board with logged Pacman's positions
    """
    log_board[pacman_position[0]][pacman_position[1]] = True
    return log_board


def check_if_wall(board, position, vertical=0, horizontal=0):
    """
            Verify if the next position of Pacman or Ghosts is the wall (#).

            Parameters: board (list) : Game board
                        position (list) : Current position of a hero that we want to check walls for.
                        vertical/ horizontal (int) : Modifiers needed to check neighbouring fields on the board.
            Returns: True/ False (bool) : Boolean value defining if next position is the wall.
    """
    if board[position[0] + horizontal][position[1] + vertical] == "#":
        return True
    return False


def move_pacman(board, pacman_position):
    """
            Allow user to move Pacman by pressing keyboard keys.

            Parameters: board (list) : Game board
                        pacman_position (list) : Current Pacman's position on the board.
            Returns: new_pacman_position (list) : Next Pacman's position on the board.
    """
    move_options = ["w", "s", "a", "d"]
    move = input("Go! ")
    new_pacman_position = [0, 0]
    while move not in move_options:
        print("Wrong move!")
        move = input("Go! ")
    if move == "w":
        if not check_if_wall(board, pacman_position, horizontal=-1):
            new_pacman_position = go_up(pacman_position, new_pacman_position)
        else:
            new_pacman_position = pacman_position
    elif move == "s":
        if not check_if_wall(board, pacman_position, horizontal=1):
            new_pacman_position = go_down(pacman_position, new_pacman_position)
        else:
            new_pacman_position = pacman_position
    elif move == "a":
        if not check_if_wall(board, pacman_position, vertical=-1):
            new_pacman_position = go_left(pacman_position, new_pacman_position)
        else:
            new_pacman_position = pacman_position
    elif move == "d":
        if not check_if_wall(board, pacman_position, vertical=1):
            new_pacman_position = go_right(pacman_position, new_pacman_position)
        else:
            new_pacman_position = pacman_position
    return new_pacman_position


def go_up(last_position, new_position):
    """
            Define Pacman's or Ghost's position when moving up.

            Parameters: last_position (list) : Current hero's position on the board.
                        new_position (list) : Next hero's position on the board.
            Returns: new_position (list) : Hero's position after move.
    """
    new_position[0] = last_position[0] - 1
    new_position[1] = last_position[1]
    return new_position


def go_down(last_position, new_position):
    """
            Define Pacman's or Ghost's position when moving down.

            Parameters: last_position (list) : Current hero's position on the board.
                        new_position (list) : Next hero's position on the board.
            Returns: new_position (list) : Hero's position after move.
    """
    new_position[0] = last_position[0] + 1
    new_position[1] = last_position[1]
    return new_position


def go_left(last_position, new_position):
    """
            Define Pacman's or Ghost's position when moving left.

            Parameters: last_position (list) : Current hero's position on the board.
                        new_position (list) : Next hero's position on the board.
            Returns: new_position (list) : Hero's position after move.
    """
    new_position[0] = last_position[0]
    new_position[1] = last_position[1] - 1
    return new_position


def go_right(last_position, new_position):
    """
            Define Pacman's or Ghost's position when moving right.

            Parameters: last_position (list) : Current hero's position on the board.
                        new_position (list) : Next hero's position on the board.
            Returns: new_position (list) : Hero's position after move.
    """
    new_position[0] = last_position[0]
    new_position[1] = last_position[1] + 1
    return new_position


def move_ghosts(board, ghosts_positions, pacman_position, ghost_3):
    """
            Move Ghosts, depending on their number.

            Parameters: board (list) : Game board
                        ghosts_positions (list) : Current Ghosts' positions on the board.
                        pacman_position (list) : Current Pacman's position on the board.
                        ghost_3 (str) : Attribute to define move for Ghost 3.
            Returns: new_ghosts_positions (list) : Ghosts' position after their move.
    """
    new_ghosts_positions = []
    ghost_number = 1
    for ghost in ghosts_positions:
        if ghost_number == 1:
            new_ghosts_positions.append(move_ghost_1(board, ghost))
        elif ghost_number == 2:
            new_ghosts_positions.append(move_ghost_2(board, ghost, pacman_position))
        elif ghost_number == 3:
            new_ghosts_positions.append(move_ghost_3(board, ghost, pacman_position, ghost_3))
        ghost_number += 1
    return new_ghosts_positions


def move_ghost_1(board, ghost_position):
    """
            Move Ghost 1.

            Parameters: board (list) : Game board
                        ghost_position (list) : Current Ghost's position on the board.
            Returns: new_ghost_position (list) : Ghost's position after its move.
    """
    ghost_moved = False
    new_ghost_position = [0, 0]
    while not ghost_moved:
        direction = random.randint(0, 3)
        if direction == 0:
            if not check_if_wall(board, ghost_position, horizontal=-1):
                new_ghost_position = go_up(ghost_position, new_ghost_position)
                ghost_moved = True
        if direction == 1:
            if not check_if_wall(board, ghost_position, horizontal=1):
                new_ghost_position = go_down(ghost_position, new_ghost_position)
                ghost_moved = True
        if direction == 2:
            if not check_if_wall(board, ghost_position, vertical=-1):
                new_ghost_position = go_left(ghost_position, new_ghost_position)
                ghost_moved = True
        if direction == 3:
            if not check_if_wall(board, ghost_position, vertical=1):
                new_ghost_position = go_right(ghost_position, new_ghost_position)
                ghost_moved = True
    return new_ghost_position


def move_ghost_2(board, ghost_position, pacman_position):
    """
            Move Ghost 2.

            Parameters: board (list) : Game board
                        ghost_position (list) : Current Ghost's position on the board.
                        pacman_position (list) : Current Pacman's position on the board.
            Returns: new_ghost_position (list) : Ghost's position after  its move.
    """
    new_ghost_position = [0, 0]
    min_distance = count_distances_to_pacman(board, ghost_position, pacman_position)
    if min_distance == 0:
        new_ghost_position = go_up(ghost_position, new_ghost_position)
    elif min_distance == 1:
        new_ghost_position = go_down(ghost_position, new_ghost_position)
    elif min_distance == 2:
        new_ghost_position = go_left(ghost_position, new_ghost_position)
    elif min_distance == 3:
        new_ghost_position = go_right(ghost_position, new_ghost_position)
    return new_ghost_position


def count_distances_to_pacman(board, ghost_position, pacman_position):
    """
            Define distances between Ghost and Pacman. Needed to define the movement of Ghost 2.

            Parameters: board (list) : Game board
                        ghost_position (list) : Current Ghost's position on the board.
                        pacman_position (list) : Current Pacman's position on the board.
            Returns: distances.index(tmp) (int) : Index of the lowest distance between Pacman and Ghost.
    """
    distances = []
    if not check_if_wall(board, ghost_position, horizontal=-1):
        distances.append(count_distance(ghost_position, pacman_position, horizontal=-1))
    else:
        distances.append(1000)
    if not check_if_wall(board, ghost_position, horizontal=1):
        distances.append(count_distance(ghost_position, pacman_position, horizontal=1))
    else:
        distances.append(1000)
    if not check_if_wall(board, ghost_position, vertical=-1):
        distances.append(count_distance(ghost_position, pacman_position, vertical=-1))
    else:
        distances.append(1000)
    if not check_if_wall(board, ghost_position, vertical=1):
        distances.append(count_distance(ghost_position, pacman_position, vertical=1))
    else:
        distances.append(1000)
    tmp = min(distances)
    return distances.index(tmp)


def count_distance(ghost_position, pacman_position, horizontal=0, vertical=0):
    """
            Count distance between Ghost and Pacman.

            Parameters: ghost_position (list) : Current Ghost's position on the board.
                        pacman_position (list) : Current Pacman's position on the board.
                        vertical/ horizontal (int) : Modifiers needed to access neighbouring fields on the board.
            Returns: distance (float) : Distance between Pacman and Ghost.
    """
    distance = math.sqrt(((ghost_position[0] + horizontal) - pacman_position[0]) ** 2 + (
            ghost_position[1] + vertical - pacman_position[1]) ** 2)
    return distance


def move_ghost_3(board, ghost_position, pacman_position, ghost_3):
    """
            Move Ghost 3.

            Parameters: board (list) : Game board
                        ghost_position (list) : Current Ghost's position on the board.
                        pacman_position (list) : Current Pacman's position on the board.
                        ghost_3 (str) : Attribute to define Ghost's 3 movement.
            Returns: new_ghost_position (list) : New ghost's position.
    """
    if ghost_3 == "ghost_1":
        new_ghost_position = move_ghost_1(board, ghost_position)
    elif ghost_3 == "ghost_2":
        new_ghost_position = move_ghost_2(board, ghost_position, pacman_position)
    return new_ghost_position


def change_ghost_3(ghost_3):
    """
            Switch attribute ghost_3 to determine the next behavior of Ghost 3.

            Parameters: ghost_3 (str) : Attribute to define Ghost's 3 movement.
            Returns: ghost_3 (str) : Attribute to define Ghost's 3 movement.
    """
    if ghost_3 == "ghost_1":
        ghost_3 = "ghost_2"
    else:
        ghost_3 = "ghost_1"
    return ghost_3


def prepare_ghosts_next_round(new_ghosts_positions, ghost_3):
    """
            Prepare Ghosts for the next round

            Parameters: new_ghosts_positions (list) : Current Ghosts' positions on the board.
                        ghost_3 (str) : Attribute to define Ghost's 3 movement.
            Returns: last_ghosts_positions (list) : Last Ghosts' positions on the board.
                    ghost_3 (str) : Attribute to define Ghost's 3 movement.
    """
    last_ghosts_positions = []
    for new_ghost_position in new_ghosts_positions:
        last_ghosts_positions.append(new_ghost_position)
    ghost_3 = change_ghost_3(ghost_3)
    return last_ghosts_positions, ghost_3


def main():
    print("--- WELCOME TO PACMAN GAME! --- ")
    # Game preparation and global variables
    board = read_board("pacman_board.txt")
    log_board = copy.deepcopy(board)
    victory = False
    defeat = False
    ghost_3 = "ghost_1"
    next_places = [" ", " ", " "]
    last_pacman_position = get_position("pacman", board)
    dots_counter = count_dots(board)
    log_board = log_pacman_moves(log_board, last_pacman_position)
    last_ghosts_positions = get_position("ghost", board)

    while not victory and not defeat:
        display_board(board)
        # Pacman moves
        new_pacman_position = move_pacman(board, last_pacman_position)
        log_board = log_pacman_moves(log_board, new_pacman_position)
        dots_counter = recount_dots(board, new_pacman_position, dots_counter)

        # Check if game ends after Pacman's move
        victory = check_victory(dots_counter)
        defeat = check_defeat(new_pacman_position, last_ghosts_positions)
        if victory or defeat:
            break

        # Ghosts move
        new_ghosts_positions = move_ghosts(board, last_ghosts_positions, new_pacman_position, ghost_3)

        # Board update
        board = update_board_pacman(board, last_pacman_position, new_pacman_position)
        board = update_board_characters(board, last_ghosts_positions, next_places)
        next_places = get_next_place_in_board(board, log_board, new_ghosts_positions, last_ghosts_positions)
        board = update_board_ghosts(board, new_ghosts_positions)
        # Check if game ends after Ghosts' move
        victory = check_victory(dots_counter)
        defeat = check_defeat(new_pacman_position, new_ghosts_positions)
        if victory or defeat:
            break

        # Preparations for next round
        last_pacman_position = get_position("pacman", board)
        last_ghosts_positions, ghost_3 = prepare_ghosts_next_round(new_ghosts_positions, ghost_3)


if __name__ == "__main__":
    main()
