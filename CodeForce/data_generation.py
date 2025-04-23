import json
import os
from transformers import GenerationConfig, AutoModelForCausalLM, AutoTokenizer
import argparse
from vllm import LLM, SamplingParams
import jsonlines
import logging
from tqdm import tqdm
from pathlib import Path
import re
import pandas as pd
from examples import get_examples
import math
import json
import string
from modelscope.hub.file_download import model_file_download
from modelscope import snapshot_download


def generate_text_template(args, question, tokenizer):
    system_prompt = """You are an AI assistant responsible for providing assistance. You are provided with a problem and examples of the input. Your task is:
    (1) Write Python code to develop an input generator function capable of generating inputs for this problem. The input generator function should include a parameter that determines the maximum number of inputs it generates. The output of this function should be a list containing the generated inputs, with the length of each individual input not exceeding 10. Besides, any numbers contained in the input should not exceed 1000. Please provide the Python code without any additional explanation. Present your output in the following format: Input_generator: <your code>
    (2) Rewrite the code to eliminate manual input and encapsulate it within a function named 'solution'. The function should accept a string input as its parameter. Provide the output in the following format: Solution: <your code>.\n\n
    """

    content = []
    content.append("[Problem]:")
    content.append(data['problem'])
    llm_input = '\n'.join(content)

    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": llm_input}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    return text


def batch_data(data_list, batch_size=1):
    n = math.ceil(len(data_list) / batch_size)
    batch_data = []
    for i in range(n-1):
        start = i * batch_size
        end = (i+1)*batch_size
        batch_data.append(data_list[start:end])

    last_start = (n-1) * batch_size
    last_end = len(data_list)
    batch_data.append(data_list[last_start:last_end])
    return batch_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='******LLM inference on causal data******')
    parser.add_argument("--model_path", type=str, default="/hpc2hdd/home/jerryjiawenl/qifanzhang/models/qwen2.5-72b", help="loading paths of LLM") ### Change to your own address
    parser.add_argument("--batch_size", type=int, default=10000, help="Batch size for inference")
    parser.add_argument("--max_tokens", type=int, default=8000, help="Max tokens for inference")
    args = parser.parse_args()

    save_dir = f"/hpc2hdd/home/jerryjiawenl/qifanzhang/GraphCPT/codeforce/results"  ### Change to your own address
    Path(save_dir).mkdir(parents=True, exist_ok=True)


    results = 'results/'
    response_dict = {}
    input_texts = []

    sampling_params = SamplingParams(temperature=0.0, top_p=1, max_tokens=args.max_tokens) 
    print('sampleing =====', sampling_params)
    llm = LLM(model=args.model_path, tensor_parallel_size=8, gpu_memory_utilization=0.8)

    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    temp = 0

    input_texts = [] 
    original_datas = []
    results_dict = {}

    data_path = '/hpc2hdd/home/jerryjiawenl/qifanzhang/GraphCPT/codeforce/source/qa.json'  ### Change to your own address
    with open(data_path, 'r') as f:
        datas = json.load(f)
        
    datas=datas[60000:] ### You can adjust the data range
    print('loading datas')

    for data in datas:
        prompt = data['problem']

        template_text = generate_text_template(args, prompt, tokenizer=tokenize)
        input_texts.append(template_text)

    print(f'input_texts length is {len(input_texts)}\n')

    batch_inputs = batch_data(input_texts[temp:], batch_size=args.batch_size)

    print(f'total samples are: {len(input_texts)}')
    logging.info(f'total samples are: {len(input_texts)}')
    ind = temp
    file_counter = 1

    with jsonlines.open(f"{save_dir}/qag_60000_end.json", mode='w') as wf: ### Change the file name if needed
        for batch_input in tqdm(batch_inputs):
            completions = llm.generate(batch_input, sampling_params)
            
            for i, (problem,output) in enumerate(zip(batch_input, completions)):

                predict = output.outputs[0].text
                item = dict()
                item['problem'] = problem.split('[Problem]:')[1].strip().split('<|im_end|>')[0].strip()
                item['generator'] = predict
                wf.write(item)


    
