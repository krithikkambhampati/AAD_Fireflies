def build_bad_character_table(pattern: str) -> dict:
    """
    Preprocess the pattern for the Bad Character heuristic.

    For each character, store the LAST index it appears at in the pattern.

    Example:
        pattern = "ABAB"
        bad_char['A'] = 2
        bad_char['B'] = 3

    Complexity: O(m)
    """
    table = {}
    for i, ch in enumerate(pattern):
        table[ch] = i   # last occurrence index
    return table


def build_suffixes(pattern: str) -> list:
    """
    Build the suffix array needed for Good Suffix preprocessing.

    suffix[i] = length of longest suffix of pattern[i:]
    that is also a prefix of pattern.

    Complexity: O(m)
    """
    m = len(pattern)
    suffix = [0] * m
    suffix[m-1] = m

    g = m - 1
    f = 0

    for i in range(m-2, -1, -1):
        if i > g and suffix[i + m - 1 - f] < i - g:
            suffix[i] = suffix[i + m - 1 - f]
        else:
            g = min(g, i)
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1
            suffix[i] = f - g
    return suffix


def build_good_suffix_table(pattern: str) -> list:
    """
    Build Good Suffix table.

    shift[i] = how much to shift when mismatch occurs at position i.

    Complexity: O(m)
    """
    m = len(pattern)
    shift = [m] * m
    suffix = build_suffixes(pattern)

    # Case 1: suffix matches a suffix of pattern
    j = 0
    for i in range(m-1, -1, -1):
        if suffix[i] == i+1:
            while j < m-1-i:
                if shift[j] == m:
                    shift[j] = m-1-i
                j += 1

    # Case 2: substring inside pattern
    for i in range(m-1):
        shift[m-1-suffix[i]] = m-1-i
    return shift


def boyer_moore_search(text: str, pattern: str) -> list:
    """
    Full Boyer–Moore exact pattern matching algorithm.

    Uses BOTH:
        - Bad Character heuristic
        - Good Suffix heuristic

    Parameters
    ----------
    text : str
        The input text.
    pattern : str
        The pattern to search.

    Returns
    -------
    list
        All indices where pattern occurs in text.
    """

    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n+1))

    bad = build_bad_character_table(pattern)
    good = build_good_suffix_table(pattern)

    matches = []
    s = 0  # shift

    while s <= n - m:
        j = m - 1

        # compare from right to left
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            matches.append(s)
            s += good[0]  # full match shift
        else:
            # bad character shift
            bc_shift = j - bad.get(text[s + j], -1)
            # good suffix shift
            gs_shift = good[j]

            s += max(bc_shift, gs_shift)

    return matches


if __name__ == '__main__':
    print("Boyer-Moore Pattern Matching Algorithm")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    
    matches = boyer_moore_search(text, pattern)
    
    print(f"\nPattern '{pattern}' found at positions: {matches}")
    print(f"Total matches: {len(matches)}")
