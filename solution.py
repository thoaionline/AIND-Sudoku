assignments = []

# Rows and columns are shared between below methods
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[(rows[i] + cols[i]) for i in range(0, 9)] for cols in [cols, cols[::-1]]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)

    assert len(values) == 81

    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def unit_map():
    """
    Generate the units
    `units` is a map of arrays, each containing elements in the same group,
    Group are named 1..9 for columns, A..I for rows, and A4, A4,... G7 for blocks, X & Y for the diagonal lines

    :return:
        A dictionary representing the cells in each unit/group

    """

    # Only initiate once
    if len(units)==0:

        # Rows and columns
        for row in rows:
            units[row] = [row+col for col in cols]
        for col in cols:
            units[col] = [row+col for row in rows]

        # 3x3 blocks
        for i,row in enumerate(rows):
            for j,col in enumerate(cols):
                block_name = rows[i-i%3]+cols[j-j%3]
                # Record all units that this cell belong to
                if i%3==0 and j%3==0:
                    # First cell in a block will be used as the block name
                    units[row+col] = [row+col]
                else:
                    # Add the rest of the cells in this block to the unit
                    units[block_name].append(row+col)

        units['X'] = [(rows[i] + cols[i]) for i in range(0, 9)]
        units['Y'] = [(rows[i] + cols[8 - i]) for i in range(0, 9)]

    return units

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    last_checksum = -1

    while True:

        eliminate(values)
        only_choice(values)

        next_checksum = sum(len(box) for box in values.values())
        if next_checksum==last_checksum:
            break
        else:
            last_checksum = next_checksum

    return values

def search(values):
    pass

def get_paths_for_grid(grid):
    # Number of branches/possibilities (2..9) to check
    for row in rows:
        for col in cols:
            location = row + col
            if len(grid[location]) > 1:
                # Let's branch off this cell
                for posible_value in grid[location]:
                    yield (location, posible_value)

def verify(grid):
    """
    Verify whether the grid is a complete solution
    :param grid:
        The dictionary representing the grid
    :return:
        True if grid is complete, False otherwise
    """

    for cell_value in grid.values():
        if (len(cell_value)!=1):
            return False

    return True

def solve_with_map(values):

    # Eliminate all uncertainties
    reduce_puzzle(values)

    assignments.append(values.copy())
    # Make an assumption and go deeper
    for location, value in get_paths_for_grid(values):
        # Backup
        current_values = values.copy()
        assignments.append(current_values)
        # Make change and recursively check for next version
        assign_value(values,location,value)
        # If this path succeed, return it for pickup by solve or solve_with_map
        sub_solution = solve_with_map(values)
        if sub_solution:
            return sub_solution
        # Otherwise, restore and continue
        values = current_values

    # Now that we've tried everything we could
    return values if verify(values) else False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return solve_with_map(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
