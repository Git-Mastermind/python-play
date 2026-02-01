def make_abbreviation(input_word):
    word = list(input_word)
    abbreviation_num = len(word) - 2
    word[0:abbreviation_num] = [str(abbreviation_num)]
    return word




def abbreviation(input_word, input_abbreviation):
    word = list(input_word)
    abbreviation = list(input_abbreviation)
    numbers = ["1", "2", "3", "4", "5", "6" ,"7", "8", "9"]
    number_provided = 0
    letter_count = 0
    for i in range(len(abbreviation)):
        if abbreviation[i] not in numbers:
            if number_provided != 0:
                if abbreviation[i] == word[i + (number_provided - 1)]:
                    letter_count += 1
                else:
                    return f"abbreviation: {make_abbreviation(input_word)}"
            else:
                if abbreviation[i] == word[i]:
                    letter_count += 1
                else:
                    return f"abbreviation: {make_abbreviation(input_word)}"
        else:
            number_provided = int(abbreviation[i])
    if letter_count + number_provided == len(word):
        return "yes"
    
print(abbreviation(input_word="calender", input_abbreviation="c4nder"))
make_abbreviation(input_word="calendar")