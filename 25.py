import utils

inp_str = utils.get_input("25")
SNAFU_MAP = ['=', '-', '0', '1', '2']

def snafu_to_number(snafu):
    number = 0
    for rank, c in enumerate(reversed(snafu)):
        digit = SNAFU_MAP.index(c) - 2
        number += digit * (5 ** rank)
    return number


def number_to_snafu(n):
    snafu = ""
    while n > 0:
        n, digit = divmod(n + 2, 5)
        snafu += SNAFU_MAP[digit]
    return snafu[::-1]


def solve_p1(input_str):
    snafu_list = input_str.split('\n')
    number_sum = 0
    for snafu in snafu_list:
        number_sum += snafu_to_number(snafu)
    return number_to_snafu(number_sum)


def nts(number, string):
    return string if number <= 0 else nts((number + 2) // 5, string + SNAFU_MAP[(number + 2) % 5])


print("Part 1:", utils.time_function(solve_p1, inp_str))


# GOLF version
def r(n,s): return s if n<=0 else r((n+2)//5,s+['=','-','0','1','2'][(n+2)%5])
print(r(sum(sum((['=','-','0','1','2'].index(c)-2)*5**r for r,c in enumerate(s[::-1]))for s in inp_str.split('\n')),'')[::-1])


# One-liner with Inline recursion
print((lambda l:lambda a,b:l(l,a,b))(lambda f,n,s:s if n<=0 else f(f,(n+2)//5,s+['=','-','0','1','2'][(n+2)%5]))
      (sum(sum((['=','-','0','1','2'].index(c)-2)*5**r for r,c in enumerate(s[::-1]))for s in inp_str.split('\n')),'')[::-1])


# Equivalent to:
def f1(f_rec):  # Takes function f_rec as an argument
    def f2(n, s):  # f1 Creates function f2 with 2 arguments
        return f_rec(f_rec, n, s)  # f2 calls f_rec as a function of itself plus 2 provided params
    return f2  # f1 returns f2.
#   f1 needs a function with 3 arguments as parameters.
#   (*) First parameter must be a function that is called inside itself passing itself plus 2 params,
# setting up the recursion
#   f1 will return new function with 2 parameters, call to which that will start the recursion


def f3(f, n, s):  # Recursive implementation of function that is supplied to f1
    if n <= 0:
        return s
    n += 2
    s += ['=', '-', '0', '1', '2'][n % 5]
    return f(f, n//5, s)  # Recursive call that is explained in (*)


num_sum = sum(sum((['=','-','0','1','2'].index(c)-2)*5**r for r, c in enumerate(s[::-1])) for s in inp_str.split('\n'))
f0 = f1(f3)  # Creates function
res = f0(num_sum, '')  # Start recursion
print(res[::-1])
