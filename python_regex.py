import re
from typing import List, Tuple, Optional, Pattern


class DNARegex:
    """
    A safe, robust wrapper around Python's built-in regex engine
    specifically for DNA (A, C, G, T) sequence pattern matching.
    """

    # Pre-compiled safe patterns (no nested quantifiers)
    VALID_DNA = re.compile(r'^[ACGT]+$')
    CODON = re.compile(r'[ACGT]{3}')
    
    def __init__(self, pattern: str):
        """
        Compile the given pattern safely.
        """
        self.pattern_str = pattern
        try:
            self.regex: Pattern = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

    def search(self, sequence: str) -> Optional[re.Match]:
        """Return first match."""
        return self.regex.search(sequence)

    def find_all(self, sequence: str) -> List[str]:
        """Return all matches as list of strings."""
        return self.regex.findall(sequence)

    def find_iter(self, sequence: str):
        """Iterate through matches safely."""
        return self.regex.finditer(sequence)

    @staticmethod
    def is_valid_dna(seq: str) -> bool:
        """Check if a sequence contains only A,C,G,T."""
        return bool(DNARegex.VALID_DNA.fullmatch(seq))

    @staticmethod
    def extract_codons(seq: str) -> List[str]:
        """Extract codons in frame."""
        return DNARegex.CODON.findall(seq)

    @staticmethod
    def compile_safe(pattern: str) -> Pattern:
        """
        Compile patterns with safety checks to avoid catastrophic backtracking.
        This rejects nested quantifiers like (A+)+
        """
        forbidden = [
            r'\+\)', r'\*\)', r'\?\)',      # Quantifier before ')'
            r'\(\w*\+', r'\(\w*\*',        # Nested inside '('
            r'\(\w+\)\+', r'\(\w+\)\*',    # Group repeated
        ]

        for bad in forbidden:
            if re.search(bad, pattern):
                raise ValueError(
                    f"Unsafe regex (may cause backtracking): '{pattern}'"
                )
        
        return re.compile(pattern)


def regex_search(text: str, pattern: str) -> list:
    """
    Search for exact pattern matches in text using Python's regex engine.
    
    Parameters
    ----------
    text : str
        The text to search in.
    pattern : str
        The pattern to search for (will be escaped for literal matching).
    
    Returns
    -------
    list
        Starting indices of all matches.
    """
    # Escape pattern for literal matching
    escaped_pattern = re.escape(pattern)
    
    # Find all matches
    matches = []
    for match in re.finditer(escaped_pattern, text):
        matches.append(match.start())
    
    return matches


# -------------------------
# Example Usage
# -------------------------

if __name__ == "__main__":
    print("Python Regex Pattern Matching")
    print("=" * 50)


    
    
    # Simple pattern matching
    text = input("\nEnter text: ")
    pattern = input("Enter pattern to search: ")
    
    matches = regex_search(text, pattern)
    
    print(f"\nPattern '{pattern}' found at positions: {matches}")
    print(f"Total matches: {len(matches)}")


       