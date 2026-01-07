import math

def logarithms(result, base):
    exponent = 0
    if result == 0:
        raise RuntimeError("Invalid result for log")
    while result != 1:
        result /= base
        exponent += 1
    return exponent


print(logarithms(16, 2))

