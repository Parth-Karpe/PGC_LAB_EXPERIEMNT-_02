# Experiment 02 Formal Academic Laboratory Report

**Course:** Parallel and GPU Computing (PGC) Laboratory  
**Experiment Title:** Develop Multithreaded Programs Using Parallel Programming Libraries (POSIX Threads & OpenMP) to Understand Thread Creation, Management, Work Distribution, Synchronization, and Performance  
**Author:** Parth Karpe  
**Repository:** [Parth-Karpe/PGC_LAB_EXPERIEMNT_02](https://github.com/Parth-Karpe/PGC_LAB_EXPERIEMNT_02)  
**Environment:** WSL2 Ubuntu (GCC 15.2.0, POSIX Threads, OpenMP 4.5/5.0)

---

## 1. AIM & Objectives
To develop, analyze, and benchmark multithreaded programs using **POSIX Threads (Pthreads)** and **OpenMP** in C to understand:
1. Thread creation and termination (`pthread_create`, `pthread_join`, `#pragma omp parallel`).
2. Thread identification and work distribution (`omp_get_thread_num`, `#pragma omp parallel for`).
3. Race condition detection and prevention (`pthread_mutex_t`, `#pragma omp critical`).
4. Thread coordination and synchronization points (`#pragma omp barrier`).
5. Empirical speedup and parallel efficiency scaling across 1, 2, 4, 6, and 16 threads for $10^9$ operations.

---

## 2. Theoretical Foundations

### 2.1 Pthreads (Explicit Low-Level Concurrency)
Pthreads provides an IEEE POSIX 1003.1c standard API in C. The programmer is responsible for:
* Explicit thread lifecycle management (`pthread_create`, `pthread_join`).
* Manual calculation of loop bounds for workload partitioning.
* Explicit allocation and destruction of synchronization primitives (`pthread_mutex_init`, `pthread_mutex_destroy`).

### 2.2 OpenMP (Directive-Based High-Level Concurrency)
OpenMP relies on compiler directives (`#pragma omp ...`), environment variables, and runtime library routines.
* Fork-Join execution model.
* Automatic loop scheduling and chunking (`#pragma omp parallel for`).
* Built-in reduction operators (`reduction(+:variable)`) avoiding lock contention.

---

## 3. Implementation Modules & Code Structure

### Part A: Pthreads Suite
1. **`src/01_pthreads/thread1.c`:** Creation and waiting of a single worker thread.
2. **`src/01_pthreads/thread2.c`:** Creation of 4 concurrent threads with explicit ID passing.
3. **`src/01_pthreads/thread_sum.c`:** Static partitioning of an 8-element array into 4 chunks of size 2, summing to 360.
4. **`src/01_pthreads/race.c`:** Deliberate race condition on a shared counter across 4 threads.
5. **`src/01_pthreads/mutex.c`:** Mutual exclusion lock protecting the critical section.
6. **`src/01_pthreads/pthread_perf.c`:** Scalable $N=10^9$ benchmark parameterized by thread count.

### Part B: OpenMP Suite
1. **`src/02_openmp/omp1.c`:** Parallel region with 16 threads querying IDs and team size.
2. **`src/02_openmp/omp_sum.c`:** Parallel for-loop reduction over 8 elements.
3. **`src/02_openmp/omp_race.c`:** OpenMP unsynchronized incrementation producing data hazard.
4. **`src/02_openmp/omp_critical.c`:** Critical section directive ensuring mutual exclusion.
5. **`src/02_openmp/omp_barrier.c`:** Two-stage phased execution enforcing all threads meet before phase 2.
6. **`src/02_openmp/omp_perf.c`:** Parallel for reduction benchmark over $N=10^9$ arithmetic operations.

### Part C: Baseline
1. **`src/03_sequential/sequential.c`:** Single-threaded baseline reference program.

---

## 4. Experimental Results & Verification

### 4.1 Verification Invariants
* **Array Sum (8 elements):** Total sum = $10+20+30+40+50+60+70+80 = \mathbf{360}$
* **Counter Increments (4 threads $\times$ 100,000):** Expected = $\mathbf{400,000}$
  * `race.c`: **150,011** (Race occurred)
  * `mutex.c`: **400,000** (Verified)
  * `omp_race.c`: **100,112** (Race occurred)
  * `omp_critical.c`: **400,000** (Verified)
* **Large Computational Sum ($N=10^9$):** Expected = $\mathbf{499,999,999,500.00}$ (Verified across all runs)

### 4.2 Benchmark Data Table
| Threads | Sequential (s) | Pthreads (s) | Pthreads Speedup | OpenMP (s) | OpenMP Speedup | OpenMP Efficiency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | 1.845448 | 1.812432 | 1.02× | 1.828267 | 1.01× | 100.9% |
| **2** | 1.845448 | 3.604127 | 0.51× | 0.940907 | 1.96× | 98.1% |
| **4** | 1.845448 | 4.572821 | 0.40× | 0.483794 | 3.81× | 95.4% |
| **6** | 1.845448 | 5.266353 | 0.35× | 0.356250 | 5.18× | 86.3% |
| **16** | 1.845448 | 10.175397 | 0.18× | **0.209669** | **8.80×** | **55.0%** |

---

## 5. Visual Evidence Artifacts
* **WSL Setup & Thread 1:** `results/screenshots/01_wsl_gcc_thread1.png`
* **Thread 2 Execution:** `results/screenshots/02_thread2_execution.png`
* **Thread Sum Reduction:** `results/screenshots/03_thread_sum_execution.png`
* **Pthreads Race vs Mutex:** `results/screenshots/04_pthread_race_mutex.png`
* **OpenMP 16 Threads:** `results/screenshots/05_omp1_16threads.png`
* **OpenMP Race, Critical & Barrier:** `results/screenshots/06_omp_sum_race_critical_barrier.png`
* **Pthreads Scaling Performance:** `results/screenshots/07_pthread_perf_scaling.png`
* **OpenMP Scaling Performance:** `results/screenshots/08_omp_perf_scaling.png`
* **Full Benchmark Execution Trace:** `results/screenshots/09_full_performance_scaling.png`

---

## 6. Conclusion
1. OpenMP directive-based parallelism provides exceptional scalability for data-parallel loop reductions, achieving an empirical **$8.80\times$ speedup on 16 threads** with minimal developer boilerplate.
2. Race conditions occur in both Pthreads and OpenMP when multiple threads mutate shared memory without synchronization; they are reliably resolved using `pthread_mutex_t` and `#pragma omp critical`.
3. Coordination across parallel execution phases is cleanly achieved via `#pragma omp barrier`.
