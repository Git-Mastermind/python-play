base_numbers = {
    1:"one",
    2:"two",
    3:"three",
    4:"four",
    5:"five",
    6:"six",
    7:"seven",
    8:"eight",
    9:"nine",
}

tens = {
    2:"twenty",
    3:"thirty",
    4:"fourty",
    5:"fifty",
    6:"sixty",
    7:"eighty",
    9:"ninety"
}

teens = {
    11:"eleven",
    12:"twelve",
    13:"thirteen",
    14:"fourteen",
    15:"fifteen",
    16:"sixteen",
    17:"seventeen",
    18:"eighteen",
    19:"nineteen"
}

number = input("Enter a number: ")

if len(base_numbers[int(number)]) == 4:
    thousands = number[0]
    hundreds = 0
    tens = 0
    if int(number[1]) == 0:
        if int(number[2]) == 1:
            tens = teens[int(f"{number[2]}{number[3]}")]
            print(f"{thousands} thousand and {tens}")
            