import time


def calculations(num1, num2):
    return num1 + num2


def calculations2(num1, num2):
    return num1 - num2


if __name__ == '__main__':
    a = 1
    b = 100

    start = time.time()
    result = calculations(a, b)
    end = time.time()
    print("calculations needed ", end-start, "seconds")

    start = time.time()
    result2 = calculations2(a, b)
    end = time.time()
    print("calculations2 needed ", end - start, "seconds")

    c = 400000
    d = 10000000000
    start = time.time()
    result = calculations(c, d)
    end = time.time()
    print("calculations needed ", end-start, "seconds")

    print(f"Result of calculation: {result}")
    print(f"Result of calculation2: {result2}")

# STRG + ALT + SHIFT + L
