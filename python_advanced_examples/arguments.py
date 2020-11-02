def myfunc(*args):  # -> treat undefined number of input parameters as tuple
    print(args)


def myfunc2(**kwargs):
    print(kwargs)


def myfunc3(*args, **kwargs):
    print(args, kwargs)


def myfunc4(a, b):
    print(a + b)


if __name__ == '__main__':
    myfunc(1, 2, 3, 4, 5)
    myfunc(1, 2, 3, 4, 5, 6, 7, 8, "pizza")

    myfunc2(price=12)
    myfunc2(price=12, food=["butter", "bread"])

    myfunc3(1, 2, 3, 4, 5, 6, 7, 8, "pizza", price=12, food=["butter", "bread"])

    myfunc3(1, 2, 3, 4, 5, 6, 7, 8, "pizza", food=["butter", "bread"], price=12)

    myfunc4(*(4, 5))
