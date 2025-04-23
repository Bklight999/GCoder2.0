import sys
import networkx as nx
import random
import numpy as np
from collections import deque
import json
from tqdm import tqdm
import signal
import threading
import datetime
import argparse




with open('/mnt/sdc/qifan/leetcode/source/codeforce/qag.json','r') as f: ### Change to your own address
    datas = json.load(f)

trace_list=[]
demo_list = []
valid_problem = 0
st = 0
ed = 10
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--st', type=int, default=0, help='start index')
parser.add_argument('--ed', type=int, default=10, help='end index')
args = parser.parse_args()

st = args.st
ed = args.ed

for i in tqdm(range(st, ed)):
    cnt = 0
    try:
        problem = datas[str(i)]['problem']
        generator = datas[str(i)]['generator'].split('Input_generator:')[1].split('```python')[1].split('```')[0]
        code = datas[str(i)]['generator'].split('Solution:')[1].split('```python')[1].split('```')[0]
        # if 'return' not in solution:
        #     continue
        
        exec(generator)
        exec(code)
        
        input_list = input_generator(30) ### Generate 30 inputs, you can change this number
        for input in input_list:
            try:
                trace_data = []
                parameter = {}
                initial_variables = {}
                max_depth = 0  
                recursion_detected = False  

                def trace_calls(frame, event, arg):
                    global parameter
                    global initial_variables
                    global max_depth
                    global recursion_detected

                    if event != 'line': 
                        return trace_calls

                    co = frame.f_code
                    variables = frame.f_locals

    
                    func_args = co.co_varnames[:co.co_argcount]
                    parameter = func_args


                    if 'self' in variables:
                        variables.pop('self')

         
                    if not initial_variables:
                        initial_variables = variables.copy()

                    changed_variables = {
                        k: v for k, v in variables.items()
                        if k not in initial_variables or initial_variables[k] != v
                    }


                    if changed_variables:
                        trace_data.append("; ".join(f"{k} : {v}" for k, v in changed_variables.items() if isinstance(v, (int, float, str, list, dict, tuple, set, np.ndarray, deque))))

                def timeout_handler():
                    sys.settrace(None) 
                    raise TimeoutError("Function execution exceeded time limit.")

                try:
                    timer = threading.Timer(0.5, timeout_handler) 
                    timer.start() 

                    sys.settrace(trace_calls)  
                    try:
                        ans = solution(input)
                        
                    except TimeoutError:
                        print("Function execution timed out.")  
                        ans = None  
                    finally:
                        sys.settrace(None)  
                        timer.cancel()  

                    trace_data = "\n".join(trace_data)
                except:
                    sys.settrace(None)
                    trace_data = "\n".join(trace_data)
                    continue

                trace_data = trace_data + "\nAccording to the trace, the answer is {}".format(ans)

                num_lines = len(trace_data.split('\n'))
                if num_lines > 50 or num_lines < 5:
                    continue

                trace_list.append({
                    "id": len(trace_list),
                    "prompt": "Given the problem:\n\n<Problem>"+problem.split('Problem Description:')[1]+"<Problem>\n\nAnd the input of the problem:\n<Input>\n{}<Input>\n\nPredict the output of the problem based on the following code:\n\n<Code>{}<Code>\n".format(input,code),
                    "code": code,
                    "input_generator": generator,
                    "input": input,
                    "answer": ans,
                    "trace": trace_data,
                })
                cnt += 1
                if cnt == 1:
                    demo_list.append({
                        "prompt": "Given the problem:\n\n<Problem>"+problem.split('Problem Description:')[1]+"\n<Problem>\n\nAnd the input of the problem:\n<Input>\n{}<Input>\n\nPredict the output of the problem based on the following code:\n\n<Code>{}<Code>\n".format(input,code),
                        "trace": trace_data,
                    })
                if cnt == 5:
                    break
                #print(trace_data)
            except:
                continue
        if cnt > 0:
            valid_problem += 1
    except:
        continue

current_date = datetime.date.today()
with open(f'/mnt/sdc/qifan/leetcode/data_generator/datas/{current_date}/codeforce_2/data/trace_{st}_{ed}.json','w') as f: ###Change to your own address
    json.dump(trace_list, f)

with open(f'/mnt/sdc/qifan/leetcode/data_generator/datas/{current_date}/codeforce_2/demo/demo_{st}_{ed}.txt','w') as f: ###Change to your own address
    for i in range(len(demo_list)):
        f.write('Prompt: '+demo_list[i]['prompt']+'\n\n')
        f.write('Trace: '+demo_list[i]['trace']+'\n\n')
        f.write('------------------------------------\n\n')
print(valid_problem)
print(len(trace_list))


