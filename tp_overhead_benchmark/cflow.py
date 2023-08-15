from logging.config import stopListening
import os
import sys
from subprocess import call 

visited = [] # List to keep track of visited nodes.
queue = []     #Initialize a queue
call_stack = ["~"] * 50 

cflow_graph = {}        # what function is calling what functions                                       main -> all the functions directly called from main
tp_overhead = {}        # first is the tp and then the overhead and the number of calls                 [TP_NAME] -> [OVERALL_OVERHEAD] , [NUMBER_OF_CALLS]
function_tp_map = {}    # what tracepoints are inserted inside each function                            [FUNCTION_NAME] -> [TRACEPOINT_NAME]
DEPTH = 1
BUDGET = 40000


def create_function_tp_map():
    function_tp_map.clear()
    function_tp_map["short_loop_fun()"] = "empty_tp_256b"
    function_tp_map["long_loop_fun()"] = "empty_tp_1k"
    function_tp_map["file_access_fun()"] = "empty_tp_64b"
    function_tp_map["memory_aloc_fun()"] = "empty_tp_2k"
    function_tp_map["block_input_fun()"] = "empty_tp_512b"
    function_tp_map["short_loop_fun_2()"] = "empty_tp_256b_2"
    function_tp_map["long_loop_fun_2()"] = "empty_tp_1k_2"
    function_tp_map["file_access_fun_2()"] = "empty_tp_64b_2"
    function_tp_map["memory_aloc_fun_2()"] = "empty_tp_2k_2"
    function_tp_map["block_input_fun_2()"] = "empty_tp_512b_2"


def stop_lttng():
    stop = "lttng destroy"
    call (stop, shell= True)
  

def start_lttng(fun_list):

    enable_tp = ""

    for item in fun_list:
        if item in function_tp_map:
            enable_tp += function_tp_map[item] + ","

    start = "lttng create my-user-space-session"
    enable = ("lttng enable-event --userspace " + enable_tp)[:-1]
    run = "lttng start"

    call(start, shell=True)
    call(enable, shell=True)
    call(run, shell=True)

    return 

def create_graph(lst):

    for item in lst:
        indent = 0
        while indent < 50:
            if item.startswith("    "):
                item = item[4:]
                indent += 1
            if not item.startswith("    "):
                _info = item.find("<")
                if _info != -1:
                    item = item [:_info - 1]
                else:
                    # item = item[:-1]
                    # continue
                    break
                cflow_graph[item] = []
                if indent != 0:
                    cflow_graph[call_stack[indent -1]].append(item)    

                call_stack[indent] = item
                break
    return cflow_graph

def bfs (graph, node, layer):
    queue.append(node)
    l = 0
    while l <= layer:
        lenq = len(queue)
        for i in range(lenq):
            s = queue.pop(0)
            visited.append(s)
            print(s)

            for n in graph[s]:
                queue.append(n)
        l += 1
    return visited

def read_tp_overhead():
    tp_overhead.clear()
    file = open ("result_2.txt")
    lines = file.readlines()

    for l in lines:
        lst = l.split(",")
        tp_overhead[lst[0]] = [int(lst[1]) , int(lst[2][:-1])]

    return 


def read_cflow():
    file = open("cflow_result.txt" , "r")
    lines = file.readlines()
    graph = create_graph(lines)
    return graph
   
def calculate_current_overhead(overheads):
    overhead = 0

    for i in overheads.keys():
        overhead += int (overheads[i][0])

    return overhead


def main():

    # while True:

    # stop_lttng()
    create_function_tp_map()
    read_tp_overhead()
    current_overhead = calculate_current_overhead(tp_overhead)
    read_cflow()

    print (current_overhead , BUDGET)
    candidates = bfs(cflow_graph, "main()", DEPTH)
    print (candidates)
    start_lttng(candidates)
    


    # if current_overhead < BUDGET:
    #     DEPTH += 1
    #     candidates = bfs(cflow_graph, "main()", DEPTH)
    #     start_lttng(candidates)
        

    



main()