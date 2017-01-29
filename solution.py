assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

#Implimention of naked twin strategy
#Two boxes have identical values values and hence 
#no other box in the same unit can contain the same value.
#All the boxes in the same unit, which contains Naked Twins, are scanned 
#and occurance of the possible values that can be held by naked twins is removed from other boxes.

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    prune_twins = {key:val for key,val in values.items()}
    for units in unitlist:
        digits = {}
        twin_pairs   = {}
        # Find all pairs of naked twins
        for box in units:
            val = values[box]
            # do only for values with two digits
            if len(val) == 2:
                if val in digits:
                    # Found a naked twin pair
                    twin_pairs[val] = (box, digits[val])
                else:
                    # Found just one box with two digit value
                    digits[val] = box

        # Remove the digits in naked twins, from other boxes 
        #refer http://www.sudokudragon.com/tutorialnakedtwins.htm for more details.
        for twin_value, twin_boxes in twin_pairs.items():
            # Find set of other boxes in the unit
            other_boxes = set(units) - set(twin_boxes)
            for other_box in other_boxes:
                value = values[other_box]
                # Remove both digits of twin pair from other boxes
                newval = value.replace(twin_value[0], '').replace(twin_value[1], '')
                if newval != value:
                    prune_twins= assign_value(prune_twins, other_box, newval)
    return prune_twins

#Extending method/function cross defined in lession 4-- Encoding the Board-- file utils.py 
#Note: the arguments to the function are in caps, as against small letter in lesson 4 
#rest remains the same... 
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

#Again from  lession 4, Encoding the Board, all the variables are taken as it is
#Note: An additional variable diagonal_units to accont for diagonal elements
rows = 'ABCDEFGHI'
cols = '123456789'
width = len(rows) 

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]	  
diagonal_units = [ [ row[idx] for idx, row in enumerate(row_units) ],
               [ row[width - idx - 1] for idx, row in enumerate(row_units) ] ]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#Extending the code in lession 5 -- Strategy1: Elimination -- file utils.py
#This is the first step used for information gain/constraint propogation
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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

#copying the display function in utils.py
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

#refer utils.py and lesson 5: Strategy Elimination
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

#refer utils.py and lesson 6 -- Strategy 2 Only Choice
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

#refer to utils.py lesson 7 -- constraint propogation... 
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        # Call naked twins strat to reduce search space
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

#refer to utils.py and lesson 9 : Strategy 3 Search
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    if isinstance(grid, str):
        grid = grid_values(grid)
    return search(grid)

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
