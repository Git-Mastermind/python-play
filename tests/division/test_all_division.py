from tests.division.test_division import test_division_is_successful
from tests.division.test_zero_division import test_zero_division_error_is_successful

def test_all_division():
    dividend = 6
    divisor = 6
    print(test_division_is_successful(dividend, divisor, dividend//divisor, dividend % divisor))
    divisor = 4
    print(test_division_is_successful(dividend, divisor, dividend//divisor, dividend % divisor))
    divisor = 0
    print(test_zero_division_error_is_successful(dividend, divisor))

test_all_division()