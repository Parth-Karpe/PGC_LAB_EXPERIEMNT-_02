#include <stdio.h>
#include <pthread.h>

#define ARRAY_SIZE 8
int array[ARRAY_SIZE] = {10, 20, 30, 40, 50, 60, 70, 80};
int partial_sums[4];

typedef struct
{
    int thread_id;
    int start_index;
    int end_index;
} ThreadData;

void *calculate_sum(void *arg)
{
    ThreadData *data = (ThreadData *)arg;
    int sum = 0;
    for (int i = data->start_index; i < data->end_index; i++)
    {
        sum += array[i];
    }
    partial_sums[data->thread_id] = sum;
    printf("Thread %d partial sum = %d\n", data->thread_id + 1, sum);
    return NULL;
}

int main()
{
    pthread_t threads[4];
    ThreadData thread_data[4];

    for (int i = 0; i < 4; i++)
    {
        thread_data[i].thread_id = i;
        thread_data[i].start_index = i * 2;
        thread_data[i].end_index = (i + 1) * 2;
        pthread_create(&threads[i], NULL, calculate_sum, &thread_data[i]);
    }

    for (int i = 0; i < 4; i++)
    {
        pthread_join(threads[i], NULL);
    }

    int total_sum = 0;
    for (int i = 0; i < 4; i++)
    {
        total_sum += partial_sums[i];
    }

    printf("Total sum = %d\n", total_sum);
    return 0;
}
