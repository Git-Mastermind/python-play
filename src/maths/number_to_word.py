base_numbers = {
    0:"zero",
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
    1:"ten",
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


def number_to_word(number):
    number = str(number)
    thousands_place = base_numbers[int(number[0])]
    # hundreds_place = base_numbers[int(number[1])]


    if int(number) < 0 or len(number) > 4:
        raise Exception("Invalid Number Length. Provide number 0-9999")
    else:
        if len(number) == 1:
            base_numbers[int(number)]
            print(f"{base_numbers[int(number)]}")
            quit()

        elif len(number) == 2:
            if int(number[1]) == 0:
                tens_place = tens[int(number[0])]
            else:
                tens_place = tens[int(number[0])] + " " + base_numbers[int(number[1])]
            print(f"{tens_place}")

        elif len(number) == 3:
            hundreds_place = number[0]
            if int(number[1]) == 0:
                tens_place = base_numbers[int(number[2])]

            else:
                if int(number[1]) < 2:
                    tens_place = teens[int(f"{number[1]}{number[2]}")]

                else:
                    if int(number[2]) == 0:
                        tens_place = tens[int(number[1])]

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

            elif int(number[3]) == 0:
                hundreds_place = number[1]
                tens_place = tens[int(number[2])]

                print(f"{thousands_place} thousand {base_numbers[int(hundreds_place)]} hundred and {tens_place}")

            else:
                hundreds_place = number[1]

                if int(number[2]) < 2:
                    tens_place = teens[int(f"{number[2]}{number[3]}")]

                else:
                    tens_place = tens[int(number[2])] + " " + base_numbers[int(number[3])]
                    print(f"{thousands_place} thousand {base_numbers[int(hundreds_place)]} hundred and {tens_place}")


                
            
def find_place_values(number):
    quotient = number
    remainder = 0

    while quotient >= 10:
        remainder = quotient % 10
        quotient = quotient // 10
        print(remainder)
    print(quotient)
        

def number_to_word_place_value(number):
    place_values = []
    quotient = number
    remainder = 0
    while quotient >= 10:
        remainder = quotient % 10
        quotient = quotient // 10
        place_values.append(remainder)
    place_values.append(quotient)
    ones = base_numbers[place_values[0]]

    if len(place_values) == 1:
        print(f"{ones}")
    
    elif len(place_values) == 2:
        tens_place = tens[place_values[1]]
        if place_values[0] == 0:
            print(f"{tens_place}")
        else:
            print(f"{tens_place} {ones}")
    
    elif len(place_values) == 3:
        tens_place = tens[place_values[1]]
        if place_values[1] == 0:
            hundreds_place = base_numbers[place_values[2]]
            print(f"{hundreds_place} hundred and {tens_place}")
        hundreds_place = base_numbers[place_values[2]]
        print(f"{hundreds_place} hundred and {tens_place} {ones}")
    
    elif len(place_values) == 4:
        tens_place = tens[place_values[1]]
        hundreds_place = base_numbers[place_values[2]]
        thousands_place = base_numbers[place_values[3]]

        print(f"{thousands_place} thousand {hundreds_place} hundred and {tens_place} {ones}")
    
        

number = int(input("Number: "))
number_to_word_place_value(number)
    