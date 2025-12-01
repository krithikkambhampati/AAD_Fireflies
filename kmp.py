def compute_lps(pattern: str) -> list:
    """
    Constructs the LPS (Longest Proper Prefix which is also Suffix) array.

    LPS[i] = length of the longest prefix of 'pattern'
             which is also a suffix ending at index i.

    Parameters
    ----------
    pattern : str
        The pattern whose LPS table we are building.

    Returns
    -------
    list
        The LPS array of size len(pattern).
    """

    lps = [0] * len(pattern)
    length = 0   # length of current matching prefix
    i = 1        # lps[0] is always 0

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # fallback to previous longest prefix
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> list:
    """
    Performs KMP exact string matching on text.

    Parameters
    ----------
    text : str
        The text to search inside.
    pattern : str
        The pattern we want to find.

    Returns
    -------
    list
        List of starting indices where pattern occurs in text.

    Notes
    -----
    This implementation strictly follows the standard KMP method:
    - Pre-compute the LPS table.
    - Scan text only once.
    - No backtracking in text.
    """

    if pattern == "":
        return list(range(len(text) + 1))  # every position matches

    matches = []
    lps = compute_lps(pattern)

    i = 0   # index on text
    j = 0   # index on pattern

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                # Pattern found!
                matches.append(i - j)
                j = lps[j - 1]  # continue searching next possible match

        else:
            if j != 0:
                # fallback using LPS array
                j = lps[j - 1]
            else:
                i += 1  # move text pointer only

    return matches


if __name__ == '__main__':
    print("KMP Pattern Matching Algorithm")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    
    matches = kmp_search(text, pattern)
    
    print(f"\nPattern '{pattern}' found at positions: {matches}")
    print(f"Total matches: {len(matches)}")
