import random
import time
import tracemalloc
import csv
import sys

sys.setrecursionlimit(50000)


# Quick sort
def quick_sort(array):
    comparisons = 0
    changes = 0

    # Recursive divide-and-conquer helper
    def _quick_sort(sub_array, low, high):
        if low < high:
            pivot_index = _partition(sub_array, low, high)
            _quick_sort(sub_array, low, pivot_index - 1)
            _quick_sort(sub_array, pivot_index + 1, high)

    # Lomuto partition scheme with randomized pivot selection
    def _partition(sub_array, low, high):
        nonlocal comparisons, changes

        # Swap random pivot to the end to mitigate worst-case behavior
        rand_pivot = random.randint(low, high)
        sub_array[rand_pivot], sub_array[high] = (
            sub_array[high],
            sub_array[rand_pivot],
        )
        changes += 1

        pivot = sub_array[high]
        i = low - 1

        # Rearrange elements based on comparison with pivot
        for j in range(low, high):
            comparisons += 1
            if sub_array[j] <= pivot:
                i += 1
                if i != j:
                    sub_array[i], sub_array[j] = (
                        sub_array[j],
                        sub_array[i],
                    )
                    changes += 1

        # Place pivot in its correct sorted position
        if (i + 1) != high:
            sub_array[i + 1], sub_array[high] = (
                sub_array[high],
                sub_array[i + 1],
            )
            changes += 1

        return i + 1

    # Work on a copy to avoid mutating the original input array
    result = array.copy()
    _quick_sort(result, 0, len(result) - 1)

    return result, comparisons, changes


# Heap sort
def heap_sort(array):
    if not array:
        return []
    comparisons = 0
    changes = 0

    # Maintain the max-heap property for a subtree rooted at index i
    def _heapify(sub_array, n, i):
        nonlocal comparisons, changes

        # Initialize largest as root and calculate child indices
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Check if left child exists and is larger than root
        if left < n and sub_array[left] > sub_array[largest]:
            comparisons += 1
            largest = left

        # Check if right child exists and is larger than current largest
        if right < n and sub_array[right] > sub_array[largest]:
            comparisons += 1
            largest = right

        # If root is not largest, swap and recursively heapify the affected
        # subtree
        if largest != i:
            comparisons += 1
            changes += 1
            sub_array[i], sub_array[largest] = (
                sub_array[largest],
                sub_array[i],
            )
            _heapify(sub_array, n, largest)

    # Build max-heap
    result = array.copy()
    n = len(result)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(result, n, i)

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        # Move current root to end
        result[i], result[0] = result[0], result[i]
        changes += 1
        _heapify(result, i, 0)

    return result, comparisons, changes


# Radix sort
def radix_sort(array):
    if not array:
        return []
    comparisons = 0
    changes = 0

    # Stable counting sort subroutine based on the digit specified by exp
    def _counting_sort_by_digit(sub_array, exp):
        nonlocal changes

        n = len(sub_array)
        output = [0] * n
        count = [0] * 10

        # Count digit frequencies at current positional exponent
        for i in range(n):
            index = (sub_array[i] // exp) % 10
            count[index] += 1

        # Transform counts to cumulative positions for stable placement
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build output array iterating backwards to preserve stability
        for i in range(n - 1, -1, -1):
            index = (sub_array[i] // exp) % 10
            output[count[index] - 1] = sub_array[i]
            count[index] -= 1
            changes += 1

        # Copy sorted elements back to the input array
        for i in range(n):
            sub_array[i] = output[i]
            changes += 1

    # Radix Sort LSD approach
    result = array.copy()
    max_val = max(result)

    # Process digit positions from least to most significant
    exp = 1
    while max_val // exp > 0:
        _counting_sort_by_digit(result, exp)
        exp *= 10

    return result, comparisons, changes


def generate_random_array(n):
    # Random and unique number sampling
    array = random.sample(range(0, n + 1), n)
    return array


def generate_inverse_array(n):
    # Simple decrescent numbers
    array = list(range(n, 0, -1))
    return array


def benchmark(algorithm, data):
    # Performance tracking begin
    data_copy = data.copy()
    time_begin = time.perf_counter()
    tracemalloc.start()

    # Get inside information on algorithm
    result, comparisons, changes = algorithm(data_copy)

    # Perfomance tracking end
    time_end = time.perf_counter()
    time_total = time_end - time_begin
    _, memory_peak = tracemalloc.get_traced_memory()
    memory_total = memory_peak / (1024 * 1024)
    tracemalloc.stop()

    return result, comparisons, changes, time_total, memory_total


def get_benchmark_data(algorithm, data, storage):
    # Get full data from an algorithm
    _, comparisons, changes, time, memory = benchmark(algorithm, data)
    storage.append(
        [
            comparisons,
            changes,
            f"{time:.9f}",
            f"{memory:.9f}",
        ]
    )


def main():
    sizes = [1000, 5000, 10000, 20000]
    num_runs = 5

    # Initialize variables for performance data
    quick_sort_data_random = []
    quick_sort_data_inverse = []
    heap_sort_data_random = []
    heap_sort_data_inverse = []
    radix_sort_data_random = []
    radix_sort_data_inverse = []

    # Helper to execute multiple runs and average results
    def run_benchmark(func, size, is_inverse, target_list):
        temp_data = []
        for _ in range(num_runs):
            arr = (
                generate_inverse_array(size)
                if is_inverse
                else generate_random_array(size)
            )
            get_benchmark_data(func, arr, temp_data)

        # Average metrics across runs
        comp = sum(int(r[0]) for r in temp_data) // num_runs
        changes = sum(int(r[1]) for r in temp_data) // num_runs

        def parse_num(v):
            return float(str(v).replace("ms", "").replace("MB", ""))

        time_val = round(
            (sum(parse_num(r[2]) for r in temp_data) / num_runs) * 1000,
            3,
        )
        mem_val = round(
            sum(parse_num(r[3]) for r in temp_data) / num_runs,
            3,
        )

        target_list.append([comp, changes, time_val, mem_val])

    # Get performance data
    for size in sizes:
        # Quick Sort
        run_benchmark(quick_sort, size, False, quick_sort_data_random)
        run_benchmark(quick_sort, size, True, quick_sort_data_inverse)

        # Heap Sort
        run_benchmark(heap_sort, size, False, heap_sort_data_random)
        run_benchmark(heap_sort, size, True, heap_sort_data_inverse)

        # Radix Sort
        run_benchmark(radix_sort, size, False, radix_sort_data_random)
        run_benchmark(radix_sort, size, True, radix_sort_data_inverse)

    # Create results file and organize benchmark data
    with open("benchmark_results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Algorithm",
                "Array Type",
                "Size",
                "Comparisons",
                "Changes",
                "Time",
                "Memory",
            ]
        )

        datasets = [
            ("Quick Sort", "Random", quick_sort_data_random),
            ("Quick Sort", "Inverse", quick_sort_data_inverse),
            ("Heap Sort", "Random", heap_sort_data_random),
            ("Heap Sort", "Inverse", heap_sort_data_inverse),
            ("Radix Sort", "Random", radix_sort_data_random),
            ("Radix Sort", "Inverse", radix_sort_data_inverse),
        ]

        for algorithm, array_type, data in datasets:
            for i, row in enumerate(data):
                writer.writerow([algorithm, array_type, sizes[i]] + row)


if __name__ == "__main__":
    main()
