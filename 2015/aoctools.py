"""A collection of data structures and algorithms for Advent of Code puzzles."""
import heapq
import os
import requests
from collections import defaultdict

TOKEN = os.getenv('AOC_TOKEN')
if not TOKEN:
    with open('token.txt') as f:
        TOKEN = f.read()

URL = 'https://adventofcode.com/{year}/day/{day}/input'
LOCAL = 'inputs/{day}.txt'

class Data:
    """
    Retrieves puzzle inputs for one puzzle given the day and year.
    Requires TOKEN to be present in environment or a text file.
    """
    @staticmethod
    def fetch(*, day: int, year: int, no_strip=False):
        """Retrieves the raw data from the website."""
        if year < 2015 or not 1 <= day <= 25:
            raise ValueError('Day must be within range 1-25 and year must be after 2015.')

        url = URL.format(year=year, day=day)
        local_path = LOCAL.format(day=day)
        if os.path.exists(local_path):
            with open(local_path) as f:
                if no_strip:
                    return f.read()
                else:
                    return f.read().strip()
        response = requests.get(url, cookies={'session': TOKEN})
        if 'Puzzle inputs differ by user.  Please log in to get your puzzle input.' in response.text:
            raise ValueError('Token has expired. Please go to Applications -> Cookies and get the new token.')
        with open(local_path, 'w') as f:
            f.write(response.text)
        if no_strip:
            return response.text
        else:
            return response.text.strip()

    @staticmethod
    def generator(iterable):
        """Helper method to use generators for parsing data."""
        yield from iterable

    @staticmethod
    def fetch_by_line(*, day: int, year: int, gen=False, no_strip=False):
        """
        Returns an iterable to get data by line.
        Set gen to True to return a generator.
        """
        data_str = Data.fetch(day=day, year=year, no_strip=no_strip)
        if no_strip:
            lines = data_str.split('\n')
        else:
            lines = data_str.strip().split('\n')
        return Data.generator(data_str) if gen else lines

    @staticmethod
    def double_enum(iterable):
        """Nested iteration yielding indices and elements at each loop."""
        for i, row in enumerate(iterable):
            for j, item in enumerate(row):
                yield i, j, item

class Grid2D:
    """Utility class which allows mapping of points onto a grid and 2D movement."""
    def __init__(self, *, default=None):
        self.points = defaultdict(lambda: default)
        self.default = default
        self.max_x = self.max_y = -float('inf')
        self.min_x = self.min_y = float('inf')

    # Movement
    intercardinal = [-1 - 1j, 0 - 1j, 1 - 1j, -1, 1, -1 + 1j, 0 + 1j, 1 + 1j]
    cardinal = [0 - 1j, -1 + 0j, 0 + 1j, 1 + 0j]
    north, west, south, east = cardinal
    
    @property
    def corners(self):
        return [(self.min_x, self.min_y), (self.min_x, self.max_y), (self.max_x, self.min_y), (self.max_x, self.max_y)]
    
    @property
    def x_range(self):
        return self.max_x - self.min_x
    
    @property
    def y_range(self):
        return self.max_y - self.min_y

    def item(self, pos):
        """Returns the current item at the point."""
        return self[self.convert(pos)]

    def convert(self, item):
        """Converts tuples to complex numbers."""
        if type(item) != complex:
            return complex(*item)
        return item

    def revert(self, comp):
        """Converts complex numbers to a tuple (x, y)."""
        return (comp.real, comp.imag)

    def manhattan(self, p1, p2):
        """Computes the manhattan distance to another point."""
        p1, p2 = map(self.convert, (p1, p2))
        return abs(p1.real - p2.real) + abs(p1.imag - p2.imag)

    def __contains__(self, item):
        return self.convert(item) in self.points

    def __getitem__(self, item):
        return self.points[self.convert(item)]

    def __setitem__(self, item, value):
        item = self.convert(item)
        if item.real > self.max_x:
            self.max_x = int(item.real)
        if item.real < self.min_x:
            self.min_x = int(item.real)
        if item.imag > self.max_y:
            self.max_y = int(item.imag)
        if item.imag < self.min_y:
            self.min_y = int(item.imag)
        self.points[item] = value

    def __repr__(self):
        return f'Grid2D(default=\'{self.default}\')'

class Vector:
    """Operations on numeric sequence and <x, y, z> vectors."""
    def __init__(self, *seq):
        self.sequence = seq

    @property
    def x(self):
        """Returns the first element of the sequence."""
        try:
            return self.sequence[0]
        except IndexError:
            print('Vector has no x element.')

    @property
    def y(self):
        """Returns the second element of the sequence."""
        try:
            return self.sequence[1]
        except IndexError:
            print('Vector has no y element.')

    @property
    def z(self):
        """Returns the third element of the sequence."""
        try:
            return self.sequence[2]
        except IndexError:
            print('Vector has no z element.')

    def __add__(self, other):
        return Vector(*(a + b for a, b in zip(self.sequence, other.sequence)))
    __radd__ = __add__

    def __sub__(self, other):
        return Vector(*(a - b for a, b in zip(self.sequence, other.sequence)))
    __rsub__ = __sub__

    def __repr__(self):
        return f'<{", ".join(self.sequence)}>'

class Geometry:
    """Collection of common geometrical methods and values."""
    cardinal = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    intercardinal = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    @staticmethod
    def manhattan(p1, p2):
        """Computes the manhattan distance between two points."""
        return sum(abs(a2 - a1) for a1, a2 in zip(p1, p2))

    @staticmethod
    def neighbors(p):
        """Returns points directly neighboring a given point."""
        return [(p[0] + d[0], p[1] + d[1]) for d in Geometry.cardinal]

    @staticmethod
    def adjacent(p):
        """Returns points adjacent to a point (including diagonals)."""
        return [(p[0] + d[0], p[1] + d[1]) for d in Geometry.intercardinal]

    @staticmethod
    def border_rect(min_p, max_p):
        """A generator which yields points corresponding to the border of a rectangle."""
        x0, y0 = min_p
        x1, y1 = max_p
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if y0 < y < y1 and x0 < x < x1:
                    continue
                yield (x, y)

class PriorityQueue:
    """A data structure in which elements get added according to priority values.
    Lower priority values are retrieved first."""
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def print_ans(puzzle: str, answer: str):
    """Prints the answer to a puzzle in the form `puzzle: answer`."""
    print('Day {}: {}'.format(puzzle, answer))

def prod(iterable):
    """Calculates the product of a list."""
    p = 1
    for x in iterable:
        p *= x
    return p