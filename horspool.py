def build_shift_table(pattern: str) -> dict:
    """
    Builds the shift table used by Horspool's algorithm.

    For each character, store how much we should shift the pattern
    when a mismatch occurs at the last character.

    Strategy:
        If a mismatch occurs at j, we shift pattern by:
            shift[text[i+j]] = length - j - 1

    Last character is special: default shift = pattern length.

    Returns
    -------
    dict(char → int)
        Bad character shift values.
    """
    m = len(pattern)
    table = {ch: m for ch in set(pattern)}  # default shift = m

    # Fill all but last character
    for i in range(m - 1):
        table[pattern[i]] = m - 1 - i

    return table


def horspool_search(text: str, pattern: str) -> list:
    """
    Horspool string matching algorithm.

    Parameters
    ----------
    text : str
        Text to search in.
    pattern : str
        Pattern to search for.

    Returns
    -------
    list
        Starting indices of all matches of pattern in text.

    Notes
    -----
    - Aligns pattern at position i, compares from rightmost char.
    - On mismatch, shifts pattern using the shift table based
      on mismatched text character.
    - Worst-case O(n*m), but excellent average performance.
    """
    n, m = len(text), len(pattern)

    if m == 0:
        return list(range(n + 1))

    shift = build_shift_table(pattern)
    matches = []

    i = 0  # alignment index in text

    while i <= n - m:
        # compare pattern backwards
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            matches.append(i)
            i += m  # full match shift
        else:
            # get text character causing mismatch
            char = text[i + m - 1]
            i += shift.get(char, m)  # default m if char not in table

    return matches


if __name__ == '__main__':
    print("Horspool Pattern Matching Algorithm")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    
    matches = horspool_search(text, pattern)
    
    print(f"\nPattern '{pattern}' found at positions: {matches}")
    print(f"Total matches: {len(matches)}")
