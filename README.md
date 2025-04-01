# Python Canvas Grader

<h4 style="color:red">This project will execute code provided by students; if you suspect the code to be malicious, obviously do not run it. To stay safe, it would be wise to run this in a virtual machine!! See Run docker container section!</h4>

This small program is used to test simple python programs against a number of inputs and
see if they result in the correct outputs. 

The inputs and outputs are both written in corresponding files,
so if you expect a piece of code to take 2 inputs and then provide a newline,
your input file would look like this:

input0.txt
```
100
50


```

and if the code adds these and prints out the average and sum, your output file would look like this:

output0.txt
```
75
150
```

Notice that the corresponding input/outputs have the same integer right before the extension name;
this is to make sure the program knows they are corresponding files.

The way the program tests for these outputs is by simply checking the resulting output for the substrings
provided in output#.txt. This has the drawback of potentially giving a false positive test if, perhaps, 
a student said the average = 150 and the sum = 75 in the last example. Since both outputs are technically
found in the resulting output, we are 'good'; but we know that technically the code is in fact wrong.

If your piece of code expects a single outputting value, then this is perfect solution.
Otherwise, beware!

# config.json

There are a few things to configure for the project if need be:

### num_of_tests
This integer is going to tell the system how many of the input/output files there
are that needs to be ran and tested.

By default, it uses 3, but if you need more or less, just change this number.
There is no check in the code for the value inputted here, so
if you put in 4 and provide it 3 files, it would look for the fourth file and fail.

### delete_unzipped_dir

This boolean is going to tell the program whether or not you want the unzipped
directory created in this process deleted at the end of running this program.

If, for instance, you want to keep the unzipped file to take a look
at the code written, you could by setting this to `false`.

It is `true` by default.

### only_run_files_containing_substring

This will provide an extra check on to what file to run if there
are perhaps multiple python files submitted by the student.

By default it is set to `""` (an empty string), which 
indicated to the program that ALL found python files should be
ran against the provided inputs/outputs.

If you only wanted to run the tests against files perhaps containing
the word 'sum' in it, you would simply change this empty string to `"sum"`.
Also note this is case sensitive!!

### print_outputs
If you want to see the exact outputs resulting from your tests, set this to
`true`.

It is set to `false` by default, so you just see whether or not it failed/passed
each test.

### time_until_gives_up
This floating point value determine how long each individual test will run (in seconds) until the process is terminated.

This is in place to ensure no infinite loops keep the program running forever.

If you have a poorly running device or expect the student's code to run for a longer period of time, change this to a more preferable time.

### zipped_submission_file

This string tells the program the file name for the zip file containing all the students code.
Canvas SHOULD export this file as `submissions.zip`, but if that is not the case, you can always rename the
file or change the expecting zip file name in the config.json file

# Submission.zip

For assignment on canvas, there should be an option to 
> Download Submissions

This should provide you a file called 'submissions.zip'.
Place this file inside of the working directory of this project.
<h4 style="color:red">THE CODE WILL NOT WORK IF YOU DO NOT PROVIDE IT THIS submissions.zip FILE!!!</h4>

If you renamed the file, there is an option in config.json to change the expecting zip file.

# ignore_students.txt

If there are any students which code you want to skip in your test run, you
can put their name here. This name needs to match the name found on the file!

# Run docker container

Obviously, make sure you have docker installed.
Also, make sure your submissions.zip file, along with the expected inputs and outputs and configs are all set previous
to building the grader!!!

Build this image:
```
docker build -t canvas_grader .
```


Rebuild image (and prune dangling):
```
docker build -t canvas_grader . && docker image prune -f
```


Run the container:
```
docker run -it --rm canvas_grader
```

# NOTE: This was only tested on linux, so, if you try running the code on another operating system, I cannot guarantee it works correctly