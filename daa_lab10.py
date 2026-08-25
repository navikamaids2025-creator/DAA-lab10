import streamlit as st
import random
import time
import sys

sys.setrecursionlimit(20000)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="QuickSort Experiment",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ QuickSort Algorithm Experiment")

st.write(
    "Comparison of Deterministic QuickSort and "
    "Randomized QuickSort."
)


# ============================================================
# GLOBAL COMPARISON COUNTER
# ============================================================

comparisons = 0


# ============================================================
# PARTITION
# ============================================================

def partition(arr, low, high):

    global comparisons

    pivot = arr[high]

    i = low - 1

    for j in range(low, high):

        comparisons += 1

        if arr[j] <= pivot:

            i += 1

            arr[i], arr[j] = (
                arr[j],
                arr[i]
            )

    arr[i + 1], arr[high] = (
        arr[high],
        arr[i + 1]
    )

    return i + 1


# ============================================================
# DETERMINISTIC QUICKSORT
# ============================================================

def deterministic_quicksort(arr, low, high):

    if low < high:

        pi = partition(
            arr,
            low,
            high
        )

        deterministic_quicksort(
            arr,
            low,
            pi - 1
        )

        deterministic_quicksort(
            arr,
            pi + 1,
            high
        )


# ============================================================
# RANDOMIZED QUICKSORT
# ============================================================

def randomized_quicksort(arr, low, high):

    if low < high:

        # Choose random pivot
        rand_idx = random.randint(
            low,
            high
        )

        # Move random pivot to end
        arr[rand_idx], arr[high] = (
            arr[high],
            arr[rand_idx]
        )

        pi = partition(
            arr,
            low,
            high
        )

        randomized_quicksort(
            arr,
            low,
            pi - 1
        )

        randomized_quicksort(
            arr,
            pi + 1,
            high
        )


# ============================================================
# RUN TEST
# ============================================================

def run_test(sort_function, arr):

    global comparisons

    # Copy original array
    a = arr[:]

    comparisons = 0

    start = time.perf_counter()

    sort_function(
        a,
        0,
        len(a) - 1
    )

    elapsed = (
        time.perf_counter() - start
    ) * 1000

    return comparisons, elapsed


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Settings")

N = st.sidebar.number_input(
    "Number of Elements",
    min_value=100,
    max_value=10000,
    value=5000,
    step=100
)

run = st.sidebar.button(
    "🚀 Run Experiment"
)


# ============================================================
# RUN EXPERIMENT
# ============================================================

if run:

    with st.spinner(
        "Running QuickSort experiments..."
    ):

        # ----------------------------------------------------
        # Create test cases
        # ----------------------------------------------------

        test_cases = {

            "Random": [
                random.randint(
                    1,
                    100000
                )
                for _ in range(N)
            ],

            "Sorted": list(
                range(N)
            ),

            "Reverse": list(
                range(N, 0, -1)
            ),

            "Nearly Sorted": list(
                range(N)
            )
        }

        # ----------------------------------------------------
        # Make Nearly Sorted slightly shuffled
        # ----------------------------------------------------

        ns = test_cases["Nearly Sorted"]

        for _ in range(N // 20):

            i = random.randint(
                0,
                N - 1
            )

            j = random.randint(
                0,
                N - 1
            )

            ns[i], ns[j] = (
                ns[j],
                ns[i]
            )

        # ----------------------------------------------------
        # Run tests
        # ----------------------------------------------------

        results = []

        for case, arr in test_cases.items():

            d_comps, d_time = run_test(
                deterministic_quicksort,
                arr
            )

            r_comps, r_time = run_test(
                randomized_quicksort,
                arr
            )

            results.append({
                "Input Type": case,
                "DQS Comparisons": d_comps,
                "DQS Time (ms)": round(
                    d_time,
                    2
                ),
                "RQS Comparisons": r_comps,
                "RQS Time (ms)": round(
                    r_time,
                    2
                )
            })


    # ========================================================
    # RESULTS
    # ========================================================

    st.success(
        "Experiment completed successfully!"
    )

    st.header(
        f"📊 Results for N = {N}"
    )

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # AVERAGE TIME
    # ========================================================

    avg_dqs = sum(
        row["DQS Time (ms)"]
        for row in results
    ) / len(results)

    avg_rqs = sum(
        row["RQS Time (ms)"]
        for row in results
    ) / len(results)


    col1, col2 = st.columns(2)

    col1.metric(
        "Average DQS Time",
        f"{avg_dqs:.2f} ms"
    )

    col2.metric(
        "Average RQS Time",
        f"{avg_rqs:.2f} ms"
    )


    # ========================================================
    # EXECUTION TIME CHART
    # ========================================================

    st.subheader(
        "⏱️ Execution Time Comparison"
    )

    chart_data = {
        "Input Type": [
            row["Input Type"]
            for row in results
        ],

        "Deterministic QuickSort": [
            row["DQS Time (ms)"]
            for row in results
        ],

        "Randomized QuickSort": [
            row["RQS Time (ms)"]
            for row in results
        ]
    }

    st.bar_chart(
        chart_data,
        x="Input Type"
    )


    # ========================================================
    # COMPARISON CHART
    # ========================================================

    st.subheader(
        "🔢 Number of Comparisons"
    )

    comparison_data = {
        "Input Type": [
            row["Input Type"]
            for row in results
        ],

        "Deterministic QuickSort": [
            row["DQS Comparisons"]
            for row in results
        ],

        "Randomized QuickSort": [
            row["RQS Comparisons"]
            for row in results
        ]
    }

    st.bar_chart(
        comparison_data,
        x="Input Type"
    )


    # ========================================================
    # OBSERVATION
    # ========================================================

    st.subheader("📝 Observation")

    st.info(
        """
        **Deterministic QuickSort** always chooses the last element
        as the pivot. Therefore, sorted and reverse-sorted inputs can
        produce the worst-case **O(N²)** behavior.

        **Randomized QuickSort** chooses a random pivot, making
        consistently poor partitions much less likely.

        The average-case complexity of QuickSort is **O(N log N)**,
        while the worst-case complexity is **O(N²)**.
        """
    )
