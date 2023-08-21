# Cost-Aware Instrumentation prototype

This repository contains the source code of the cost-aware instrumentation prototype 


## requirements for using the framework

For benchmarking user space trace points you can use `LTTng-UST`.

For profiling the application you can use `Uftrace` or `perf` or any other profiling tool that you can extract the execution time of each function. 

## How to run the framework

**Step 1:** 

Extract the static metrics from the application source code by running the command below:

`cd static_features/`

`python3 static_feature [PATH_TO_YOUR_PROJECT_DIRECTORY]`

The result of this command will be a JSON file containing all the static metrics extracted from the application. 

**Step2 :** 

Calculate the weighted sum of all the metrics by passing the result of previous step to `calculate_weighted_sum`.

The result of this step will be a csv file containing total_CPU, total_IO, total_network and the input and the output size of each function. 


**Step 3:** 

Run the application once normally to obtain the total execution time 

Run the application with full profiling enabled to extract the call frequency of each function 

This can be done using `uftrace record [YOUR_APPLICATION]` and then using `uftrace report`. 

**Step 4:**
Pass the result of step 2 and step 3 to the `problem_solver` script. 

In this script you need to change the total available budget based on your pereference. 

You can also change the generic algorithm values based on your problem. 

The result of this step will be a list of funciton that are suggested for initial instrumentation. 

