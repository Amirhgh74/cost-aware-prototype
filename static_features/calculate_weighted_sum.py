import json
import csv

# Read JSON data
with open('result_httpd.json', 'r') as f:
    data = json.load(f)



# Read CSV weights
weights = {}
with open('feature_weight.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # skip the header row
    for row in csv_reader:
        feature = row[0]
        weights[feature] = {}
        weights[feature]['cpu'] = float(row[1])
        weights[feature]['io'] = float(row[2])
        weights[feature]['network'] = float(row[3])

result = []

# Calculate weighted sums for each file element
for file_elem in data:
    file_name = file_elem['file']
    total_cpu = 0
    total_io = 0
    total_network = 0

    # Calculate weighted sum for each function element
    for func_elem in file_elem['functions']:
        name = func_elem["name"]
        num_loop = func_elem['number_of_loops']
        input_size = func_elem['input_size']
        output_size = func_elem['return_size']
        num_nested_loop = func_elem['number_of_nested_loops']
        is_recursive = 1 if func_elem['is_recursive'] else 0
        num_branch = func_elem['number_of_branches']['number_of_branch_total']
        using_thread = func_elem['extended features']['number_of_threads'] 
        fork_process = func_elem['extended features']['number_of_forks'] 
        num_exception = func_elem['extended features']['number_of_exception_handling']
        num_lock = func_elem['extended features']['number_of_lock_access']
        file_access = func_elem['extended features']['number_of_file_access'] 
        input_wait = func_elem['extended features']['number_of_input_wait'] 
        syscall = func_elem['extended features']['number_of_syscalls'] 
        socket = func_elem['extended features']['number_of_sockets'] 

        total_cpu += (num_loop * weights['num_loop']['cpu']
                      + num_nested_loop * weights['num_nested_loop']['cpu']
                      + is_recursive * weights['is_recursive']['cpu']
                      + num_branch * weights['num_branch']['cpu']
                      + using_thread * weights['using_thread']['cpu']
                      + fork_process * weights['fork_process']['cpu']
                      + num_exception * weights['num_exception']['cpu']
                      + num_lock * weights['num_lock']['cpu']
                      + file_access * weights['file_access']['cpu']
                      + input_wait * weights['input_wait']['cpu']
                      + syscall * weights['syscall']['cpu']
                      + socket * weights['socket']['cpu'])

        total_io += (num_loop * weights['num_loop']['io']
                     + num_nested_loop * weights['num_nested_loop']['io']
                     + is_recursive * weights['is_recursive']['io']
                     + num_branch * weights['num_branch']['io']
                     + using_thread * weights['using_thread']['io']
                     + fork_process * weights['fork_process']['io']
                     + num_exception * weights['num_exception']['io']
                     + num_lock * weights['num_lock']['io']
                     + file_access * weights['file_access']['io']
                     + input_wait * weights['input_wait']['io']
                     + syscall * weights['syscall']['io']
                     + socket * weights['socket']['io'])

        total_network += (num_loop * weights['num_loop']['network']
                        + num_nested_loop * weights['num_nested_loop']['network']
                        + is_recursive * weights['is_recursive']['network']
                        + num_branch * weights['num_branch']['network']
                        + using_thread * weights['using_thread']['network']
                        + fork_process * weights['fork_process']['network']
                        + num_exception * weights['num_exception']['network']
                        + num_lock * weights['num_lock']['network']
                        + file_access * weights['file_access']['network']
                        + input_wait * weights['input_wait']['network']
                        + syscall * weights['syscall']['network']
                        + socket * weights['socket']['network'])

        result.append([name, total_cpu, total_io, total_network, input_size, output_size])

        
        # print ("function : " + name + " cpu weight sum : " + str(total_cpu) + "  io weight sum : " + str(total_io) + "    network weight sum : " + str(total_network))

# Sort the scores based on the range score in descending order
result.sort(key=lambda x: x[3], reverse=True)


# print (result)
# Output filename
output_filename = 'weighted_sum_httpd.csv'

# Write the data to the CSV file
with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    # writer.writerow(['Name', 'Total_CPU', 'Total_IO', 'Total_Network', 'Input_Size', 'Output_Size'])
    writer.writerow(['Name','Total_Network'])

    
    # Write the function data
    # writer.writerows([result[0], result[3]])

    for i in result:
        writer.writerow([i[0], i[3]])
