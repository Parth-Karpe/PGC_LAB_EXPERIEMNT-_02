# Experiment 02: Performance Analysis & Scaling Characteristics

## 1. Problem Definition & Mathematical Invariant
* **Workload Description:** Large-scale double-precision arithmetic reduction sum over $N = 1,000,000,000$ iterations.
* **Element Formula:**
  $$S = \sum_{i=0}^{N-1} (i \times 10^{-6}) = 10^{-6} \times \frac{(N-1)N}{2}$$
* **Mathematical Target:**
  $$\text{Target} = 10^{-6} \times \frac{999,999,999 \times 1,000,000,000}{2} = \mathbf{499,999,999,500.00}$$

---

## 2. Experimental Timing & Scaling Summary Table

| Computing Model | Threads ($p$) | Execution Time ($T_p$, s) | Measured Speedup ($S_p = \frac{T_{\text{seq}}}{T_p}$) | Parallel Efficiency ($E_p = \frac{S_p}{p} \times 100$) | Verification Sum | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sequential (Baseline)** | 1 | **1.845448 s** | **1.0000×** | **100.00%** | `499999999500.00` | ✅ Passed |
| **Pthreads** | 1 | **1.812432 s** | **1.0182×** | **101.82%** | `499999999500.00` | ✅ Passed |
| **Pthreads** | 2 | **3.604127 s** | **0.5120×** | **25.60%** | `499999999500.00` | ✅ Passed |
| **Pthreads** | 4 | **4.572821 s** | **0.4036×** | **10.09%** | `499999999500.00` | ✅ Passed |
| **Pthreads** | 6 | **5.266353 s** | **0.3504×** | **5.84%** | `499999999500.00` | ✅ Passed |
| **Pthreads** | 16 | **10.175397 s** | **0.1814×** | **1.13%** | `499999999500.00` | ✅ Passed |
| **OpenMP** | 1 | **1.828267 s** | **1.0094×** | **100.94%** | `499999999500.00` | ✅ Passed |
| **OpenMP** | 2 | **0.940907 s** | **1.9613×** | **98.07%** | `499999999500.00` | ✅ Passed |
| **OpenMP** | 4 | **0.483794 s** | **3.8145×** | **95.36%** | `499999999500.00` | ✅ Passed |
| **OpenMP** | 6 | **0.356250 s** | **5.1802×** | **86.34%** | `499999999500.00` | ✅ Passed |
| **OpenMP** | 16 | **0.209669 s** | **8.8017×** | **55.01%** | `499999999500.00` | ✅ Passed |

---

## 3. Key Observations & Theoretical Derivations

### A. OpenMP High Parallel Efficiency
* **Scaling Behavior:** OpenMP demonstrates outstanding near-linear scaling up to 6 cores ($5.18\times$ speedup, $86.34\%$ efficiency) and peaks at **$8.80\times$ speedup on 16 threads** ($0.209669\text{ s}$).
* **Compiler Optimization & Reduction Tree:** The `#pragma omp parallel for reduction(+:sum)` directive allows the GCC runtime to allocate thread-local accumulators in CPU registers and merge them in $O(\log p)$ steps without cache-line false sharing or kernel-space lock contention.

### B. Pthreads Thread Creation & Memory Contention Overhead
* **Scaling Behavior:** In `pthread_perf.c`, increasing thread count exhibits thread-creation overhead, thread context switching, and non-optimized accumulator writing, showing negative scaling under this specific micro-benchmark setup compared to OpenMP's compiler-level vectorization and loop chunk scheduling.

### C. Synchronization Mechanics: Race Condition vs Protection
1. **Unsynchronized Accumulation:**
   * Expected: $400,000$ (4 threads $\times$ 100,000 increments)
   * `race.c` (Pthreads): Recorded **$150,011$** (Lost updates due to interleaved read-modify-write CPU instructions).
   * `omp_race.c` (OpenMP): Recorded **$100,112$** (Severe data corruption across concurrent cores).
2. **Synchronized Execution:**
   * `mutex.c` (`pthread_mutex_lock` / `unlock`): Recorded exact **$400,000$** (100% correct).
   * `omp_critical.c` (`#pragma omp critical`): Recorded exact **$400,000$** (100% correct).
3. **Coordination via Barrier:**
   * `omp_barrier.c` strictly enforces that all 4 threads finish Stage 1 before any thread is allowed to progress into Stage 2.
