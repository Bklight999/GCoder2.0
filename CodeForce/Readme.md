# Source
Necessary files **`qa.json`** and **`qag_60000_end.json`** are provided in [GoogleDrive](https://drive.google.com/drive/folders/1-eMPBr7IWN9g5TpDkPnRzX40Ob-CqMsi/).

# Usage
The group of codes is designed to **generate a number of problem-answer pairs** for ([Codeforces](https://codeforces.com/)). The problem includes the following components: the original problem (comprising the Problem definition, input and output specifications, sample input and output, and notes), the input to the problem, and the code for solving the problem.  

The answer includes the following: a step-by-step code execution trace that records the changes in intermediate variables and the final answer to the problem.  

Here is an example of a problem-answer pair:

```
<Problem>
Johny likes numbers *n* and *k* very much. Now Johny wants to find the smallest integer *x* greater than *n*, so it is divisible by the number *k*.

Input Specification:
The only line contains two integers *n* and *k* (1<=≤<=*n*,<=*k*<=≤<=109).

Output Specification:
Print the smallest integer *x*<=&gt;<=*n*, so it is divisible by the number *k*.

Demo Input:
['5 3\n', '25 13\n', '26 13\n']

Demo Output:
['6\n', '26\n', '39\n']

Note:
none
<Problem>

And the input of the problem:
<Input>
484 250
<Input>

Predict the output of the problem based on the following code:

<Code>
def solution(input_str):
    n, k = map(int, input_str.strip().split())
    x = n + 1
    while x % k != 0:
        x += 1
    return f"{x}\n"
<Code>

---------------

Trace: n : 484; k : 250
n : 484; k : 250; x : 485
n : 484; k : 250; x : 485
n : 484; k : 250; x : 486
n : 484; k : 250; x : 486
n : 484; k : 250; x : 487
n : 484; k : 250; x : 487
n : 484; k : 250; x : 488
n : 484; k : 250; x : 488
n : 484; k : 250; x : 489
n : 484; k : 250; x : 489
n : 484; k : 250; x : 490
n : 484; k : 250; x : 490
n : 484; k : 250; x : 491
n : 484; k : 250; x : 491
n : 484; k : 250; x : 492
n : 484; k : 250; x : 492
n : 484; k : 250; x : 493
n : 484; k : 250; x : 493
n : 484; k : 250; x : 494
n : 484; k : 250; x : 494
n : 484; k : 250; x : 495
n : 484; k : 250; x : 495
n : 484; k : 250; x : 496
n : 484; k : 250; x : 496
n : 484; k : 250; x : 497
n : 484; k : 250; x : 497
n : 484; k : 250; x : 498
n : 484; k : 250; x : 498
n : 484; k : 250; x : 499
n : 484; k : 250; x : 499
n : 484; k : 250; x : 500
n : 484; k : 250; x : 500
According to the trace, the answer is 500.
```

---

# How to Run the Codes

## Step 1: Generate Input Generator and Solution Code for Each Problem Using LLMs

1. **Modify Addresses**  
   Open the file **`data_generation.py`** and modify the required addresses (marked as `### Change to your own address`). Ensure that the necessary data source **`qa.json`** is available in the specified folder.

2. **Run the Script**  
   Execute the following command to generate the input generator and solution code:
   ```bash
   python data_generation.py
   ```

3. **Output**  
   The output of the script will be a JSON file containing:  
   - **The code for solving the problem**  
   - **The input generator**  

   A demo output file, **`qag_60000_end.json`**, is provided for reference.

4. **Note**  
   The quality of the generated code depends on the performance of the LLMs. **Better LLMs produce more executable and reliable code, which directly impacts the number of final problem-answer pairs.**

---

## Step 2: Generate Code Execution Trace for Each Problem Based on the Input Generator and Solution Code

1. **Modify Addresses**  
   Open the files **`data_generator_args_codeforce.py`** and **`run_codeforce.py`**, and modify the required addresses (marked as `### Change to your own address`).

2. **Run the Script**  
   Execute the following command:
   ```bash
   python run_codeforce.py
   ```

3. **Output**  
   The program will generate a folder named **`codeforce`**, which contains two subfolders:
   - **`data`**: This folder contains the batch-generated data.  
   - **`demo`**: This folder contains partial data demos from each batch.

4. **Batch Processing**  
   - Data generation is performed in batches to balance speed and memory usage.  
   - Serial data generation is slow, while parallel generation can place significant demand on system memory. Using batches optimizes this process.
   - Adjust the batch size and the total number of batches in **`data_generator_args_codeforce.py`** to prevent memory overflow of your device.

