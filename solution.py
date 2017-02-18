assignments = []

# Rows and columns are shared between below methods
rows = 'ABCDEFGHI'
cols = '123456789'
all_values = '123456789'
units = {}

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

def cross(A, B):
    "Cross product of elements in A and elements in B."
    pass

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

    grid_map = {}

    # Initialise an empty grid, for visualisation
    for row in rows:
        for col in cols:
            grid_map[row+col]='';

    # Empty map
    assignments.append(grid_map.copy())

    i = 0;
    for row in rows:
        for col in cols:
            grid_map[row+col] = all_values if grid[i]=='.' else grid[i]
            i+=1

    # First map
    assignments.append(grid_map.copy())

    return grid_map


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    assignments.append(values.copy())

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
    """
    Eliminate all impossible possibilities from a board
    :param values: a map represent the sudoku board
    :return:
    """

    units = unit_map()

    updated = True

    while updated:
        updated = False
        for unit in units.values():
            for cell in unit:
                if len(values[cell]) == 1:
                    for other_cell in unit:
                        if cell!=other_cell:
                            if values[cell][0] in values[other_cell]:
                                updated = True
                                values = assign_value(
                                    values,
                                    other_cell,
                                    values[other_cell].replace(values[cell], '', 1)
                                )

    return values

def only_choice(values):
    pass

def reduce_puzzle(values):
    pass

def search(values):
    pass

def get_paths_for_grid(grid):
    # Number of branches/possibilities (2..9) to check
    for branches_count in range(2,10):
        for row in rows:
            for col in cols:
                location = row+col
                if len(grid[location])==branches_count:
                    # Let's branch off this cell
                    for posible_value in grid[location]:
                        yield (location,posible_value)

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
    values = eliminate(values)

    # Make an assumption and go deeper
    for location, value in get_paths_for_grid(values):
        # Backup
        current_values = values.copy()
        # Make change and recursively check for next version
        assign_value(values,location,value)
        # If this path succeed, return it for pickup by solve or solve_with_map
        solve_with_map(values)
        if (verify(values)):
            return values
        # Otherwise, restore
        values = current_values

    # Now that we've tried everything we could
    return values

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
