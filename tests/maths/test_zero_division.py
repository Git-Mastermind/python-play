from maths.division import divide

def test_zero_division_error_is_successful(dividend, divisor):
    try:
        divide(dividend, divisor)
    except ZeroDivisionError:
        return "✅ Success! Zero Division Error was raised!"

print(test_zero_division_error_is_successful(2, 0))


