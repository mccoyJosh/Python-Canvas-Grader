import os, subprocess
from zipfile import ZipFile
from shutil import rmtree
import multiprocessing
import time
import json

config_file_name = 'config.json'

if not os.path.exists(config_file_name):
    print("ERROR: WHERE IS THE config.json FILE!!!")
    exit(0)

with open('config.json', 'r') as config_file:
    configs = json.load(config_file)
    input_size = configs['num_of_tests']
    delete_unzipped_dir = configs['delete_unzipped_dir']
    file_name_needs_to_contain = configs['only_run_files_containing_substring']
    print_result_outputs = configs['print_outputs']
    give_up_time_limit = configs['time_until_gives_up']
    zip_file_name = configs['zipped_submission_file']
    print_error_from_failed_code = configs['print_error_from_failed_code']


# Sets up main root file path(s)
current_directory = os.getcwd()
original_zip_file_path = current_directory + "/" + zip_file_name
exported_dir_name = current_directory + "/" + "submissions"


# Unzips zip file
with ZipFile(original_zip_file_path) as zip_object:
    zip_object.extractall(exported_dir_name)

# If the directory failed to unzip
if not os.path.exists(exported_dir_name):
    print("ERROR: SUBMISSION DIRECTORY DOES NOT EXIST")
    exit(0)

# format: ('name', [list_of_programming file], [list_of_other_files]) 
# I would use a dictionary but I'd rather keep the order of the students as they appear
si = []

# determines if student already exists in list
# if student was found, will return its index
# otherwise return -1
def student_index(student_name):
    for index, student in enumerate(si):
        if student[0] == student_name:
            return index
    return -1

# Gets all the file paths for python files

for subdir, dirs, files in os.walk(exported_dir_name):
    for file in files:
        filepath = subdir + os.sep + file
        split_file_name = file.split("_")
        student_name = split_file_name[0]
        student_position = student_index(student_name)
        if student_position == -1:
            student_position = len(si)
            si.append((student_name, [], []))
        

        if filepath.endswith(".py"):
            si[student_position][1].append(filepath)
        else:
            si[student_position][2].append(filepath)


# Gets students that should be ignored
ignore_student_list = []

with open("ignore_students.txt") as file:
    for line in file:
        ignore_student_list.append(line.strip())

code_result = ""

def run_python(code_file, input_file_obj):
    global code_result
    errfile = open('error.txt', 'w')
    try:
        code_result = str(subprocess.check_output(['python', code_file], stdin=input_file_obj, stderr=errfile))
    except subprocess.CalledProcessError as e:
        if print_error_from_failed_code:
            errfile.close()
            errfile = open('error.txt', 'r')
            print(f"Error executing code: {e}")
            print(errfile.read())
        else:
            print("Code failed!!")
    errfile.close()

# Goes through python files and 
for student in si:
    # Gets info on student
    student_name = student[0]
    prgm_paths = student[1]
    other_paths = student[2]
    dash_num = 120
    run_code = True
    print('\n')
    print('-' * dash_num)
    print(f"NAME: {student_name}")

    # Checks if we should run any of this students code!
    if student_name in ignore_student_list:
        run_code = False
    print("OTHER FILES:")
    for path in other_paths:
        print(f"\t{path}")
    print("PROGRAM FILES & RESULTS")

    # Goes to every filepath found ending with .py
    for code in prgm_paths:
        print(f'\t{code}')
        file_path_split = code.split(os.sep)
        filename = file_path_split[len(file_path_split) -1]

        # Ensures this code should be run AND has valid file name, if specified
        if run_code and (file_name_needs_to_contain in filename or file_name_needs_to_contain == ''):
            try:
                # Goes through all inputs
                for i in range(input_size):
                    current_input = f'inputs/input{i}.txt'
                    current_expected = f'outputs/output{i}.txt'
                    print(f"Using {current_input}")
                    with open(current_input) as input_file:
                        code_result = ""
                        # Runs process running code!
                        p = multiprocessing.Process(target=run_python, name="Python Test Run", args=(code, input_file))
                        p.run()
                        # Sleeps for a number of seconds
                        time.sleep(give_up_time_limit)

                        # If code is not finished in this time period, the process is terminated
                        # This should hopefully prevent infinite loops in student's code from 
                        # Making this run forever
                        if p.is_alive():
                            p.terminate()
                            print('WARNING: Test code took too long')
                        else:
                            if print_result_outputs:
                                formatted_results = code_result.replace("\\n", '\n\t')
                                print(f"RESULTS: \n\t", formatted_results)
                            # If the process finished, we just check to see if we received a valid output
                            with open(current_expected) as output_file:
                                for line in output_file:
                                    fixed_line = line.strip()
                                    print(f'TEST FOR {fixed_line}: ', end='')
                                    if fixed_line in code_result:
                                        print('✅')
                                    else:
                                        print('❌')
            except FileNotFoundError as e:
                print(f'Could not find file (probably I/O files) {e}')
        else:
            print("CODE NOT RAN")



# Deletes unzipped files at end
if delete_unzipped_dir:
    rmtree(exported_dir_name)
