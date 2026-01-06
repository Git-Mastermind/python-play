from datetime import datetime
import math
def check_prime_number(num):  
    start_time = datetime.now() 
    is_prime = True
    ending_point = math.ceil(math.sqrt(num)) + 1
    #ending_point = 56893997
    for i in range(2,  ending_point):
        if num % i == 0: 
            print(i)  
            is_prime = False  # found one factor, cannot be prime
            break
    end_time = datetime.now()
    run_time = end_time - start_time 
    print(f"run time: {run_time.total_seconds() * 1000} ms")
    
    return is_prime


# BEFORE: 
# 56893999 took 3327 ms
# 56893990 took 3366 ms

# AFTER:

# 56893990 took 0.048 ms

# BEFORE:
# 56893997 took 3417 ms

# AFTER
# 56893997 took 0.425 ms

print(check_prime_number(56893997))


