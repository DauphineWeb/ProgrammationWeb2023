
def is_palindrome(word):
    """
    Checks if a given word is a palindrome or not.
    """
    word = word.replace(' ', '').lower()
    return word[::-1] == word
