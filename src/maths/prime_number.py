from datetime import datetime
def check_prime_number(num):  # RETURNS: Boolean for is_prime, and run time
    start_time = datetime.now()  # starting the timer
    factors = []  # empty list for factors
    for i in range(1, num + 1):
        if num % i == 0:  # if the number is a factor
            factors.append(i)  # append to the factors list
    end_time = datetime.now()  # after the loop runs, mark the end time
    run_time = end_time - start_time

    if factors == [1, num]:  # if the number is a prime number
        return True, run_time  # return that it is a prime number and the run time
    else:
        return False, run_time  # return that it is not a prime number and the run time


