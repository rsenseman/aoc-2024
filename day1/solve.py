from collections import Counter

def get_data(input='./data.txt'):
    with open(input) as f:
        contents = f.readlines()

    return contents

def clean_data(data_dirty):
    clean_lines = [line.strip().split() for line in data_dirty]
    clean_contents = [[int(x), int(y)] for x,y in clean_lines]
    return clean_contents

def solve_part1(data):
    x_all, y_all = list(zip(*data))
    x_sorted, y_sorted = sorted(x_all), sorted(y_all)

    total_distance = sum(abs(x-y) for x,y in zip(x_sorted, y_sorted))

    return total_distance

def solve_part2(data):
    x_all, y_all = list(zip(*data))
    candidates = set(x_all)

    y_counts = Counter(y_all)
    score_parts = {x * y_counts.get(x, 0) for x in x_all}

    similarity_score = sum(score_parts)
    return similarity_score

if __name__ == '__main__':
    if False:
        data_dirty = get_data('./data_test.txt')
        data = clean_data(data_dirty)
        answer = solve_part1(data)
        print(answer)

        data_dirty = get_data()
        data = clean_data(data_dirty)
        answer = solve_part1(data)
        print(answer)

    if True:
        data_dirty = get_data('./data_test.txt')
        data = clean_data(data_dirty)
        answer = solve_part2(data)
        print(answer)

        data_dirty = get_data()
        data = clean_data(data_dirty)
        answer = solve_part2(data)
        print(answer)