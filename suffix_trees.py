class SuffixTreeNode:
    """
    A node in the suffix tree. 
    Each edge stores a substring (start, end) instead of single characters.
    """
    def __init__(self):
        self.children = {}       # dict: char -> (start, end, SuffixTreeNode)
        self.suffix_index = -1   # leaf nodes store starting position of suffix


class NaiveSuffixTree:
    """
    Naive suffix tree construction with edge compression.
    Edges represent substrings via (start, end) indices.

    Complexity:
        Construction: O(n^2) - still quadratic but more space efficient
        Space: O(n) - linear number of nodes (at most 2n)
    """

    def __init__(self, text: str):
        self.root = SuffixTreeNode()
        self.text = text
        self.build()

    def insert_suffix(self, suffix_start: int):
        """
        Inserts a suffix starting at position suffix_start.

        Parameters
        ----------
        suffix_start : int
            Starting position of the suffix in the text.
        """
        node = self.root
        i = suffix_start  # current position in text
        
        while i < len(self.text):
            ch = self.text[i]
            
            # If no edge starts with this character, create new leaf
            if ch not in node.children:
                # Create leaf node with edge containing rest of suffix
                leaf = SuffixTreeNode()
                leaf.suffix_index = suffix_start
                node.children[ch] = (i, len(self.text) - 1, leaf)
                return
            
            # Edge exists, need to traverse or split
            start, end, child = node.children[ch]
            edge_len = end - start + 1
            
            # Try to match along the edge
            j = 0
            while j < edge_len and i + j < len(self.text) and self.text[start + j] == self.text[i + j]:
                j += 1
            
            # Full edge matched, continue to child
            if j == edge_len:
                node = child
                i += edge_len
            else:
                # Partial match - need to split the edge
                # Create internal node at split point
                split_node = SuffixTreeNode()
                
                # Update existing edge to go to split node (shortened)
                node.children[ch] = (start, start + j - 1, split_node)
                
                # Add edge from split node to old child (remainder of old edge)
                old_char = self.text[start + j]
                split_node.children[old_char] = (start + j, end, child)
                
                # Add new leaf for current suffix
                new_char = self.text[i + j] if i + j < len(self.text) else None
                if new_char:
                    leaf = SuffixTreeNode()
                    leaf.suffix_index = suffix_start
                    split_node.children[new_char] = (i + j, len(self.text) - 1, leaf)
                else:
                    # Current suffix ends at split point
                    split_node.suffix_index = suffix_start
                return

    def build(self):
        """
        Build the suffix tree by inserting all suffixes.

        Algorithm:
        for i in [0 .. n-1]:
            insert suffix starting at position i

        Example:
            text = "banana$"
            Inserts suffixes at positions: 0,1,2,3,4,5,6
        """
        for i in range(len(self.text)):
            self.insert_suffix(i)

    def has_substring(self, pattern: str) -> bool:
        """
        Check if pattern exists in the text by traversing the suffix tree.

        Complexity: O(m) where m = pattern length
        """
        node = self.root
        i = 0  # position in pattern
        
        while i < len(pattern):
            ch = pattern[i]
            
            # No edge starting with this character
            if ch not in node.children:
                return False
            
            start, end, child = node.children[ch]
            edge_len = end - start + 1
            
            # Match characters along the edge
            j = 0
            while j < edge_len and i < len(pattern):
                if self.text[start + j] != pattern[i]:
                    return False
                i += 1
                j += 1
            
            # Move to child node if we consumed entire edge
            if j == edge_len:
                node = child
        
        return True


if __name__ == '__main__':
    print("Naive Suffix Tree")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    
    print("\nBuilding suffix tree...")
    tree = NaiveSuffixTree(text)
    
    found = tree.has_substring(pattern)
    
    if found:
        print(f"\nPattern '{pattern}' FOUND in text!")
    else:
        print(f"\nPattern '{pattern}' NOT FOUND in text.")
