def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Computes Damerau–Levenshtein edit distance between two strings.

    Allowed operations (all cost = 1):
        - Insert
        - Delete
        - Substitute
        - Transpose adjacent characters

    DP Relation:

        dp[i][j] = minimum edits to convert s1[0..i] -> s2[0..j]

    Additionally:
        If s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]:
            dp[i][j] = min(dp[i][j], dp[i-2][j-2] + 1)

    Parameters
    ----------
    s1 : str
        First string
    s2 : str
        Second string

    Returns
    -------
    int
        Minimum edit distance

    Complexity
    ----------
    Time:  O(len(s1) * len(s2))
    Space: O(len(s1) * len(s2))
    """

    n, m = len(s1), len(s2)
    dp = [[0]*(m+1) for _ in range(n+1)]

    # base cases
    for i in range(n+1):
        dp[i][0] = i
    for j in range(m+1):
        dp[0][j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):

            cost = 0 if s1[i-1] == s2[j-1] else 1

            # substitution / insertion / deletion
            dp[i][j] = min(
                dp[i-1][j] + 1,      # deletion
                dp[i][j-1] + 1,      # insertion
                dp[i-1][j-1] + cost  # substitution / match
            )

            # transposition
            if i > 1 and j > 1 \
               and s1[i-1] == s2[j-2] \
               and s1[i-2] == s2[j-1]:
                dp[i][j] = min(
                    dp[i][j],
                    dp[i-2][j-2] + 1
                )

    return dp[n][m]


def find_approximate_matches(text: str, pattern: str, k: int) -> list:
    """
    Find all positions where pattern matches text with at most k edits.
    
    Parameters
    ----------
    text : str
        The text to search in.
    pattern : str
        The pattern to search for.
    k : int
        Maximum allowed edit distance.
    
    Returns
    -------
    list
        Starting indices where pattern matches with ≤k edits.
    """
    matches = []
    m = len(pattern)
    n = len(text)
    
    for i in range(n - m + 1):
        window = text[i:i+m]
        distance = damerau_levenshtein_distance(pattern, window)
        if distance <= k:
            matches.append(i)
    
    return matches


if __name__ == '__main__':
    print("Damerau-Levenshtein Approximate Matching")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    k = int(input("Enter max edit distance (k): "))
    
    matches = find_approximate_matches(text, pattern, k)
    
    print(f"\nPattern '{pattern}' found (with ≤{k} edits) at positions: {matches}")
    print(f"Total matches: {len(matches)}")
