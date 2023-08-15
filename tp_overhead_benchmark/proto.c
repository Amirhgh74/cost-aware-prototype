#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "empty-tp.h"
#include <unistd.h>


char zero_16b[16] = { 0 };
char zero_64b[64] = { 0 };
char zero_256b[256] = { 0 };
char zero_512b[512] = { 0 };
int result[1000];


int x;
struct timespec start, end;
long long latency_start, latency_end;

int short_l = 0;
int long_l = 0;
int file_l = 0;
int memory_l = 0;
int input_l = 0;


int count_short = 0;
int count_long = 0;
int count_file = 0;
int count_memory = 0;
int count_input = 0;


int short_l_2 = 0;
int long_l_2 = 0;
int file_l_2 = 0;
int memory_l_2 = 0;
int input_l_2 = 0;


int count_short_2 = 0;
int count_long_2 = 0;
int count_file_2 = 0;
int count_memory_2 = 0;
int count_input_2 = 0;




void short_loop_fun(){
    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    short_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

   
    int i = 0;

    for (i = 0; i < 100; i++){
        // do something
    }

    short_loop_fun_2();
    file_access_fun_2();
    
    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    short_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_short += 2;
}

void long_loop_fun(){

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_1k, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    long_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);
    
    int i = 0;

    for (i = 0; i < 800; i ++){
        // do something
    }

    long_loop_fun_2();
    file_access_fun_2();

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_1k, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    long_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_long += 2;
}

void file_access_fun(){

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_64b, zero_64b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    file_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);


    FILE *f;
    f = fopen("dummy.txt" , "w");

    char * tmp = "this is a test";

    int i = 0;
    for (i = 0; i < 50; i++){
        fprintf(f, "%s" ,tmp);
        fprintf(f,"%s", "\n");
    }

    fclose(f);


    file_access_fun_2();

    file_access_fun_2();

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_64b, zero_64b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    file_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_file += 2;

}

void memory_aloc_fun(){
    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_2k, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    memory_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    void* ptr;
    int i = 0;

    ptr = (int*) malloc(1 * sizeof(int));
    sleep(1);
    free(ptr);

    file_access_fun_2();

    short_loop_fun_2();

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_2k, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    memory_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_memory += 2;
}


// void block_input_fun(){
//     clock_gettime(CLOCK_MONOTONIC, &start);
//     tracepoint(empty_tp, empty_tp_512b, zero_256b, zero_256b);
//     clock_gettime(CLOCK_MONOTONIC, &end);
//     input_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

//     int n ;

//     printf("enter a number to continue ...\n");
//     scanf("%d" , &n);

//     printf("you have entered %d\n" , n);
//     int i = 0;

//     file_access_fun_2();

//     long_loop_fun_2();


//     clock_gettime(CLOCK_MONOTONIC, &start);
//     tracepoint(empty_tp, empty_tp_512b, zero_256b, zero_256b);
//     clock_gettime(CLOCK_MONOTONIC, &end);
//     input_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

//     count_input += 2 ;
// }

void short_loop_fun_2(){
    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_256b_2, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    short_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

   
    int i = 0;

    for (i = 0; i < 100; i++){
        // do something
    }

    memory_aloc_fun_2();

    // block_input_fun_2();
    
    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_256b_2, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    short_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_short_2 += 2;
}


void long_loop_fun_2(){

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_1k_2, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    long_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);
    
    int i = 0;

    for (i = 0; i < 800; i ++){
        // do something
    }

   
    memory_aloc_fun_2();


    // block_input_fun_2();

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_1k_2, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    long_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_long_2 += 2;
}

void file_access_fun_2(){

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_64b_2, zero_64b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    file_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);


    FILE *f;
    f = fopen("dummy.txt" , "w");

    char * tmp = "this is a test";

    int i = 0;
    for (i = 0; i < 500; i++){
        fprintf(f, "%s" ,tmp);
        fprintf(f,"%s", "\n");
    }

    fclose(f);

    
    short_loop_fun_2();


    memory_aloc_fun_2();

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_64b_2, zero_64b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    file_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_file_2 += 2;

}

void memory_aloc_fun_2(){
    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_2k_2, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    memory_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    void* ptr;

    ptr = (int*) malloc(1 * sizeof(int));
    sleep(1);
    free(ptr);

    clock_gettime(CLOCK_MONOTONIC, &start);
    tracepoint(empty_tp, empty_tp_2k_2, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b);
    clock_gettime(CLOCK_MONOTONIC, &end);
    memory_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

    count_memory_2 += 2;
}


// void block_input_fun_2(){
//     clock_gettime(CLOCK_MONOTONIC, &start);
//     tracepoint(empty_tp, empty_tp_512b_2, zero_256b, zero_256b);
//     clock_gettime(CLOCK_MONOTONIC, &end);
//     input_l_2 += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

//     int n ;

//     printf("enter a number to continue ...\n");
//     scanf("%d" , &n);

//     printf("you have entered %d\n" , n);

//     clock_gettime(CLOCK_MONOTONIC, &start);
//     tracepoint(empty_tp, empty_tp_512b_2, zero_256b, zero_256b);
//     clock_gettime(CLOCK_MONOTONIC, &end);
//     input_l += (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);

//     count_input_2 += 2 ;
// }





// void do_trace(){
//     // tracepoint(empty_tp, empty_tp_4b, 0);
//     // tracepoint(empty_tp, empty_tp_16b, zero_16b);
//     // tracepoint(empty_tp, empty_tp_64b, zero_64b);
//     // tracepoint(empty_tp, empty_tp_256b, zero_256b);
//     // tracepoint(empty_tp, empty_tp_512b, zero_256b, zero_256b);
//     // tracepoint(empty_tp, empty_tp_1k, zero_256b, zero_256b, zero_256b, zero_256b);
//     // tracepoint(empty_tp, empty_tp_2k, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b, zero_256b);
// }

void write_results(){
    FILE *f;
    f = fopen("result_2.txt" , "w");
    
    fprintf(f, "%s", "empty_tp_256b");
    fprintf(f, "%s", ",");

    fprintf(f, "%d", short_l);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_short);
    fprintf(f, "%s", "\n");

    fprintf(f, "%s", "empty_tp_1k");
    fprintf(f, "%s", ",");

    fprintf(f, "%d", long_l);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_long);
    fprintf(f, "%s", "\n");


    fprintf(f, "%s", "empty_tp_64b");
    fprintf(f, "%s", ",");

    fprintf(f, "%d", memory_l);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_memory);
    fprintf(f, "%s", "\n");

    fprintf(f, "%s", "empty_tp_2k");
    fprintf(f, "%s", ",");


    fprintf(f, "%d", file_l);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_file);
    fprintf(f, "%s", "\n");

    fprintf(f, "%s", "empty_tp_512b");
    fprintf(f, "%s", ",");


    fprintf(f, "%d", input_l);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_input);
    fprintf(f, "%s", "\n");

    fprintf(f, "%s", "empty_tp_256b_2");
    fprintf(f, "%s", ",");

    fprintf(f, "%d", short_l_2);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_short_2);
    fprintf(f, "%s", "\n");

    fprintf(f, "%s", "empty_tp_1k_2");
    fprintf(f, "%s", ",");

    fprintf(f, "%d", long_l_2);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_long_2);
    fprintf(f, "%s", "\n");


    fprintf(f, "%s", "empty_tp_64b_2");
    fprintf(f, "%s", ",");

    fprintf(f, "%d", memory_l_2);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_memory_2);
    fprintf(f, "%s", "\n");

    fprintf(f, "%s", "empty_tp_2k_2");
    fprintf(f, "%s", ",");


    fprintf(f, "%d", file_l_2);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_file_2);
    fprintf(f, "%s", "\n");

    fprintf(f, "%s", "empty_tp_512b_2");
    fprintf(f, "%s", ",");


    fprintf(f, "%d", input_l_2);
    fprintf(f, "%s", ",");


    fprintf(f, "%d", count_input_2);
    fprintf(f, "%s", "\n");

    fclose(f);
}

int main(int argc, char *argv[])
{
    
    int x;
    
    // while (1){

        puts("Cost Aware Tracing Demo!\nPress Enter to continue...");

        /*
        * The following getchar() call is only placed here for the purpose
        * of this demonstration, to pause the application in order for
        * you to have time to list its tracepoints. It's not needed
        * otherwise.
        */
        getchar();

        printf("well this was fun ... ");

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
        

        int i;

        for (i = 0; i < 2; i++){
            short_loop_fun();
        } 

        for (i = 0; i < 2; i++){
            long_loop_fun();
        } 

        for (i = 0; i < 3; i++){
            memory_aloc_fun();
        } 

        for (i = 0; i < 2; i++){
            file_access_fun();
        } 

        // for (i = 0; i < 2; i++){
        //     block_input_fun();
        // } 


        
        write_results();
    // }

    return 0;
}
