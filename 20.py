import utils

input_str = utils.get_input("20")


class Item:
    def __init__(self, value=None, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

    def __str__(self):
        return f"{self.prev.value if self.prev else 'None'} -> {self.value} -> {self.next.value if self.next else 'None'}\n"


class LinkedList:
    def __init__(self, start: int = None):
        self.start = Item(start)
        self.start.next, self.start.prev = self.start, self.start

    def push(self, number):
        if self.start.value is None:
            self.start.value = number
            return self.start
        item = Item(number, self.start.prev, self.start)
        item.prev.next, item.next.prev = item, item
        return item

    def move(self, item, size):
        offset = item.value
        if offset == 0:
            return
        s = item
        self.remove(item)
        dir = offset / abs(offset)
        offset = abs(offset) % (size - 1)
        while offset > 0:
            s = s.next if dir > 0 else s.prev
            offset -= 1
        self.insert(item, s if dir > 0 else s.prev)

    def remove(self, item):
        item.prev.next, item.next.prev = item.next, item.prev
        if item == self.start:
            self.start = item.next

    def insert(self, item, after):
        item.prev, item.next = after, after.next
        item.prev.next, item.next.prev = item, item
        if after == self.start.prev:
            self.start = after


def parse_input(input_str, decryption_key=1) -> (LinkedList, list, Item):
    zero = None
    item_order = []
    linked_list = LinkedList()
    for item_str in input_str.split('\n'):
        item = int(item_str) * decryption_key
        item_order.append(linked_list.push(item))
        if item == 0:
            zero = item_order[-1]
    return linked_list, item_order, zero


def solve_p1(input_str):
    linked_list, item_order, zero = parse_input(input_str)
    for item in item_order:
        linked_list.move(item, len(item_order))
    item = zero
    res = []
    for i in range(1, 3001):
        item = item.next
        if i % 1000 == 0:
            res.append(item.value)
    return sum(res)


def solve_p2(input_str):
    linked_list, item_order, zero = parse_input(input_str, 811589153)
    for i in range(10):
        for item in item_order:
            linked_list.move(item, len(item_order))
    item = zero
    res = []
    for i in range(1, 3001):
        item = item.next
        if i % 1000 == 0:
            res.append(item.value)
    return sum(res)


part1 = utils.time_function(solve_p1, input_str)
print(part1)
part2 = utils.time_function(solve_p2, input_str)
print(part2)
