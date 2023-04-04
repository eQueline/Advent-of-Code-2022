import copy
from collections import deque

import requests
import main

input_str = "1\n2\n-3\n3\n-2\n0\n4\n"
input_str = requests.get('https://adventofcode.com/2022/day/20/input', cookies={"session": main.SESSION_ID}).text

numbers = deque()
numbers_idx = {}
numbers_list = []
max_number = 0
for idx, number_str in enumerate(input_str[:-1].split("\n")):
    number = int(number_str)
    numbers.append(number)
    numbers_idx[number] = idx
    numbers_list.append(number)
    max_number = max(max_number, number)

print(numbers)
total_len = len(numbers_list)
for i in range(total_len):
    idx = numbers.index(numbers_list[i])
    numbers.rotate(-idx)
    number = numbers.popleft()
    new_idx = number
    numbers.insert((new_idx - (1 if number < 0 else 0)) % total_len, number + max_number * 5)
    numbers.rotate(idx)

    # print(numbers)
    # printer = []
    # for n in numbers:
    #     if n > total_len * 3:
    #         printer.append(n - total_len * 6)
    #     else:
    #         printer.append(n)
    # print(printer)
for idx, n in enumerate(numbers):
    numbers[idx] = numbers[idx] - max_number * 5
print(numbers)
v1 = numbers[(numbers.index(0) + 1000) % total_len]
v2 = numbers[(numbers.index(0) + 2000) % total_len]
v3 = numbers[(numbers.index(0) + 3000) % total_len]
print(v1, v2, v3)
print(v1 + v2 + v3)
