def reverse(x: int) -> int:
    nums = list(map(int, str(x)))
    reversed_integer = []
    for i in range(len(nums)):
        if i == 0:
            reversed_integer.append(nums[-1]) 
        else:
            reversed_integer.append(nums[-i])
    return int("".join(str(i) for i in reversed_integer))

print(reverse(x=123))