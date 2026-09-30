#include <stdio.h>
#include <pthread.h>

void *print_message(void *arg)
{
    int thread_num = *(int *)arg;
    printf("Thread %d is running\n", thread_num);
    return NULL;
}

int main()
{
    pthread_t threads[4];
    int thread_ids[4];

    for (int i = 0; i < 4; i++)
    {
        thread_ids[i] = i + 1;
        pthread_create(&threads[i], NULL, print_message, &thread_ids[i]);
    }

    for (int i = 0; i < 4; i++)
    {
        pthread_join(threads[i], NULL);
    }

    return 0;
}
