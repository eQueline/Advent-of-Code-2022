import requests
import main

input_str = "1\n2\n-3\n3\n-2\n0\n4\n"
input_str = requests.get('https://adventofcode.com/2022/day/20/input', cookies={"session": main.SESSION_ID}).text


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

    def move(self, item):
        offset = item.value
        if offset == 0:
            return
        s = item
        self.remove(item)
        dir = offset / abs(offset)
        offset = abs(offset) % (len(ar)-1)
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

    def __str__(self):
        string = ""
        s = self.start
        while s is not self.start.prev:
            string += str(s) + " "
            s = s.next
        return string


def rotate(array, linked_list):
    for item in array:
        linked_list.move(item)


# Part 1
zero = None
ar = []
ll = None
for x in input_str[:-1].split('\n'):
    n = int(x) * 811589153
    if ll is None:
        ll = LinkedList(n)
        ar.append(ll.start)
        continue
    ar.append(ll.push(n))
    if n == 0:
        zero = ar[-1]
rotate(ar, ll)
s = zero
res = []
for i in range(1, 3001):
    s = s.next
    if i % 1000 == 0:
        res.append(s.value)
print(res, sum(res))


# Part 2
ar = []
ll = None
for x in input_str[:-1].split('\n'):
    n = int(x) * 811589153
    if ll is None:
        ll = LinkedList(n)
        ar.append(ll.start)
        continue
    ar.append(ll.push(n))
    if n == 0:
        zero = ar[-1]
for i in range(10):
    rotate(ar, ll)
s = zero
res = []
for i in range(1, 3001):
    s = s.next
    if i % 1000 == 0:
        res.append(s.value)
print(res, sum(res))
