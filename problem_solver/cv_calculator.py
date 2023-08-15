import sys
from pathlib import Path
import os 
import csv


scale_to_multiplier = {
    "us": 1,
    "ms": 1000,
    "s": 1000000,
    "m": 60000000,
}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cv_calulator.py <input_directory>")
        exit(1)
    
    input_directory = sys.argv[1]
    if not Path(input_directory).is_dir():
        print("Input directory does not exist")
        exit(1)

    result = {}
    files_address = []
    scores = []

    for subdir, dirs, files in os.walk(input_directory):
        for file in files:
            files_address.append(os.path.join(subdir, file))   

    for p in files_address:
        if p.endswith(".txt"):
            file_path = Path(p)
            print (p)

            # Read the file and extract the relevant data
            with open(file_path, "r") as file:
                lines = file.readlines()[2:]  # Skip the header rows

            # Process each line and calculate the score
            for line in lines:
                parts = line.split()

                function_name = parts[-1]
                avg_time = float(parts[0]) * scale_to_multiplier[parts[1]]
                min_time = float(parts[2]) * scale_to_multiplier[parts[3]]
                max_time = float(parts[4]) * scale_to_multiplier[parts[5]]

                range = (max_time - min_time) 

                if function_name in result:
                    result[function_name].append((range, avg_time))
                else:
                    result[function_name] = [(range, avg_time)]


    for i in result.keys():
        lst = result[i]

        range = 0 
        mean = 0 
        count = 0

        for item in lst:
            range += float (item[0])
            mean += float (item[1])
            count += 1
        
        overall_range = range / count
        overall_mean = mean / count

        cv_score = overall_range / overall_mean

        scores.append((i , cv_score))



    # Sort the scores based on the range score in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Print the list of functions and their scores
    for function, score in scores:
        print(f"{function}: {score:.2f}")


    # Write the merged data to a CSV file
    with open('CV_score_httpd.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Function', 'score'])
        for function, score in scores:
            writer.writerow([function, score])

    print("Done")
