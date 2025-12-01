"""
Comprehensive benchmark for exact pattern matching algorithms.

Compares:
- KMP
- Boyer-Moore
- Horspool
- Ukkonen's Suffix Tree
- Python Regex (re module via dna_regex.py)

Fixed Parameters:
- Pattern length (P): 20 bases

Variable Parameter:
- Text size (T): 10K, 20K, 30K, 40K, 50K, 60K, 70K, 80K, 90K, 100K bases

Two graphs:
1. Time vs Text Size
2. Memory vs Text Size
"""

import os
import time
import re
import tracemalloc
import matplotlib.pyplot as plt

# Import exact matching algorithms
from kmp import kmp_search
from boyer_moore import boyer_moore_search
from horspool import horspool_search
from suffix_trees import NaiveSuffixTree
from ukkonen import SuffixTree
from python_regex import DNARegex


def load_ecoli_sequence(fasta_path='E-coli.fasta'):
    """Load E-coli genome sequence from FASTA file."""
    sequence = []
    with open(fasta_path, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequence.append(line.strip())
    return ''.join(sequence)


# =============================================================================
# REGEX WRAPPER
# =============================================================================

def regex_search(text, pattern):
    """Search using DNARegex wrapper."""
    # Escape pattern for exact matching
    escaped_pattern = re.escape(pattern)
    dna_regex = DNARegex(escaped_pattern)
    matches = [m.start() for m in dna_regex.find_iter(text)]
    return matches


# =============================================================================
# TIME BENCHMARKING
# =============================================================================

def benchmark_time_kmp(text, pattern):
    """Measure time for KMP."""
    start = time.time()
    matches = kmp_search(text, pattern)
    elapsed = time.time() - start
    return elapsed, len(matches)


def benchmark_time_boyer_moore(text, pattern):
    """Measure time for Boyer-Moore."""
    start = time.time()
    matches = boyer_moore_search(text, pattern)
    elapsed = time.time() - start
    return elapsed, len(matches)


def benchmark_time_horspool(text, pattern):
    """Measure time for Horspool."""
    start = time.time()
    matches = horspool_search(text, pattern)
    elapsed = time.time() - start
    return elapsed, len(matches)


def benchmark_time_suffix_tree(text, pattern):
    """Measure time for Naive Suffix Tree."""
    start = time.time()
    tree = NaiveSuffixTree(text)
    result = tree.has_substring(pattern)
    elapsed = time.time() - start
    return elapsed, 1 if result else 0


def benchmark_time_ukkonen(text, pattern):
    """Measure time for Ukkonen's Suffix Tree."""
    start = time.time()
    tree = SuffixTree(text)
    result = tree.has_substring(pattern)
    elapsed = time.time() - start
    return elapsed, 1 if result else 0


def benchmark_time_regex(text, pattern):
    """Measure time for Python Regex."""
    start = time.time()
    matches = regex_search(text, pattern)
    elapsed = time.time() - start
    return elapsed, len(matches)


def run_time_benchmarks(full_sequence, pattern, text_sizes):
    """Run time benchmarks for all text sizes."""
    results = {
        'KMP': {},
        'Boyer-Moore': {},
        'Horspool': {},
        'Suffix Tree': {},
        'Ukkonen': {},
        'Python Regex': {}
    }
    
    print("\n" + "="*60)
    print("TIME BENCHMARK - EXACT MATCHING ALGORITHMS")
    print("="*60)
    print(f"Pattern length (P): {len(pattern)} bases")
    print(f"Pattern: {pattern}")
    print(f"Text sizes: {text_sizes}")
    print("="*60)
    
    for text_size in text_sizes:
        text = full_sequence[:text_size]
        print(f"\nText size: {text_size:,} bases")
        
        # KMP
        print(f"  [1/6] Running KMP...")
        try:
            elapsed, num_matches = benchmark_time_kmp(text, pattern)
            results['KMP'][text_size] = elapsed
            print(f"        Time: {elapsed:.6f}s, Matches: {num_matches}")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['KMP'][text_size] = None
        
        # Boyer-Moore
        print(f"  [2/6] Running Boyer-Moore...")
        try:
            elapsed, num_matches = benchmark_time_boyer_moore(text, pattern)
            results['Boyer-Moore'][text_size] = elapsed
            print(f"        Time: {elapsed:.6f}s, Matches: {num_matches}")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Boyer-Moore'][text_size] = None
        
        # Horspool
        print(f"  [3/6] Running Horspool...")
        try:
            elapsed, num_matches = benchmark_time_horspool(text, pattern)
            results['Horspool'][text_size] = elapsed
            print(f"        Time: {elapsed:.6f}s, Matches: {num_matches}")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Horspool'][text_size] = None
        
        # Suffix Tree
        print(f"  [4/6] Running Suffix Tree...")
        try:
            elapsed, num_matches = benchmark_time_suffix_tree(text, pattern)
            results['Suffix Tree'][text_size] = elapsed
            print(f"        Time: {elapsed:.6f}s")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Suffix Tree'][text_size] = None
        
        # Ukkonen
        print(f"  [5/6] Running Ukkonen...")
        try:
            elapsed, num_matches = benchmark_time_ukkonen(text, pattern)
            results['Ukkonen'][text_size] = elapsed
            print(f"        Time: {elapsed:.6f}s")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Ukkonen'][text_size] = None
        
        # Python Regex
        print(f"  [6/6] Running Python Regex...")
        try:
            elapsed, num_matches = benchmark_time_regex(text, pattern)
            results['Python Regex'][text_size] = elapsed
            print(f"        Time: {elapsed:.6f}s, Matches: {num_matches}")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Python Regex'][text_size] = None
    
    return results


# =============================================================================
# MEMORY BENCHMARKING
# =============================================================================

def benchmark_memory_kmp(text, pattern):
    """Measure memory for KMP."""
    tracemalloc.start()
    matches = kmp_search(text, pattern)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def benchmark_memory_boyer_moore(text, pattern):
    """Measure memory for Boyer-Moore."""
    tracemalloc.start()
    matches = boyer_moore_search(text, pattern)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def benchmark_memory_horspool(text, pattern):
    """Measure memory for Horspool."""
    tracemalloc.start()
    matches = horspool_search(text, pattern)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def benchmark_memory_suffix_tree(text, pattern):
    """Measure memory for Naive Suffix Tree."""
    tracemalloc.start()
    tree = NaiveSuffixTree(text)
    result = tree.has_substring(pattern)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def benchmark_memory_ukkonen(text, pattern):
    """Measure memory for Ukkonen."""
    tracemalloc.start()
    tree = SuffixTree(text)
    result = tree.has_substring(pattern)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def benchmark_memory_regex(text, pattern):
    """Measure memory for Python Regex."""
    tracemalloc.start()
    matches = regex_search(text, pattern)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def run_memory_benchmarks(full_sequence, pattern, text_sizes):
    """Run memory benchmarks for all text sizes."""
    results = {
        'KMP': {},
        'Boyer-Moore': {},
        'Horspool': {},
        'Suffix Tree': {},
        'Ukkonen': {},
        'Python Regex': {}
    }
    
    print("\n" + "="*60)
    print("MEMORY BENCHMARK - EXACT MATCHING ALGORITHMS")
    print("="*60)
    print(f"Pattern length (P): {len(pattern)} bases")
    print(f"Text sizes: {text_sizes}")
    print("="*60)
    
    for text_size in text_sizes:
        text = full_sequence[:text_size]
        print(f"\nText size: {text_size:,} bases")
        
        # KMP
        print(f"  [1/6] Measuring KMP memory...")
        try:
            mem = benchmark_memory_kmp(text, pattern)
            results['KMP'][text_size] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['KMP'][text_size] = None
        
        # Boyer-Moore
        print(f"  [2/6] Measuring Boyer-Moore memory...")
        try:
            mem = benchmark_memory_boyer_moore(text, pattern)
            results['Boyer-Moore'][text_size] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Boyer-Moore'][text_size] = None
        
        # Horspool
        print(f"  [3/6] Measuring Horspool memory...")
        try:
            mem = benchmark_memory_horspool(text, pattern)
            results['Horspool'][text_size] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Horspool'][text_size] = None
        
        # Suffix Tree
        print(f"  [4/6] Measuring Suffix Tree memory...")
        try:
            mem = benchmark_memory_suffix_tree(text, pattern)
            results['Suffix Tree'][text_size] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Suffix Tree'][text_size] = None
        
        # Ukkonen
        print(f"  [5/6] Measuring Ukkonen memory...")
        try:
            mem = benchmark_memory_ukkonen(text, pattern)
            results['Ukkonen'][text_size] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Ukkonen'][text_size] = None
        
        # Python Regex
        print(f"  [6/6] Measuring Python Regex memory...")
        try:
            mem = benchmark_memory_regex(text, pattern)
            results['Python Regex'][text_size] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Python Regex'][text_size] = None
    
    return results


# =============================================================================
# PLOTTING
# =============================================================================

def plot_results(time_results, memory_results):
    """Create plots with separate memory graphs for better visibility."""
    
    # =========================================================================
    # FIGURE 1: TIME COMPARISON (split if needed)
    # =========================================================================
    fig1, axes1 = plt.subplots(1, 2, figsize=(16, 7))
    
    # Separate tree-based from pattern matching algorithms for time
    pattern_matching_algos = ['KMP', 'Boyer-Moore', 'Horspool', 'Python Regex']
    tree_algos = ['Suffix Tree', 'Ukkonen']
    
    # Plot 1a: Pattern matching algorithms time
    for algo_name in pattern_matching_algos:
        if algo_name in time_results:
            measurements = time_results[algo_name]
            text_sizes = sorted([k for k in measurements.keys() if measurements[k] is not None])
            times = [measurements[k] for k in text_sizes]
            text_sizes_kb = [size / 1000 for size in text_sizes]
            
            axes1[0].plot(text_sizes_kb, times, marker='o', label=algo_name, linewidth=2, markersize=6)
    
    axes1[0].set_xlabel('Text Size (KB)', fontsize=12)
    axes1[0].set_ylabel('Time (seconds)', fontsize=12)
    axes1[0].set_title('Time: Pattern Matching Algorithms\n(P=20 bases)', fontsize=13, fontweight='bold')
    axes1[0].legend(fontsize=9, loc='best')
    axes1[0].grid(True, alpha=0.3)
    
    # Plot 1b: Tree-based algorithms time (separate scale)
    for algo_name in tree_algos:
        if algo_name in time_results:
            measurements = time_results[algo_name]
            text_sizes = sorted([k for k in measurements.keys() if measurements[k] is not None])
            times = [measurements[k] for k in text_sizes]
            text_sizes_kb = [size / 1000 for size in text_sizes]
            
            axes1[1].plot(text_sizes_kb, times, marker='o', label=algo_name, linewidth=2, markersize=6)
    
    axes1[1].set_xlabel('Text Size (KB)', fontsize=12)
    axes1[1].set_ylabel('Time (seconds)', fontsize=12)
    axes1[1].set_title('Time: Tree-Based Algorithms\n(P=20 bases)', fontsize=13, fontweight='bold')
    axes1[1].legend(fontsize=9, loc='best')
    axes1[1].grid(True, alpha=0.3)
    
    plt.suptitle('Time Comparison - Exact Matching Algorithms', fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('exact_matching_time_benchmark.png', dpi=300, bbox_inches='tight')
    print(f"\nTime plot saved to exact_matching_time_benchmark.png")
    plt.show()
    
    # =========================================================================
    # FIGURE 2: MEMORY COMPARISON (split for visibility)
    # =========================================================================
    fig2, axes2 = plt.subplots(1, 2, figsize=(16, 7))
    
    # Plot 2a: Pattern matching algorithms memory
    for algo_name in pattern_matching_algos:
        if algo_name in memory_results:
            measurements = memory_results[algo_name]
            text_sizes = sorted([k for k in measurements.keys() if measurements[k] is not None])
            memory = [measurements[k] for k in text_sizes]
            text_sizes_kb = [size / 1000 for size in text_sizes]
            
            axes2[0].plot(text_sizes_kb, memory, marker='o', label=algo_name, linewidth=2, markersize=6)
    
    axes2[0].set_xlabel('Text Size (KB)', fontsize=12)
    axes2[0].set_ylabel('Peak Memory (bytes)', fontsize=12)
    axes2[0].set_title('Memory: Pattern Matching Algorithms\n(P=20 bases)', fontsize=13, fontweight='bold')
    axes2[0].legend(fontsize=9, loc='best')
    axes2[0].grid(True, alpha=0.3)
    axes2[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    # Plot 2b: Tree-based algorithms memory (separate scale)
    for algo_name in tree_algos:
        if algo_name in memory_results:
            measurements = memory_results[algo_name]
            text_sizes = sorted([k for k in measurements.keys() if measurements[k] is not None])
            memory = [measurements[k] for k in text_sizes]
            text_sizes_kb = [size / 1000 for size in text_sizes]
            
            axes2[1].plot(text_sizes_kb, memory, marker='o', label=algo_name, linewidth=2, markersize=6)
    
    axes2[1].set_xlabel('Text Size (KB)', fontsize=12)
    axes2[1].set_ylabel('Peak Memory (bytes)', fontsize=12)
    axes2[1].set_title('Memory: Tree-Based Algorithms\n(P=20 bases)', fontsize=13, fontweight='bold')
    axes2[1].legend(fontsize=9, loc='best')
    axes2[1].grid(True, alpha=0.3)
    axes2[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    plt.suptitle('Memory Comparison - Exact Matching Algorithms', fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('exact_matching_memory_benchmark.png', dpi=300, bbox_inches='tight')
    print(f"\nMemory plot saved to exact_matching_memory_benchmark.png")
    plt.show()


def main():
    """Main execution."""
    print("="*60)
    print("COMPLETE EXACT MATCHING BENCHMARK")
    print("="*60)
    
    # Load E-coli sequence
    print("\nLoading E-coli genome...")
    ecoli_path = 'E-coli.fasta'
    if not os.path.exists(ecoli_path):
        print(f"ERROR: {ecoli_path} not found!")
        return
    
    full_sequence = load_ecoli_sequence(ecoli_path)
    print(f"Loaded sequence of length: {len(full_sequence):,} bases")
    
    # Fixed parameters
    PATTERN_LENGTH = 20  # P = 20 bases
    pattern = full_sequence[1000:1000+PATTERN_LENGTH]
    
    # Variable parameter
    text_sizes = list(range(20000, 520000, 20000))  # 20K, 40K, 60K, ..., 500K
    
    print(f"\nFIXED PARAMETER:")
    print(f"  Pattern length (P): {PATTERN_LENGTH} bases")
    print(f"  Pattern: {pattern}")
    
    print(f"\nVARIABLE PARAMETER:")
    print(f"  Text size (T): {text_sizes[0]:,} to {text_sizes[-1]:,} bases ({len(text_sizes)} steps)")
    
    # Run benchmarks
    time_results = run_time_benchmarks(full_sequence, pattern, text_sizes)
    memory_results = run_memory_benchmarks(full_sequence, pattern, text_sizes)
    
    # Plot results
    print("\nGenerating plots...")
    plot_results(time_results, memory_results)
    
    print("\nBenchmark complete!")


if __name__ == '__main__':
    main()
