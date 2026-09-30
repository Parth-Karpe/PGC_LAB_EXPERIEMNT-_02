CC = gcc
CFLAGS = -O2 -Wall
PTHREAD_FLAGS = -pthread
OMP_FLAGS = -fopenmp

TARGETS = \
    01_pthreads/thread1 \
    01_pthreads/thread2 \
    01_pthreads/thread_sum \
    01_pthreads/race \
    01_pthreads/mutex \
    01_pthreads/pthread_perf \
    02_openmp/omp1 \
    02_openmp/omp_sum \
    02_openmp/omp_race \
    02_openmp/omp_critical \
    02_openmp/omp_barrier \
    02_openmp/omp_perf \
    03_sequential/sequential

all: $(TARGETS)

01_pthreads/%: 01_pthreads/%.c
	$(CC) $(CFLAGS) $< -o $@ $(PTHREAD_FLAGS)

02_openmp/%: 02_openmp/%.c
	$(CC) $(CFLAGS) $< -o $@ $(OMP_FLAGS)

03_sequential/%: 03_sequential/%.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(TARGETS)

.PHONY: all clean
