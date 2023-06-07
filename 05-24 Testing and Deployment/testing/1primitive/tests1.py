from palindrome import is_palindrome

total = 0
succeeded = 0

def test_palindrome(input, expected):
    global total, succeeded
    total += 1
    result = is_palindrome(input)
    if result == expected:
        succeeded += 1
    else:
        print(f"Error in is_palindrome({input}): expected {expected}, got {result}")

test_palindrome('tôt', True)
test_palindrome('', True)
test_palindrome('bientôt', False)
test_palindrome('Level', True)
test_palindrome('racecar', True)
test_palindrome('my gym', True)
test_palindrome('forward', False)
test_palindrome('Anna', True)

print(f"{succeeded} of {total} tests succeeded {'🎉' if succeeded == total else '🚩'}")
