import json
import subprocess
import datetime
import os
import psutil
import time

with open('/mnt/sdc/qifan/leetcode/source/codeforce/qag.json', 'r') as file: ### Change to your own address
    datas = json.load(file)

current_date = datetime.date.today()

base_path = f'/mnt/sdc/qifan/leetcode/data_generator/datas/{current_date}' ### Change to your own address
os.makedirs(f"{base_path}/codeforce/data", exist_ok=True)
os.makedirs(f"{base_path}/codeforce/demo", exist_ok=True)

data_length = len(datas)
batch_size = 10
batch_limit = 100  
max_memory_usage = psutil.virtual_memory().total // 2
batch_time_limit = 60  
start = 0

print(f"Data length: {data_length}")

def run_script(st, ed):
    return subprocess.Popen(['python', 'data_generator_args_codeforce.py', '--st', str(st), '--ed', str(ed)])

for i in range(start, data_length, batch_size * batch_limit):
    st_ed_pairs = [
        (st, min(st + batch_size, data_length))
        for st in range(i, min(i + batch_size * batch_limit, data_length), batch_size)
    ]
    
    processes = []  
    start_time = time.time() 
    
    for st, ed in st_ed_pairs:
        while psutil.virtual_memory().used >= max_memory_usage:  
            print(f"Memory usage high, waiting...")
            time.sleep(1)
        
        print(f"Starting task for range: {st} - {ed}")
        p = run_script(st, ed)
        processes.append((p, st, ed)) 

    while processes:
        current_time = time.time()
        if current_time - start_time > batch_time_limit:  
            print("Time limit exceeded for current batch. Terminating remaining processes...")
            for p, st, ed in processes:
                if p.poll() is None:  
                    print(f"Terminating process for range: {st} - {ed}")
                    p.terminate()  
            break  
        
        for p, st, ed in processes[:]:  
            if p.poll() is not None: 
                print(f"Task for range: {st} - {ed} completed.")
                processes.remove((p, st, ed))  
        
        time.sleep(1)  

    for p, st, ed in processes:
        if p.poll() is None:  
            print(f"Force killing process for range: {st} - {ed}")
            p.kill()  