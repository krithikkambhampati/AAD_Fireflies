def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Computes the Levenshtein edit distance between two strings.

    Allowed operations:
        - Insert  (cost 1)
        - Delete  (cost 1)
        - Substitute (cost 1)
    
    DP Relation (matches report):
        dp[i][j] = minimum edits to convert s1[0..i] → s2[0..j]

    Parameters
    ----------
    s1 : str
        First string.
    s2 : str
        Second string.

    Returns
    -------
    int
        Minimum edit distance.

    Complexity
    ----------
    Time:  O(len(s1) * len(s2))
    Space: O(len(s1) * len(s2))
    """

    n, m = len(s1), len(s2)

    # Initialize DP matrix
    dp = [[0]*(m+1) for _ in range(n+1)]

    # Base cases:
    # converting to/from empty string
    for i in range(n+1):
        dp[i][0] = i
    for j in range(m+1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, n+1):
        for j in range(1, m+1):

            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]   # no cost
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # deletion
                    dp[i][j-1],    # insertion
                    dp[i-1][j-1]   # substitution
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
        distance = levenshtein_distance(pattern, window)
        if distance <= k:
            matches.append(i)
    
    return matches


if __name__ == '__main__':
    print("Levenshtein Approximate Matching")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    k = int(input("Enter max edit distance (k): "))
    
    matches = find_approximate_matches(text, pattern, k)
    
    print(f"\nPattern '{pattern}' found (with ≤{k} edits) at positions: {matches}")
    print(f"Total matches: {len(matches)}")
