from src.maths.prime_number import check_prime_number

def check_prime_number_is_successful(num, prime_or_not):
    result = check_prime_number(num)
    is_prime = result[0]
    run_time = result[1]
    if is_prime == bool(prime_or_not):
        print("✅ success")
    else:
        print(f"❌ you expected prime to be {prime_or_not}, but it was {is_prime}")

num = int(input("Number: "))
prime_or_not = input("enter True if prime, False for composite number: ")
check_prime_number_is_successful(num, prime_or_not)