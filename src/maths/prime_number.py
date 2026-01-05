from datetime import datetime
def check_prime_number(num):
    start_time = datetime.now()  # starting the timer
    factors = []  # empty list for factors
    for i in range(1, num + 1):
        if num % i == 0:  # if the number is a factor
            factors.append(i)  # append to the factors list
    end_time = datetime.now()  # after the loop runs, mark the end time
    run_time = end_time - start_time

    if factors == [1, num]:  # if the number is a prime number
        return "✅ prime number", run_time  # return that it is a prime number and the run time
    else:
        return "☑️ not prime number", run_time  # return that it is not a prime number and the run time

num = int(input("Number: "))  # getting the number from the user

answer = check_prime_number(num)  # output of the function (TUPLE) goes into answer

prime_number_check = answer[0]  # first part goes into a variable

run_time = answer[1]  # runtime also goes in a variable

print(prime_number_check)  # print if it is a prime number

print(run_time)  # print the runtime