import time


def time_measure(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{wrapper.__name__}', with parameters: {args}, {kwargs} needed: {end-start} seconds")
        return result
    wrapper.__name__ = func.__name__
    return wrapper


@time_measure
def calculations(num1, num2, num3=10):
    return num1 + num2 + num3


@time_measure
def calculations2(num1, num2):
    return num1 - num2


if __name__ == '__main__':
    a = 1
    b = 100
    c = 20
    result = calculations(a, b, num3=c)
    result2 = calculations2(a, b)

    c = 400000
    d = 10000000000
    result = calculations(c, d)

    print(f"Result of calculation: {result}")
    print(f"Result of calculation2: {result2}")

# STRG + ALT + SHIFT + L
