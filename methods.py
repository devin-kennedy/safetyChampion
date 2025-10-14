
# Returns the x, y coordinate of a 1d list in a 2d array with a given size
def xy_by_index(i: int, size: int):
    return divmod(i, size)


# Returns a list of surrounding valid positions from the origin
def surrounding_cells(size: int, pos: tuple[int, int]):
    cells = []
    ns = [-1, 0, 1]
    for x in ns:
        for y in ns:
            if 0 <= pos[0] + x < size and 0 <= pos[1] + y < size and ((x, y) != (0, 0)):
                cells.append((x + pos[0], y + pos[1]))
    return cells


# Returns a list of all cells in a row excluding the origin
# hashtag segregate list comprehensions
def row_cells(size: int, pos: tuple[int, int]):
    return [(pos[0], i) for i in range(size) if i != pos[1]]


# Same thing as above but with col
def col_cells(size: int, pos: tuple[int, int]):
    return [(i, pos[1]) for i in range(size) if i != pos[0]]


# Returns if the cell rgb value is in the list of known rgb values within a certain tolerance
# Returns either known value or None
def check_rgb(cell_rgb: tuple, all_rgb: list, tolerance: int):
    for v in all_rgb:
        dr = abs(cell_rgb[0] - v[0])
        dg = abs(cell_rgb[1] - v[1])
        db = abs(cell_rgb[2] - v[2])
        if dr <= tolerance and dg <= tolerance and db <= tolerance:
            return v
    return None
