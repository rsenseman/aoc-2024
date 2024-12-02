from dataclasses import dataclass
from typing import List

DELTA_MIN = 1
DELTA_MAX = 3

def get_data(input='./data.txt'):
    with open(input) as f:
        contents = f.readlines()

    return contents

def clean_data(data_dirty):
    clean_lines = [line.strip().split() for line in data_dirty]
    clean_contents = [[int(x) for x in inner_list] for inner_list in clean_lines]
    return clean_contents

@dataclass
class Level:
    data: List[int]
    
    @classmethod
    def from_line(cls, line: List[int]):
        return cls(line)

    @property
    def is_monotonic(self):
        deltas = [x-y for x,y in zip(self.data[1:], self.data[:-1])]

        is_positive = lambda v: v > 0
        is_negative = lambda v: v < 0

        return (
            all(map(is_positive, deltas)) or \
            all(map(is_negative, deltas))
        )

    @property
    def are_deltas_in_range(self):
        deltas = [abs(x-y) for x,y in zip(self.data[1:], self.data[:-1])]

        return all(
            [
                (v <= DELTA_MAX) and (v >= DELTA_MIN)
                for v
                in deltas
            ]
        )
    
    @property
    def is_safe(self):
        return self.is_monotonic and self.are_deltas_in_range
    
def solve_part1(data):
    levels = [Level.from_line(line) for line in data]

    return sum(int(level.is_safe) for level in levels)

def solve_part2(data):
    pass

if __name__ == '__main__':
    data_dirty = get_data('./data_test.txt')
    data = clean_data(data_dirty)
    answer = solve_part1(data)
    print(answer)

    data_dirty = get_data()
    data = clean_data(data_dirty)
    answer = solve_part1(data)
    print(answer)

    # data_dirty = get_data('./data_test.txt')
    # data = clean_data(data_dirty)
    # answer = solve_part2(data)
    # print(answer)

    # data_dirty = get_data()
    # data = clean_data(data_dirty)
    # answer = solve_part2(data)
    # print(answer)