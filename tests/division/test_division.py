from src.division import divide

def test_division_is_successful(dividend, divisor, expected_quotient, expected_remainder):     # Divisor, what we will pas through the function above
    answer = divide(dividend, divisor)  # Calling the function and passing through our dividend and divisor. return type: TUPLE
    quotient = answer[0] # quotient is the first element in the tuple
    remainder = answer[1] # remainder is the second element in the tuple

    if quotient == expected_quotient and remainder == expected_remainder:  # if the quotient and remainder was what we expected 
        return "✅ General division is a success!"  # Success!
    else:
        return f"❌ Expected {expected_quotient} quotient, got {quotient}, Expected {expected_remainder} remainder, got {remainder}"  # Incorrect, and what the quotient and remainders were 

print(test_division_is_successful(27, 4, 6, 3))