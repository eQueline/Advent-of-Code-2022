import re
import utils

input_str = utils.get_input("21")


class Monkey:
    def __init__(self, value, left=None, right=None, op=None):
        self.value = value
        self.left = left
        self.right = right
        self.op = op

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

    def __str__(self):
        if self.left is None:
            return str(self.value)
        return " ".join((str(self.left), self.op, str(self.right))) + " = " + str(self.value)

def init(input_str):
    monkeys_dict = {}
    for line in input_str.split("\n"):
        m = re.findall(r'([a-z0-9+\-*/]+)', line)
        if len(m) == 2:
            monkeys_dict[m[0]] = Monkey(int(m[1]))
        else:
            monkeys_dict[m[0]] = Monkey(None, m[1], m[3], m[2])
    return monkeys_dict


def calculate_monkeys(monkeys, skip_root=False):
    number_monkeys = [m for m in monkeys if monkeys[m].value is not None]
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
                if skip_root and monkey_name == "root":
                    continue
                monkey.calculate()
                number_monkeys.append(monkey_name)


def solve_p1(input_str):
    monkeys = init(input_str)
    calculate_monkeys(monkeys)
    return monkeys["root"].value


def solve_p2(input_str):
    monkeys = init(input_str)
    monkeys.pop("humn")
    calculate_monkeys(monkeys, skip_root=True)

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
        if monkey_name == "root":
            value = operand
        elif monkey.op == "+":
            value = monkey.value - operand
        elif monkey.op == "-":
            if variable == monkey.left:
                value = monkey.value + operand
            else:
                value = operand - monkey.value
        elif monkey.op == "*":
            value = monkey.value // operand
        elif monkey.op == "/":
            if variable == monkey.left:
                value = monkey.value * operand
            else:
                value = operand // monkey.value
        if variable == "humn":
            return value
        monkeys[variable].value = value
        equations.append(variable)


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, input_str)
print("Part 2:", part2)
