import copy
import re
import requests
import main

input_str = "root: pppw + sjmn\ndbpl: 5\ncczh: sllz + lgvd\nzczc: 2\nptdq: humn - dvpt\ndvpt: 3\nlfqf: 4\nhumn: 5\nljgn: 2\nsjmn: drzm * dbpl\nsllz: 4\npppw: cczh / lfqf\nlgvd: ljgn * ptdq\ndrzm: hmdt - zczc\nhmdt: 32\n"
input_str = requests.get('https://adventofcode.com/2022/day/21/input', cookies={"session": main.SESSION_ID}).text

class Monkey:
    def __init__(self, value, left=None, right=None, op=None):
        self.value = value
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        if self.left is None:
            return str(self.value)
        return " ".join((str(self.left), self.op, str(self.right))) + " = " + str(self.value)

    def can_calculate(self):
        return type(self.left) is not str and type(self.right) is not str

    def calculate(self):
        if not self.can_calculate():
            return None
        if self.op == '+':
            self.value = self.left + self.right
        if self.op == '-':
            self.value = self.left - self.right
        if self.op == '*':
            self.value = self.left * self.right
        if self.op == '/':
            self.value = self.left // self.right
        return self.value


def init():
    monkeys_dict = {}
    for line in input_str[:-1].split("\n"):
        m = re.findall(r'([a-z0-9+\-*/]+)', line)
        if len(m) == 2:
            monkeys_dict[m[0]] = Monkey(int(m[1]))
        else:
            monkeys_dict[m[0]] = Monkey(None, m[1], m[3], m[2])
    return monkeys_dict


# Part 1
monkeys = init()
number_monkeys = [m for m in monkeys if monkeys[m].value is not None]
#print(number_monkeys)
while len(number_monkeys) > 0:
    number_monkey = number_monkeys.pop()
    for monkey_name in monkeys:
        monkey = monkeys[monkey_name]
        if monkey.value is not None:
            continue
        if monkey.left == number_monkey:
            monkey.left = monkeys[number_monkey].value
        if monkey.right == number_monkey:
            monkey.right = monkeys[number_monkey].value
        if monkey.can_calculate():
            #print(f"Calculated monkey {monkey_name}")
            monkey.calculate()
            number_monkeys.append(monkey_name)
print("root", "=", monkeys["root"].value)


# Part 2
monkeys = init()
human = monkeys.pop("humn")
number_monkeys = [m for m in monkeys if monkeys[m].value is not None]
#print(number_monkeys)
while len(number_monkeys) > 0:
    number_monkey = number_monkeys.pop()
    for monkey_name in monkeys:
        monkey = monkeys[monkey_name]
        if monkey.value is not None:
            continue
        if monkey.left == number_monkey:
            monkey.left = monkeys[number_monkey].value
        if monkey.right == number_monkey:
            monkey.right = monkeys[number_monkey].value
        if monkey.can_calculate():
            if monkey_name == "root":
                continue
            #print(f"Calculated monkey {monkey_name}")
            monkey.calculate()
            number_monkeys.append(monkey_name)
monkeys["root"].op = "=="
equations = ["root"]
while len(equations) > 0:
    monkey_name = equations.pop()
    monkey = monkeys[monkey_name]

    if type(monkey.left) is str:
        variable = monkey.left
        operand = monkey.right
    else:
        variable = monkey.right
        operand = monkey.left
    value = 0
    if monkey.op == "==":
        value = operand
    if monkey.op == "+":
        value = monkey.value - operand
    if monkey.op == "-":
        if variable == monkey.left:
            value = monkey.value + operand
        else:
            value = operand - monkey.value
    if monkey.op == "*":
        value = monkey.value // operand
    if monkey.op == "/":
        if variable == monkey.left:
            value = monkey.value * operand
        else:
            value = operand // monkey.value
    if variable == "humn":
        print("humn", "=", value)
        break
    monkeys[variable].value = value
    equations.append(variable)