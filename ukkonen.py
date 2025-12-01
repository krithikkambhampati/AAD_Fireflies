class End:
    """
    Represents shared global end index for all leaves.
    It allows O(1) update when extending leaves.
    """
    def __init__(self, value=0):
        self.value = value


class Node:
    """
    Node of a suffix tree in Ukkonen's algorithm.

    suffix_link -> link to another internal node for fast jumps.
    children -> edges stored as character -> (start, End, Node)
    """
    def __init__(self):
        self.children = {}
        self.suffix_link = None


class SuffixTree:
    """
    Ukkonen's linear-time suffix tree implementation. Construction is O(n).

    The tree uses the original input string and stores edges as (start, end).
    """
    def __init__(self, text):
        self.text = text
        self.root = Node()

        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0

        self.remainder = 0       # number of pending suffixes
        self.last_created_node = None

        self.end = End(-1)       # global end

        self.build()

    # =========================================================================
    # Helper functions
    # =========================================================================

    def edge_length(self, start, end):
        return end.value - start + 1

    def walk_down(self, start, end, nxt):
        """Skip/Count trick."""
        if self.active_length >= self.edge_length(start, end):
            self.active_edge += self.edge_length(start, end)
            self.active_length -= self.edge_length(start, end)
            self.active_node = nxt
            return True
        return False

    # =========================================================================
    # Construction
    # =========================================================================

    def extend(self, pos):
        """
        Handles extension for single phase (i)
        Ukkonen extension rules are implemented here.
        """
        self.end.value += 1
        self.remainder += 1
        self.last_created_node = None

        while self.remainder > 0:

            if self.active_length == 0:
                self.active_edge = pos

            ch = self.text[self.active_edge]

            # CASE 1: no edge starting with active_edge
            if ch not in self.active_node.children:

                leaf = Node()
                self.active_node.children[ch] = (pos, self.end, leaf)

                # RULE 2 extension
                if self.last_created_node:
                    self.last_created_node.suffix_link = self.active_node
                    self.last_created_node = None

            else:
                start, end, nxt = self.active_node.children[ch]

                # Skip/Count trick
                if self.walk_down(start, end, nxt):
                    continue

                # CASE 2: edge already contains next character
                if self.text[start + self.active_length] == self.text[pos]:
                    self.active_length += 1

                    # RULE 3 (showstopper)
                    if self.last_created_node:
                        self.last_created_node.suffix_link = self.active_node
                        self.last_created_node = None
                    break

                # CASE 3: split edge and create internal + leaf
                split_end = End(start + self.active_length - 1)
                internal = Node()

                self.active_node.children[ch] = (start, split_end, internal)
                internal.children[self.text[pos]] = (pos, self.end, Node())
                nxt_start = start + self.active_length
                nxt_char = self.text[nxt_start]
                internal.children[nxt_char] = (nxt_start, end, nxt)

                # suffix links
                if self.last_created_node:
                    self.last_created_node.suffix_link = internal
                self.last_created_node = internal

            self.remainder -= 1

            # Active point update
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remainder + 1
            else:
                self.active_node = (
                    self.active_node.suffix_link
                    if self.active_node.suffix_link
                    else self.root
                )

    def build(self):
        """Main Ukkonen loop."""
        for i in range(len(self.text)):
            self.extend(i)

    def has_substring(self, pattern: str) -> bool:
        """
        Search for a pattern in the suffix tree.
        
        Parameters
        ----------
        pattern : str
            The pattern to search for.
        
        Returns
        -------
        bool
            True if pattern exists in the text, False otherwise.
        
        Complexity: O(m) where m is pattern length
        """
        if not pattern:
            return True
        
        node = self.root
        i = 0  # position in pattern
        
        while i < len(pattern):
            ch = pattern[i]
            
            # No edge starting with this character
            if ch not in node.children:
                return False
            
            start, end, child = node.children[ch]
            
            # Get actual end value
            edge_end = end.value if isinstance(end, End) else end
            edge_len = edge_end - start + 1
            
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
    print("Ukkonen's Suffix Tree Algorithm")
    print("=" * 50)
    
    text = input("Enter text: ")
    pattern = input("Enter pattern to search: ")
    
    print("\nBuilding suffix tree...")
    tree = SuffixTree(text)
    
    found = tree.has_substring(pattern)
    
    if found:
        print(f"\nPattern '{pattern}' FOUND in text!")
    else:
        print(f"\nPattern '{pattern}' NOT FOUND in text.")
