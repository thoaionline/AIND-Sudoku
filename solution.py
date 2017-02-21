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

max_depth = 0

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
    for unit in unitlist:
        # { value: [location] } dictionary
        value_to_locations = {}
        for location in unit:
            value = values[location]
            if value in value_to_locations:
                value_to_locations[value].append(location)
            else:
                value_to_locations[value] = [location]

        for twin in  [value for (value, locations) in value_to_locations.items() if len(value) == 2 and len(locations) == 2]:
            for other_location in [l for l in unit if values[l]!=twin]:
                for digit in twin:

    return values

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

    print("Max depth: " + str(max_depth))

    if not values:
        print("No solution")
        return

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

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
        naked_twins(values)

        next_checksum = sum(len(box) for box in values.values())
        if next_checksum==last_checksum:
            break
        else:
            last_checksum = next_checksum

    return values

def search(value):
    """
    Search and return all possible paths from current state

    Args:
        value(dict)
    Returns:
        A enumerable of (location, possible_values)
    """
    for row in rows:
        for col in cols:
            location = row + col
            if len(value[location]) > 1:
                # Let's branch off this cell
                for posible_value in value[location]:
                    yield (location, posible_value)

def verify(grid):
    """
    Verify whether the grid is a complete solution.

    This function assumes that the solver is logically correct and only checks for a filled grid.

    :param grid:
        The dictionary representing the grid
    :return:
        True if grid is complete, False otherwise
    """

    for cell_value in grid.values():
        if (len(cell_value)!=1):
            return False

    return True

def solve_with_map(values, level = 1):

    # Record the level
    global max_depth
    max_depth = max(max_depth, level)

    # print("Level "+str(level))
    # display(values)

    # Resolve all trivial boxes
    if not reduce_puzzle(values):
        return False

    assignments.append(values.copy())
    # Make an assumption and go deeper
    for location, value in search(values):
        # Backup
        current_values = values.copy()
        assignments.append(current_values)
        # Make change and recursively check for next version
        assign_value(values,location,value)
        # If this path succeed, return it for pickup by solve or solve_with_map
        sub_solution = solve_with_map(values, level + 1)
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
    global max_depth
    max_depth = 0
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
