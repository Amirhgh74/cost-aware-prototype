#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "empty-tp.h"


char zero_16b[16] = { 0 };
char zero_64b[64] = { 0 };
char zero_256b[256] = { 0 };
char zero_512b[512] = { 0 };
int result[1000];



void do_trace(){
    // tracepoint(empty_tp, empty_tp_4b, 0);
    // tracepoint(empty_tp, empty_tp_16b, zero_16b);
    // tracepoint(empty_tp, empty_tp_64b, zero_64b);
    // tracepoint(empty_tp, empty_tp_256b, zero_256b);
    // tracepoint(empty_tp, empty_tp_512b, zero_256b, zero_256b);
    // tracepoint(empty_tp, empty_tp_1k, zero_256b, zero_256b, zero_256b, zero_256b);
    tracepoint(empty_tp, empty_tp_2k, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b);
}

void write_results(){
    FILE *f;
    f = fopen("2k.txt" , "w");

    char text [10];

    int i = 0;
    for (i = 0; i < 1000; i++){
        snprintf (text, sizeof(text), "%d",result[i]);
        fprintf(f, text);
        fprintf(f, "\n");
    }

    fclose(f);
}

int main(int argc, char *argv[])
{
    
    int x;
    struct timespec start, end;
    long long latency;


    puts("Hello, World!\nPress Enter to continue...");

    /*
     * The following getchar() call is only placed here for the purpose
     * of this demonstration, to pause the application in order for
     * you to have time to list its tracepoints. It's not needed
     * otherwise.
     */
    getchar();

    /*
     * A tracepoint() call.
     *
     * Arguments, as defined in hello-tp.h:
     *
     * 1. Tracepoint provider name   (required)
     * 2. Tracepoint name            (required)
     * 3. my_integer_arg             (first user-defined argument)
     * 4. my_string_arg              (second user-defined argument)
     *
     * Notice the tracepoint provider and tracepoint names are
     * NOT strings: they are in fact parts of variables that the
     * macros in hello-tp.h create.
     */
    // tracepoint(hello_world, my_first_tracepoint, 23, "hi there!");

    // for (x = 0; x < argc; ++x) {
    //     tracepoint(hello_world, my_first_tracepoint, x, argv[x]);
    // }

    // puts("Quitting now!");
    // tracepoint(hello_world, my_first_tracepoint, x * x, "x^2");

    int i;

    for (i =0; i < 50; i++){
        do_trace();
    }


    for (i = 0; i < 1000; i++){
        clock_gettime(CLOCK_MONOTONIC, &start);
        do_trace();
        clock_gettime(CLOCK_MONOTONIC, &end);
        latency = (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

        result[i] = latency;
    }


    // for (i = 0; i < 1000; i++){
    //     printf("latency is : %d\n" , result[i]);
    // }

    write_results();

    return 0;
}
