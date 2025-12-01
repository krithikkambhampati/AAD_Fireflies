"""
Benchmark script for fuzzy/approximate pattern matching algorithms.

Compares:
- Levenshtein Distance
- Damerau-Levenshtein Distance  
- Shift-Or (approximate matching)

Fixed Parameters:
- Text size (T): 1,000,000 bases from E-coli genome
- Pattern length (P): 20 bases

Variable Parameter:
- Edit distance (k): 0, 1, 2, 3, 4, 5

Two graphs:
1. Time vs Edit Distance
2. Memory vs Edit Distance
"""

import os
import time
import tracemalloc
import matplotlib.pyplot as plt

# Import fuzzy matching algorithms
from Levenshtein import levenshtein_distance
from shift_or import shift_or_approx

# Import Damerau-Levenshtein (handle special filename)
import importlib.util
spec = importlib.util.spec_from_file_location("damerau", "Damerau–Levenshtein.py")
damerau_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(damerau_module)
damerau_levenshtein_distance = damerau_module.damerau_levenshtein_distance


def load_ecoli_sequence(fasta_path='E-coli.fasta'):
    """Load E-coli genome sequence from FASTA file."""
    sequence = []
    with open(fasta_path, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequence.append(line.strip())
    return ''.join(sequence)


def find_approximate_match_levenshtein(text, pattern, k):
    """
    Find all positions in text where pattern matches with at most k edits.
    Uses sliding window with Levenshtein distance.
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


def find_approximate_match_damerau(text, pattern, k):
    """
    Find all positions in text where pattern matches with at most k edits.
    Uses sliding window with Damerau-Levenshtein distance.
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


# =============================================================================
# TIME BENCHMARKING
# =============================================================================

def benchmark_time_levenshtein(text, pattern, k):
    """Measure time for Levenshtein-based approximate matching."""
    start = time.time()
    matches = find_approximate_match_levenshtein(text, pattern, k)
    elapsed = time.time() - start
    return elapsed, len(matches)


def benchmark_time_damerau(text, pattern, k):
    """Measure time for Damerau-Levenshtein-based approximate matching."""
    start = time.time()
    matches = find_approximate_match_damerau(text, pattern, k)
    elapsed = time.time() - start
    return elapsed, len(matches)


def benchmark_time_shift_or(text, pattern, k):
    """Measure time for Shift-Or approximate matching."""
    start = time.time()
    matches = shift_or_approx(text, pattern, k)
    elapsed = time.time() - start
    return elapsed, len(matches)


def run_time_benchmarks(text, pattern, k_values):
    """Run time benchmarks for all edit distances."""
    results = {
        'Levenshtein': {},
        'Damerau-Levenshtein': {},
        'Shift-Or': {}
    }
    
    print("\n" + "="*60)
    print("TIME BENCHMARK - FUZZY MATCHING ALGORITHMS")
    print("="*60)
    print(f"Text size (T): {len(text):,} bases")
    print(f"Pattern length (P): {len(pattern)} bases")
    print(f"Pattern: {pattern}")
    print(f"Edit distances (k): {k_values}")
    print("="*60)
    
    for k in k_values:
        print(f"\nEdit distance k = {k}:")
        
        # Levenshtein
        print(f"  [1/3] Running Levenshtein...")
        try:
            elapsed, num_matches = benchmark_time_levenshtein(text, pattern, k)
            results['Levenshtein'][k] = elapsed
            print(f"        Time: {elapsed:.4f}s, Matches: {num_matches}")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Levenshtein'][k] = None
        
        # Damerau-Levenshtein
        print(f"  [2/3] Running Damerau-Levenshtein...")
        try:
            elapsed, num_matches = benchmark_time_damerau(text, pattern, k)
            results['Damerau-Levenshtein'][k] = elapsed
            print(f"        Time: {elapsed:.4f}s, Matches: {num_matches}")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Damerau-Levenshtein'][k] = None
        
        # Shift-Or
        print(f"  [3/3] Running Shift-Or...")
        try:
            elapsed, num_matches = benchmark_time_shift_or(text, pattern, k)
            results['Shift-Or'][k] = elapsed
            print(f"        Time: {elapsed:.4f}s, Matches: {num_matches}")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Shift-Or'][k] = None
    
    return results


# =============================================================================
# MEMORY BENCHMARKING
# =============================================================================

def benchmark_memory_levenshtein(text, pattern, k):
    """Measure memory for Levenshtein-based approximate matching."""
    tracemalloc.start()
    matches = find_approximate_match_levenshtein(text, pattern, k)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def benchmark_memory_damerau(text, pattern, k):
    """Measure memory for Damerau-Levenshtein-based approximate matching."""
    tracemalloc.start()
    matches = find_approximate_match_damerau(text, pattern, k)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def benchmark_memory_shift_or(text, pattern, k):
    """Measure memory for Shift-Or approximate matching."""
    tracemalloc.start()
    matches = shift_or_approx(text, pattern, k)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def run_memory_benchmarks(text, pattern, k_values):
    """Run memory benchmarks for all edit distances."""
    results = {
        'Levenshtein': {},
        'Damerau-Levenshtein': {},
        'Shift-Or': {}
    }
    
    print("\n" + "="*60)
    print("MEMORY BENCHMARK - FUZZY MATCHING ALGORITHMS")
    print("="*60)
    print(f"Text size (T): {len(text):,} bases")
    print(f"Pattern length (P): {len(pattern)} bases")
    print(f"Edit distances (k): {k_values}")
    print("="*60)
    
    for k in k_values:
        print(f"\nEdit distance k = {k}:")
        
        # Levenshtein
        print(f"  [1/3] Measuring Levenshtein memory...")
        try:
            mem = benchmark_memory_levenshtein(text, pattern, k)
            results['Levenshtein'][k] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Levenshtein'][k] = None
        
        # Damerau-Levenshtein
        print(f"  [2/3] Measuring Damerau-Levenshtein memory...")
        try:
            mem = benchmark_memory_damerau(text, pattern, k)
            results['Damerau-Levenshtein'][k] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Damerau-Levenshtein'][k] = None
        
        # Shift-Or
        print(f"  [3/3] Measuring Shift-Or memory...")
        try:
            mem = benchmark_memory_shift_or(text, pattern, k)
            results['Shift-Or'][k] = mem
            print(f"        Memory: {mem:,} bytes ({mem/(1024*1024):.2f} MB)")
        except Exception as e:
            print(f"        ERROR: {e}")
            results['Shift-Or'][k] = None
    
    return results


# =============================================================================
# PLOTTING
# =============================================================================

def plot_results(time_results, memory_results):
    """Create two plots: Time vs k, and Memory vs k."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Plot 1: Time vs Edit Distance
    for algo_name, measurements in time_results.items():
        k_values = sorted([k for k in measurements.keys() if measurements[k] is not None])
        times = [measurements[k] for k in k_values]
        
        ax1.plot(k_values, times, marker='o', label=algo_name, linewidth=2, markersize=8)
    
    ax1.set_xlabel('Edit Distance (k)', fontsize=12)
    ax1.set_ylabel('Time (seconds)', fontsize=12)
    ax1.set_title('Time vs Edit Distance\n(T=100K bases, P=20 bases)', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10, loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(sorted(time_results[list(time_results.keys())[0]].keys()))
    
    # Plot 2: Memory vs Edit Distance
    for algo_name, measurements in memory_results.items():
        k_values = sorted([k for k in measurements.keys() if measurements[k] is not None])
        memory = [measurements[k] for k in k_values]
        
        ax2.plot(k_values, memory, marker='o', label=algo_name, linewidth=2, markersize=8)
    
    ax2.set_xlabel('Edit Distance (k)', fontsize=12)
    ax2.set_ylabel('Peak Memory (bytes)', fontsize=12)
    ax2.set_title('Memory vs Edit Distance\n(T=100K bases, P=20 bases)', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10, loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(sorted(memory_results[list(memory_results.keys())[0]].keys()))
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    plt.suptitle('Fuzzy Matching Algorithm Comparison', fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    plt.savefig('fuzzy_matching_benchmark.png', dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to fuzzy_matching_benchmark.png")
    plt.show()


def main():
    """Main execution."""
    print("="*60)
    print("FUZZY MATCHING BENCHMARK")
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
    TEXT_SIZE = 100000  # T = 100K bases
    PATTERN_LENGTH = 20  # P = 20 bases
    
    text = full_sequence[:TEXT_SIZE]
    pattern = full_sequence[1000:1000+PATTERN_LENGTH]
    
    print(f"\nFIXED PARAMETERS:")
    print(f"  Text size (T): {len(text):,} bases")
    print(f"  Pattern length (P): {PATTERN_LENGTH} bases")
    print(f"  Pattern: {pattern}")
    
    # Variable parameter
    k_values = [0, 1, 2, 3, 4, 5]
    print(f"\nVARIABLE PARAMETER:")
    print(f"  Edit distance (k): {k_values}")
    
    # Run benchmarks
    time_results = run_time_benchmarks(text, pattern, k_values)
    memory_results = run_memory_benchmarks(text, pattern, k_values)
    
    # Plot results
    print("\nGenerating plots...")
    plot_results(time_results, memory_results)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\nTime (seconds):")
    for algo in time_results:
        print(f"  {algo:25s}: {list(time_results[algo].values())}")
    
    print("\nMemory (MB):")
    for algo in memory_results:
        mem_mb = [v/(1024*1024) if v else None for v in memory_results[algo].values()]
        print(f"  {algo:25s}: {mem_mb}")
    
    print("\nBenchmark complete!")


if __name__ == '__main__':
    main()
