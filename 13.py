import requests
import main
import functools

input_str = "[1,1,3,1,1]\n\
[1,1,5,1,1]\n\
\n\
[[1],[2,3,4]]\n\
[[1],4]\n\
\n\
[9]\n\
[[8,7,6]]\n\
\n\
[[4,4],4,4]\n\
[[4,4],4,4,4]\n\
\n\
[7,7,7,7]\n\
[7,7,7]\n\
\n\
[]\n\
[3]\n\
\n\
[[[]]]\n\
[[]]\n\
\n\
[1,[2,[3,[4,[5,6,7]]]],8,9]\n\
[1,[2,[3,[4,[5,6,0]]]],8,9]\n"
input_str = requests.get('https://adventofcode.com/2022/day/13/input', cookies={"session": main.SESSION_ID}).text


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


pairs = []
for x in input_str[:-1].split("\n\n"):
    strings = x.split("\n")
    pair = []
    for string in strings:
        pair_arr, _ = parse(string)
        pair.append(pair_arr)
    pairs.append(pair)


# Part 1
idx_list = []
for idx, pair in enumerate(pairs):
    if compare(pair[0], pair[1]) > 0:
        idx_list.append(idx+1)

print(sum(idx_list))


# Part 2
pairs = []
for x in input_str[:-1].split("\n\n"):
    strings = x.split("\n")
    for string in strings:
        pair_arr, length = parse(string)
        pairs.append(pair_arr)
divider1, divider2 = [[2]], [[6]]
pairs.append(divider1)
pairs.append(divider2)

cmp = functools.cmp_to_key(compare)
pairs.sort(key=cmp)
pairs.reverse()
print((pairs.index(divider1)+1) * (pairs.index(divider2)+1))
