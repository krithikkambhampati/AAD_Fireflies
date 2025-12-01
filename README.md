# AAD_Fireflies - Pattern Matching Algorithms

A comprehensive collection of exact and approximate pattern matching algorithms implemented in Python, with benchmarking tools for performance analysis on DNA sequences.

## 📋 Table of Contents
- [Overview](#overview)
- [Algorithms Implemented](#algorithms-implemented)
- [Requirements](#requirements)
- [File Descriptions](#file-descriptions)
- [How to Run](#how-to-run)
  - [Individual Algorithms](#individual-algorithms)
  - [Benchmark Scripts](#benchmark-scripts)
- [Input/Output Format](#inputoutput-format)
- [Results](#results)

---

## 🔍 Overview

This project implements and benchmarks various pattern matching algorithms for DNA sequence analysis. It includes both exact matching algorithms (finding exact occurrences) and approximate matching algorithms (allowing insertions, deletions, and substitutions).

**Dataset**: E. coli genome sequence (~4.6 million base pairs)

---

## 🧬 Algorithms Implemented

### Exact Matching Algorithms
1. **KMP (Knuth-Morris-Pratt)** - O(n+m) time, uses LPS array
2. **Boyer-Moore** - O(n) average, uses bad character and good suffix heuristics
3. **Horspool** - Simplified Boyer-Moore, excellent average performance
4. **Naive Suffix Tree** - O(n²) construction, O(m) search with edge compression
5. **Ukkonen's Suffix Tree** - O(n) construction and space, O(m) search
6. **Python Regex** - Built-in regex engine wrapper

### Approximate Matching Algorithms
1. **Levenshtein Distance** - Edit distance with insertion, deletion, substitution
2. **Damerau-Levenshtein Distance** - Includes transposition of adjacent characters
3. **Shift-Or** - Bit-parallel approximate matching

---

## 📦 Requirements

```bash
python3
matplotlib
```

Install dependencies:
```bash
pip install matplotlib
```

---

## 📁 File Descriptions

### Algorithm Files
| File | Description | Complexity |
|------|-------------|------------|
| `kmp.py` | KMP exact matching | Time: O(n+m), Space: O(m) |
| `boyer_moore.py` | Boyer-Moore exact matching | Time: O(n) avg, Space: O(m) |
| `horspool.py` | Horspool exact matching | Time: O(n) avg, Space: O(m) |
| `suffix_trees.py` | Naive suffix tree | Time: O(n²), Space: O(n) |
| `ukkonen.py` | Ukkonen's suffix tree | Time: O(n), Space: O(n) |
| `python_regex.py` | Python regex wrapper | Native regex engine |
| `Levenshtein.py` | Levenshtein distance | Time: O(nm), Space: O(nm) |
| `Damerau–Levenshtein.py` | Damerau-Levenshtein distance | Time: O(nm), Space: O(nm) |
| `shift_or.py` | Shift-Or approximate matching | Time: O(n), Space: O(Σ) |

### Benchmark Files
| File | Description |
|------|-------------|
| `benchmark_exact_complete.py` | Complete benchmark for exact matching algorithms |
| `benchmark_fuzzy_matching.py` | Benchmark for approximate matching algorithms |

### Data Files
| File | Description |
|------|-------------|
| `E-coli.fasta` | E. coli genome sequence (4,641,652 base pairs) |

---

## 🚀 How to Run

### Individual Algorithms

#### Exact Matching Algorithms

**KMP Algorithm**
```bash
python3 kmp.py
```
- **Input**: 
  - Text (string to search in)
  - Pattern (string to find)
- **Output**: List of starting indices where pattern is found

**Example:**
```
Enter text: ACGTACGT
Enter pattern to search: ACG
Pattern 'ACG' found at positions: [0, 4]
Total matches: 2
```

---

**Boyer-Moore Algorithm**
```bash
python3 boyer_moore.py
```
- **Input**: Text, Pattern
- **Output**: List of starting indices

---

**Horspool Algorithm**
```bash
python3 horspool.py
```
- **Input**: Text, Pattern
- **Output**: List of starting indices

---

**Naive Suffix Tree**
```bash
python3 suffix_trees.py
```
- **Input**: Text, Pattern
- **Output**: "Pattern FOUND in text!" or "Pattern NOT FOUND in text."

**Example:**
```
Enter text: banana
Enter pattern to search: ana
Building suffix tree...
Pattern 'ana' FOUND in text!
```

---

**Ukkonen's Suffix Tree**
```bash
python3 ukkonen.py
```
- **Input**: Text, Pattern
- **Output**: "Pattern FOUND in text!" or "Pattern NOT FOUND in text."

---

**Python Regex**
```bash
python3 python_regex.py
```
- **Input**: 
  - Choice (1 for pattern matching, 2 for DNA utilities)
  - For choice 1: Text, Pattern
  - For choice 2: DNA sequence (for ORF finding, codon extraction, motif search)
- **Output**: 
  - Choice 1: List of starting indices
  - Choice 2: ORFs, codons, motifs found

---

#### Approximate Matching Algorithms

**Levenshtein Distance**
```bash
python3 Levenshtein.py
```
- **Input**: 
  - Text (string to search in)
  - Pattern (string to find approximately)
  - Max edit distance k (integer)
- **Output**: List of positions where pattern matches with ≤k edits

**Example:**
```
Enter text: ACGTACGT
Enter pattern to search: ACGT
Enter max edit distance (k): 1
Pattern 'ACGT' found (with ≤1 edits) at positions: [0, 4]
Total matches: 2
```

---

**Damerau-Levenshtein Distance**
```bash
python3 Damerau–Levenshtein.py
```
- **Input**: Text, Pattern, Max edit distance k
- **Output**: List of positions where pattern matches with ≤k edits (includes transpositions)

---

**Shift-Or Algorithm**
```bash
python3 shift_or.py
```
- **Input**: Text, Pattern, Max edit distance k
- **Output**: List of positions where pattern matches with ≤k edits

---

### Benchmark Scripts

#### Complete Exact Matching Benchmark

```bash
python3 benchmark_exact_complete.py
```

**What it does:**
- Compares KMP, Boyer-Moore, Horspool, Suffix Tree, Ukkonen, Python Regex
- Tests on increasing text sizes (20K to 500K bases in 20K increments)
- Fixed pattern length: 20 bases
- Measures both time and memory

**Output:**
- Terminal output with detailed statistics
- Two PNG files:
  - `exact_matching_time_benchmark.png` - Time comparison plots
  - `exact_matching_memory_benchmark.png` - Memory comparison plots

**Runtime:** ~5-10 minutes (depending on system)

---

#### Fuzzy Matching Benchmark

```bash
python3 benchmark_fuzzy_matching.py
```

**What it does:**
- Compares Levenshtein, Damerau-Levenshtein, Shift-Or
- Tests with increasing edit distances (k = 0 to 5)
- Fixed text size: 100K bases
- Fixed pattern length: 20 bases
- Measures both time and memory

**Output:**
- Terminal output with detailed statistics
- `fuzzy_matching_benchmark.png` - Combined time and memory plots

**Runtime:** ~3-5 minutes

---

## 📊 Input/Output Format

### Algorithm Functions (for programmatic use)

```python
# Exact matching algorithms return list of indices
from kmp import kmp_search
matches = kmp_search(text="ACGTACGT", pattern="ACG")
# Returns: [0, 4]

# Suffix trees return boolean
from ukkonen import SuffixTree
tree = SuffixTree("ACGTACGT")
found = tree.has_substring("ACG")
# Returns: True

# Approximate matching returns list of indices within k edits
from shift_or import shift_or_approx
matches = shift_or_approx(text="ACGTACGT", pattern="ACGT", k=1)
# Returns: [0, 4]
```

---

## 📈 Results

### Expected Performance Characteristics

**Time Complexity:**
- Pattern matching (KMP, Boyer-Moore, Horspool): O(n) linear with text size
- Suffix trees: O(n) construction dominates for small patterns
- Ukkonen faster than Naive Suffix Tree due to O(n) vs O(n²) construction

**Space Complexity:**
- Pattern matching: O(m) - minimal memory
- Suffix trees: O(n) - grows linearly with text size
- Naive Suffix Tree uses more memory than Ukkonen due to less efficient compression

**Approximate Matching:**
- Time increases with edit distance k
- Damerau-Levenshtein slightly slower than Levenshtein due to transposition checks

---

