import math

def logarithms(result, base):
    power_counter = 0
    while result != 1:
        result /= base
        power_counter += 1
    return power_counter


print(logarithms(16, 2))

