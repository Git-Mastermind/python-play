def binary_to_decimal(binary_num):
        num = list[map(int, str(binary_num))]
        num = num[::-1]
        decimal = 0
        for i in range(len(num)):
            decimal += 2**i
        return decimal

print(binary_to_decimal(100))