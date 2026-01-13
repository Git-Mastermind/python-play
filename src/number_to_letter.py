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
    7:"seventy",
    8:"eighty",
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
thousands_place = base_numbers[int(number[0])]
# hundreds_place = base_numbers[int(number[1])]


if int(number) < 1 or len(number) > 4:
    print("nope")
else:
    if len(number) == 1:
        base_numbers[int(number)]
        print(f"{base_numbers[int(number)]}")
        quit()

    elif len(number) == 2:
        tens_place = tens[int(number[0])] + " " + base_numbers[int(number[1])]
        print(f"{tens_place}")
        quit()

    elif len(number) == 3:
        hundreds_place = number[0]
        if int(number[1]) == 0:
            tens_place = base_numbers[int(number[2])]
        else:
            if int(number[1]) < 2:
                tens_place = teens[int(f"{number[1]}{number[2]}")]
            else:
                tens_place = tens[int(number[1])] + " " + base_numbers[int(number[2])]
        print(f"{base_numbers[int(hundreds_place)]} hundred and {tens_place}")
    
    elif len(number) == 4:
        if int(number[1]) == 0:
            if int(number[2]) == 1:
                tens_place = teens[int(f"{number[2]}{number[3]}")]
            elif int(number[2]) == 0:
                tens_place = base_numbers[int(number[3])]
            else:
                tens_place = tens[int(number[2])] + " " + base_numbers[int(number[3])]
            print(f"{thousands_place} thousand and {tens_place}")
        elif int(number[2]) == 0:
            hundreds_place = number[1]
            tens_place = base_numbers[int(number[3])]
            print(f"{thousands_place} thousand {base_numbers[int(hundreds_place)]} hundred and {tens_place}")
        else:
            hundreds_place = number[1]
            if int(number[2]) < 2:
                tens_place = teens[int(f"{number[2]}{number[3]}")]
            else:
                tens_place = tens[int(number[2])] + " " + base_numbers[int(number[3])]
                print(f"{thousands_place} thousand {base_numbers[int(hundreds_place)]} hundred and {tens_place}")

            
        quit()

