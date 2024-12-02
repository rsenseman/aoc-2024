from dataclasses import dataclass
from typing import List

DELTA_MIN = 1
DELTA_MAX = 3
MAX_DAMPS = 1

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

    def is_monotonic(self):
        deltas = [x-y for x,y in zip(self.data[1:], self.data[:-1])]

        is_positive = lambda v: v > 0
        is_negative = lambda v: v < 0

        return (
            all(map(is_positive, deltas)) or \
            all(map(is_negative, deltas))
        )

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
        return self.is_monotonic() and self.are_deltas_in_range()
    
class LevelWithProblemDampener(Level):
    def is_monotonic_problem(self, delta, sign:str):
        if sign == 'positive':
            check_function = lambda v: v > 0
        elif sign == 'negative':
            check_function = lambda v: v < 0
        else:
            raise Exception('sign must be `positive` or `negative`')
        
        return not check_function(delta)

    def is_scale_problem(self, delta):
        delta_abs = abs(delta)

        return not (
            (delta_abs <= DELTA_MAX) and (delta_abs >= DELTA_MIN)
        )
    
    def is_safe_one_way(self, forward_or_backward:str, positive_or_negative:str):
        assert forward_or_backward in ('forward', 'backward'), 'forward_or_backward must be `forward` or `backward`'
        assert positive_or_negative in ('positive', 'negative'), 'positive_or_negative must be `positive` or `negative`'

        if forward_or_backward == 'forward':
            current, the_rest = self.data[0], self.data[1:]
        else:
            current, the_rest = self.data[-1], self.data[-2::-1]

        print()
        steamroll_counter = 0

        for next in the_rest:
            is_monotonic_problem = self.is_monotonic_problem(next-current, sign=positive_or_negative)
            is_scale_problem = self.is_scale_problem(next-current)

            print(steamroll_counter, is_monotonic_problem, is_scale_problem)
            if is_monotonic_problem or is_scale_problem:
                steamroll_counter += 1
                if steamroll_counter > MAX_DAMPS:
                    return False
                else:
                    continue
            else:
                current = next # only basic datatypes can be reassigned without getting miffed here
        else:
            return True

    @property
    def is_safe(self):
        return any(
            self.is_safe_one_way(forward_or_backward, positive_or_negative)
            for forward_or_backward in ['forward', 'backward']
            for positive_or_negative in ['positive', 'negative']
        )
    
def solve_part1(data):
    levels = [Level.from_line(line) for line in data]

    return sum(int(level.is_safe) for level in levels)

def solve_part2(data):
    num_safe = 0
    for i, line in enumerate(data):
        level = LevelWithProblemDampener.from_line(line)
        is_safe = level.is_safe
        print(f'{i+1}: {is_safe}')
        if is_safe:
            num_safe += 1
    return num_safe

if __name__ == '__main__':
    # data_dirty = get_data('./data_test.txt')
    # data = clean_data(data_dirty)
    # answer = solve_part1(data)
    # print(answer)

    # data_dirty = get_data()
    # data = clean_data(data_dirty)
    # answer = solve_part1(data)
    # print(answer)

    # data_dirty = get_data('./data_test.txt')
    # data = clean_data(data_dirty)
    # answer = solve_part2(data)
    # print(answer)

    data_dirty = get_data()
    data = clean_data(data_dirty)
    answer = solve_part2(data)
    print(answer)