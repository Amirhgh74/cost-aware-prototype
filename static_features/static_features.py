import json
import re
import sys
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
import ctypes
import os 

from utils import get_element_texts

# Create a dictionary to store variable types and sizes
variable_sizes = {
    'byte': ctypes.sizeof(ctypes.c_byte),
    'BYTE': ctypes.sizeof(ctypes.c_byte),
    'ubyte': ctypes.sizeof(ctypes.c_ubyte),
    'UBYTE': ctypes.sizeof(ctypes.c_ubyte),
    'char': ctypes.sizeof(ctypes.c_char),
    'int': ctypes.sizeof(ctypes.c_int),
    'float': ctypes.sizeof(ctypes.c_float),
    'double': ctypes.sizeof(ctypes.c_double),
    'short': ctypes.sizeof(ctypes.c_short),
    'long': ctypes.sizeof(ctypes.c_long),
    'long long': ctypes.sizeof(ctypes.c_longlong),
    'unsigned char': ctypes.sizeof(ctypes.c_ubyte),
    'unsigned int': ctypes.sizeof(ctypes.c_uint),
    'unsigned short': ctypes.sizeof(ctypes.c_ushort),
    'unsigned long': ctypes.sizeof(ctypes.c_ulong),
    'unsigned long long': ctypes.sizeof(ctypes.c_ulonglong),
    'unsigned': ctypes.sizeof(ctypes.c_int),
    'void': ctypes.sizeof(ctypes.c_void_p),
    'char pointer': ctypes.sizeof(ctypes.POINTER(ctypes.c_char)),
    'int pointer': ctypes.sizeof(ctypes.POINTER(ctypes.c_int)),
    'float pointer': ctypes.sizeof(ctypes.POINTER(ctypes.c_float)),
    'void pointer' : ctypes.sizeof(ctypes.POINTER(ctypes.c_void_p)),

    'int8_t' : ctypes.sizeof(ctypes.c_int8),
    'int16_t' : ctypes.sizeof(ctypes.c_int16),
    'int32_t' : ctypes.sizeof(ctypes.c_int32),
    'int64_t' : ctypes.sizeof(ctypes.c_int64),
    'uint8_t' : ctypes.sizeof(ctypes.c_uint8),
    'uint16_t' : ctypes.sizeof(ctypes.c_uint16),
    'uint32_t' : ctypes.sizeof(ctypes.c_uint32),
    'uint64_t' : ctypes.sizeof(ctypes.c_uint64),
    'wchar' : ctypes.sizeof(ctypes.c_wchar),
    'bool' : ctypes.sizeof(ctypes.c_bool)
    # Add more pointer types as needed
}

custom_variables = {}

def parse_param(input_text):
    if "*" in input_text: # if pointer 
        input_text = input_text[:-1] + " pointer"
        if input_text not in variable_sizes:
            return variable_sizes['int pointer']
        else:
            return variable_sizes[input_text]
        
    else:
        pattern = r'(\w+)\s*\[\s*(\d*)\s*\]'
        match = re.match(pattern, input_text)
        if match: # if list
            variable = match.group(1).strip()
            count = int(match.group(2)) if match.group(2) else 0
            size = 0 
            if size not in variable_sizes:
                size = int (variable_sizes['double'])
            else:
                size = int (variable_sizes[variable])
            return count * size
        elif "struct" in input_text: # if struct
            if input_text not in custom_variables:
                return 10
            return custom_variables[input_text]
        else:
            if input_text not in variable_sizes:
                return variable_sizes['int']
            return variable_sizes[input_text]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analysis.py <input_directory>")
        exit(1)

    input_directory = sys.argv[1]
    if not Path(input_directory).is_dir():
        print("Input directory does not exist")
        exit(1)

    result = []
    files_address = []

    for subdir, dirs, files in os.walk(input_directory):
        for file in files:
            files_address.append(os.path.join(subdir, file))
           

    # Loop through all files in the input directory
    for p in files_address:
        if p.endswith(('.cxx' , '.cc' , '.c')):
            file_path = Path(p)
            print(file_path)
            process = subprocess.run(['srcml', file_path], capture_output=True) # Run srcml on file
            xml = process.stdout.decode('utf-8')
            xml = re.sub('xmlns="[^"]+"', '', xml, count=1) # Remove namespace

            root = ET.fromstring(xml)
            includes = []

            # Save all the included libraries
            for include in root.findall('{http://www.srcML.org/srcML/cpp}include/{http://www.srcML.org/srcML/cpp}file'):
                includes.append(get_element_texts(include)[1:-1])
            
            struct_dict = {}
            # get all the struct definitions in the file
            struct_list = root.findall('struct')
            if struct_list:
                for struct in struct_list:
                    name = get_element_texts(struct.find('name'))
                    size  = 0
                    for item in struct.findall('.//decl_stmt'):
                        size_tmp = get_element_texts(item.find('.//type'))
                        # print(size_tmp)/
                        size += parse_param(size_tmp)
                    struct_dict[name] = size
                    full_name = "struct " + name
                    custom_variables[full_name] = size
           
            



            # Get root functions and print them
            for function in root.findall('function'):
                # Find all loops and nested loops
                loops = []
                loops.extend(function.findall('.//for') + function.findall('.//while') + function.findall('.//do'))

                function_name = get_element_texts(function.find('name'))

                input_param = {}
                total_param_size = 0
                for param_list in function.findall('parameter_list'):
                    if(len(param_list) == 0):
                        input_param['void'] = [0]
                    else:
                        for param in param_list:
                            type = get_element_texts(param.find('.//type/name'))
                            modifier = get_element_texts(param.find('.//type/modifier'))
                            index = get_element_texts(param.find('.//name/index'))

                            input_name = (type + modifier + index).strip()
                            
                            if '...' not in input_name:
                                input_size = parse_param(input_name)
                            total_param_size += input_size
                            
                            if input_name not in input_param.keys():
                                input_param[input_name] = [input_size]
                            else:
                                input_param[input_name].append(input_size)
                


                ret_name = get_element_texts(function.find('.//type/name'))
                ret_modifier = get_element_texts(function.find('.//type/modifier'))
                return_type = (ret_name + ret_modifier).strip()
                return_size = 0 if return_type == 'void' else parse_param(return_type)
                
                # Find the number of semi-colons in the function
                number_of_semicolons = ''.join(function.itertext()).count(';')

                number_of_nested_loops = 0
                for loop in loops:
                    nested_loops = []
                    nested_loops.extend(loop.findall('.//for') + loop.findall('.//while') + loop.findall('.//do'))
                    number_of_nested_loops += len(nested_loops)

                    if loop.find('control') is not None:
                        number_of_semicolons -= ''.join(loop.find('control').itertext()).count(';')

                number_of_loops = len(loops)

                # Find number of calls inside the function
                number_of_calls = len(function.findall('.//call'))

                # Find if uses Exception Handling
                number_of_exception_handling = len(function.findall('.//goto'))

                # analysis of all the calls in the function
                number_of_lock_access = 0
                opens_file = False
                has_input_wait = False
                is_using_threads = False
                fork_new_process = False
                is_using_syscall = False
                number_of_threads = 0
                number_of_forks = 0
                number_of_syscalls = 0
                number_of_locks = 0
                number_of_file_access = 0
                number_of_input_wait = 0
                number_of_socket = 0

                for call in function.findall('.//call'):

                    # Find number of File access 
                    file_definition = False
                    for dec in function.findall('.//decl_stmt/decl/type'):
                        if get_element_texts(dec.find('name')) == "FILE" and get_element_texts(dec.find('modifier')) == '*':
                            file_definition = True


                    for name in call.findall("name"):
                        if get_element_texts(name) == "pthread_create" and "pthread.h" in includes:
                            number_of_threads += 1

                        if get_element_texts(name) == "fork" and "stdio.h" in includes:
                            number_of_forks += 1

                        if get_element_texts(name) == "syscall" and "sys/syscall.h" in includes:
                            number_of_syscalls += 1

                        if get_element_texts(name) == "connect" and "sys/socket.h" in includes:
                            number_of_socket += 1

                        if get_element_texts(name) == "pthread_mutex_lock" and "pthread.h" in includes:
                            number_of_locks += 1

                        if get_element_texts(name) == "sem_wait" and "semaphore.h" in includes:
                            number_of_locks += 1

                        if get_element_texts(name) == "fopen" or get_element_texts(name) == "afopen":
                            if file_definition:
                                number_of_file_access += 1
                        

                        if get_element_texts(name) == "scanf" or get_element_texts(name) == "getchar" or get_element_texts(name) == "gets":
                            number_of_input_wait += 1
                        
                    # Find if function is using multithreading (should include pthread.h)
                    if get_element_texts(call.find('name')) == "pthread_create" and "pthread.h" in includes :
                        is_using_threads = True

                    if get_element_texts(call.find('name')) == "fork" and "stdio.h" in includes :
                        fork_new_process = True

                    # only explicit syscall usage is captured 
                    if get_element_texts(call.find('name')) == "syscall" and "sys/syscall.h" in includes :
                        is_using_syscall = True
                    
                    # Find number of critical section access in the function
                    if get_element_texts(call.find('name')) == "pthread_mutex_lock" and "pthread.h" in includes :
                        number_of_lock_access += 1
                    if get_element_texts(call.find('name')) == "sem_wait" and "semaphore.h" in includes :
                        number_of_lock_access += 1

                    if get_element_texts(call.find('name')) == "scanf" \
                        or get_element_texts(call.find('name')) == "getchar" \
                        or get_element_texts(call.find('name')) == "gets":
                        has_input_wait = True

                                
                # Find number of blocks
                number_of_blocks = len(function.findall('.//block'))

                # Check if function is recursive
                is_recursive = False
                for call in function.findall('.//call'):
                    if get_element_texts(call.find('name')) == function_name.split(')')[0]:
                        is_recursive = True
                        break

                # Number of statements individually
                number_of_expression_statements = len(function.findall('.//expr_stmt'))
                number_of_declaration_statements = len(function.findall('.//decl_stmt'))
                number_of_empty_statements = len(function.findall('.//empty_stmt'))

                # Number of branches
                number_of_if = len(function.findall('.//if') + function.findall('.//else'))
                number_of_switch = len(function.findall('.//switch'))
                number_of_preprocessor_if = len(function.findall('.//{http://www.srcML.org/srcML/cpp}if') + function.findall('.//{http://www.srcML.org/srcML/cpp}else') + function.findall('.//{http://www.srcML.org/srcML/cpp}elif'))

                # Check if file is already in result
                if not any(x.get('file', '&') == str(p).replace(input_directory + '/', '') for x in result):
                    result.append({
                        'file': str(p).replace(input_directory + '/', ''),
                        'struct': struct_dict,
                        'functions': []
                    })

                for item in result:
                    if item['file'] == str(p).replace(input_directory + '/', ''):
                        item['functions'].append({
                            'name': function_name,
                            'input_param': input_param,
                            'input_size': total_param_size,
                            'return_type': return_type,
                            'return_size' : return_size,
                            'line_of_codes': number_of_semicolons + number_of_blocks - 1, # -1 because of the function entire block
                            'number_of_loops': number_of_loops,
                            'number_of_nested_loops': number_of_nested_loops,
                            'is_recursive': is_recursive,
                            'number_of_branches': {
                                'number_of_if': number_of_if,
                                'number_of_switch': number_of_switch,
                                'number_of_branch_total' : number_of_if + number_of_switch
                            },
                            'extended features':{
                                'number_of_threads': number_of_threads,
                                'number_of_forks': number_of_forks,
                                'number_of_exception_handling': number_of_exception_handling,
                                'number_of_lock_access' : number_of_locks,
                                'number_of_file_access' : number_of_file_access,
                                'number_of_input_wait' : number_of_input_wait,
                                'number_of_syscalls' : number_of_syscalls,
                                'number_of_sockets' : number_of_socket
                            }
                            
                        })

    # Write result to file
    with open('result_httpd.json', 'w') as f:
        json.dump(result, f, indent=4)
