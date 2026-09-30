#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

#define N 1000000000L

double get_time()
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main(int argc, char *argv[])
{
    double sum = 0.0;
    int num_threads = 1;

    if (argc > 1)
    {
        num_threads = atoi(argv[1]);
    }
    else
    {
        printf("Enter number of threads: ");
        if (scanf("%d", &num_threads) != 1) return 1;
    }

    if (num_threads < 1 || num_threads > 32)
    {
        printf("Please enter a value between 1 and 32.\n");
        return 1;
    }

    omp_set_num_threads(num_threads);

    double start_time = get_time();

    #pragma omp parallel for reduction(+:sum)
    for (long i = 0; i < N; i++)
    {
        sum += (double)i * 0.000001;
    }

    double end_time = get_time();

    printf("Threads = %d\n", num_threads);
    printf("Sum = %.2f\n", sum);
    printf("Time = %.6f seconds\n", end_time - start_time);

    return 0;
}
