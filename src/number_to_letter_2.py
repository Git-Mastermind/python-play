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
single_number_for_thousands = base_numbers[int(number[3])]

if len(number) == 4:
    thousands_place = base_numbers[int(number[0])]
    if int(number[1]) == 0:
        if int(number[2]) < 2:
            tens_place = teens[int(f"{number[2]}{number[3]}")]
        else:
            tens_place = tens[int(number[2])] + " " + base_numbers[int(number[3])]
        print(f"{thousands_place} thousand and {tens_place}")

    elif int(number[2]) == 0:
        hundreds_place = base_numbers[number[1]]
        print(f"{thousands_place} thousand {hundreds_place} hundred and {single_number_for_thousands}")

    else:
        hundreds_place = base_numbers[number[1]]
        if int(number[2]) < 2:
            tens_place = teens[int(f"{number[2]}{number[3]}")]
        else:
            tens_place = tens[int(number[2])] + " " + base_numbers[int(number[3])]
        print(f"{thousands_place} thousand {hundreds_place} hundred and {tens_place}")
