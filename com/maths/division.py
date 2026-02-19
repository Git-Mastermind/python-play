def divide(dividend, divisor):
    remainder = dividend    # So that when the divisor is greator than the dividend, the remainder is already set
    quotient = 0
    if divisor == 0:
        raise ZeroDivisionError("Cannot divide by zero!")  # If the divisor is 0 (undefined) than raise ZeroDivisionError with a message
    while remainder >= divisor: 
        remainder = dividend - divisor  # Keep doing this until the remainder is less than the divisor 
        dividend = remainder   # So that when we subtract again, the dividend won't be the same, because if it was, it would result in an infinite while loop
        quotient += 1   # Each successful loop, the quotient increases by one
    return quotient, remainder  # In the end, return the quotient and the remainder




# print(test_division_is_successful()) # Calling the test function

