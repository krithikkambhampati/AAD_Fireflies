def shift_or_approx(text: str, pattern: str, k: int):
    """
    Bit-parallel approximate matching using Shift-Or algorithm.

    Finds all positions where pattern matches text
    with at most k edit operations.

    Allowed edits:
        - Insertion
        - Deletion
        - Substitution

    Uses bit masks and bit-parallel DP.

    Time:  O(n*k)
    Space: O(|Σ|*k)

    Returns
    -------
    list of indices where edit distance <= k
    """

    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n+1))
    
    if m > 31:
        raise ValueError("Pattern too long for bit-parallel algorithm (max 31 characters)")

    # Build bit masks for each character
    char_masks = {}
    for c in set(text + pattern):
        mask = 0
        for i in range(m):
            if i < len(pattern) and pattern[i] == c:
                mask |= (1 << i)
        char_masks[c] = mask

    # Initialize state vectors for each error level
    # R[j] represents matches with at most j errors
    R = [0] * (k + 1)
    R[0] = 1  # exact match state initialized
    
    matches = []
    
    for i, ch in enumerate(text):
        # Get character mask
        ch_mask = char_masks.get(ch, 0)
        
        # Update from highest error level to lowest
        old_R = list(R)
        
        for j in range(k, -1, -1):
            # Shift (exact match continuation)
            shifted = (old_R[j] << 1) & ch_mask
            
            # Add insertions, deletions, substitutions from lower error level
            if j > 0:
                # Insertion: don't consume pattern character
                insertion = old_R[j-1]
                # Deletion: consume pattern character but not text character  
                deletion = (old_R[j-1] << 1)
                # Substitution: consume both but they don't match
                substitution = (old_R[j-1] << 1)
                
                R[j] = shifted | insertion | deletion | substitution
            else:
                R[j] = shifted
            
            # Always start fresh matches
            R[j] |= 1
        
        # Check if pattern fully matched at this position
        if R[k] & (1 << (m)):
            matches.append(i - m + 1)
    
    return matches


if __name__ == '__main__':
    print("Shift-Or Approximate Matching Algorithm")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    k = int(input("Enter max edit distance (k): "))
    
    matches = shift_or_approx(text, pattern, k)
    
    print(f"\nPattern '{pattern}' found (with ≤{k} edits) at positions: {matches}")
    print(f"Total matches: {len(matches)}")
