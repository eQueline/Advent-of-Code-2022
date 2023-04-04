import utils
import functools

input_str = utils.get_input("13")


def extract_array(data):
    brackets = 0
    for idx, c in enumerate(data):
        if c == "[":
            brackets += 1
        if c == "]":
            brackets -= 1
        if brackets == 0:
            return data[1:idx]


def parse(data):
    res = []
    array = extract_array(data)
    if len(array) == 0:
        return [res, 2]
    i = 0
    number = None
    while i < len(array):
        c = array[i]
        i += 1
        if c == ',':
            if number is not None:
                res.append(number)
            number = None
            continue
        if c == '[':
            number = None
            subarray_str = array[i-1:]
            subarray, length = parse(subarray_str)
            i += length
            res.append(subarray)
            continue
        if number is None:
            number = int(c)
        else:
            number = number * 10 + int(c)
    if number is not None:
        res.append(number)
    return [res, len(array)+2]


def compare(left, right):
    if type(left) is int and type(right) is int:
        if left == right:
            return 0
        return 1 if left < right else -1

    if type(left) is list and type(right) is list:
        for i in range(min(len(left), len(right))):
            checked = compare(left[i], right[i])
            if checked != 0:
                return checked
        if len(left) == len(right):
            return 0
        return 1 if len(left) < len(right) else -1

    return compare(left if type(left) is list else [left],
                   right if type(right) is list else [right])


def init_p1(input_str):
    pairs = []
    for x in input_str.split("\n\n"):
        strings = x.split("\n")
        pair = []
        for string in strings:
            pair_arr, _ = parse(string)
            pair.append(pair_arr)
        pairs.append(pair)
    return pairs

def solve_p1(input_str):
    pairs = init_p1(input_str)
    idx_list = []
    for idx, pair in enumerate(pairs):
        if compare(pair[0], pair[1]) > 0:
            idx_list.append(idx + 1)
    return sum(idx_list)


def init_p2(input_str):
    lines = []
    for x in input_str.split("\n\n"):
        strings = x.split("\n")
        for string in strings:
            line_arr, _ = parse(string)
            lines.append(line_arr)
    return lines


def solve_p2(input_str):
    lines = init_p2(input_str)
    divider1, divider2 = [[2]], [[6]]
    lines.append(divider1)
    lines.append(divider2)
    cmp = functools.cmp_to_key(compare)
    lines.sort(key=cmp)
    lines.reverse()
    return (lines.index(divider1) + 1) * (lines.index(divider2) + 1)


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, input_str)
print("Part 2:", part2)
