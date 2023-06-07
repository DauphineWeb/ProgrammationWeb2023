from palindrome import is_palindrome

def test_function(input, expected):
    result = is_palindrome(input)
    if result != expected:
        print(f"Error: is_palindrome('{input}') produced {result}, expected {expected}")

test_function('dad', True)
test_function('mom', True)
test_function('sos', True)
test_function('lol', True)
test_function('kayak', True)
test_function('loll', False)
test_function('bientôt', False)
