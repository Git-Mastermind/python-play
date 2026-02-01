def mergeAlternately(word1: str, word2: str) -> str:
    first_word = list(word1)
    second_word = list(word2)
    merged_string = []
    loop_run_time = min(len(first_word), len(second_word))
    for i in range(loop_run_time):

        merged_string.append(first_word[i])

        merged_string.append(second_word[i])

    if len(first_word) > loop_run_time:

        for i in range(loop_run_time - 1, len(first_word)):

            merged_string.append(first_word[i])

        return "".join(merged_string)
    
    elif len(second_word) > loop_run_time:

        for i in range(loop_run_time - 1, len(second_word)):

            merged_string.append(second_word[i])

        return "".join(merged_string)
    else:
        return "".join(merged_string)

print(mergeAlternately(word1="ab", word2="pqrs"))