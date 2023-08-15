import re
import csv

# Define a function to parse the input files
def parse_file(filename1, filename2):
    with open(filename1) as f:
        lines = f.readlines()
    # Extract the function details from each line
    data = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue
        match = re.match(r'^([\d\.]+)\s+(ms|us|s|m)\s+([\d\.]+)\s+(ms|us|s|m)\s+([\d\.]+)\s+(ms|us|s|m)\s+(.*)$', line)
        if not match:
            continue
        self_avg, scale1, self_min, scale2, self_max, scale3, func_name = match.groups()
        # Convert the times to microseconds
        self_avg = convert_to_microseconds(self_avg, scale1)
        self_min = convert_to_microseconds(self_min, scale2)
        self_max = convert_to_microseconds(self_max, scale3)
        data.append({'name': func_name, 'self_avg': self_avg, 'self_min': self_min, 'self_max': self_max})

    with open (filename2) as f:
        lines = f.readlines()

        for line in lines [2:]:
            if not line:
                continue
            match = re.match(r'^\s*(\d+\.\d+)\s+(ms|us|s|m)\s+(\d+\.\d+)\s+(ms|us|s|m)\s+(\d+)\s+(.+)$', line)
            if not match:
                continue
            total_time, unit1, self_time, unit2, count, function_name = match.groups()
            self_time = convert_to_microseconds(self_time, unit2)
            for item in data:
                if item['name'] == function_name:
                    item ['self_time'] = self_time
                    item ['count'] = count
    
    return data

# Define a function to convert the times to microseconds
def convert_to_microseconds(value, scale):
    if scale == 'ms':
        return float(value) * 1000
    elif scale == 'us':
        return float(value)
    elif scale == 's':
        return float(value) * 1000000
    elif scale == 'm':
        return float(value) * 60000000

# Parse the two input files
data1 = parse_file('input1.txt','input2.txt')



# Write the merged data to a CSV file
with open('merged.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Function', 'Self Time', 'Count', 'Self Average', 'Self Min', 'Self Max'])
    for lst in data1:
        writer.writerow([lst['name'],lst['self_time'],lst['count'],lst['self_avg'],lst['self_min'],lst['self_max'], ])

print("Done")
