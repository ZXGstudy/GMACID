import pandas as pd
import random
import os

def read_fasta(file_path):
    sequences = []
    with open(file_path, 'r') as file:
        entries = file.read().split('>')[1:]
        for entry in entries:
            lines = entry.split('\n')
            sequence = ''.join(lines[1:])  # 获取序列并连接
            sequences.append(sequence)
    return sequences

def random_sort_samples(input_files, num_samples=2000):
    samples = []
    all_sequences = []

    # 读取所有文件中的序列
    for file in input_files:
        sequences = read_fasta(file)
        if len(sequences) < 100:
            print(f"Skipping file {file}: Not enough sequences.")
            continue
        all_sequences.extend([(file, seq) for seq in sequences])

    # 无放回抽样
    for _ in range(num_samples):
        if len(all_sequences) < 100:
            print("Not enough sequences left for another sample.")
            break
        
        sampled_indices = random.sample(range(len(all_sequences)), 100)
        sampled_sequences = [all_sequences[i] for i in sampled_indices]

        for i in sorted(sampled_indices, reverse=True):
            del all_sequences[i]

        file_name = os.path.basename(sampled_sequences[0][0])
        patient_value = file_name.split('_')[0]  # 提取第一个下划线前面的内容

        annotated_sample = f"### Instruction:\nAnnotate the following sequence.\n\n### Input:\n{' '.join(seq[1] for seq in sampled_sequences)}\n\n### Response:"
        samples.append((annotated_sample, '', patient_value))

    return samples

def write_excel(samples, output_file, response_dict):
    data = {'Annotated Sequence': [sample[0] for sample in samples], 
            'Output': [response_dict.get(sample[2], '') for sample in samples], 
            'Patient': [sample[2] for sample in samples]}
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == '__main__':
    input_dir = '/home/zxg/GMACID/cutkmer20/seqtk0.02M/test'
    output_file = '/home/zxg/GMACID/cutkmer20/seqtk0.02M/test.xlsx'
    sample_csv = '/home/zxg/GMACID/cutkmer20/seqtk0.02M/sample.csv'

    # 获取指定目录下的所有文件
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # 随机抽取并排序样本
    sampled_samples = random_sort_samples(input_files)

    # 读取 sample.csv 文件并创建 response 字典
    sample_df = pd.read_csv(sample_csv, dtype=str).fillna('')
    response_dict = {row['SampleID'].strip(): row['Response'].strip() for index, row in sample_df.iterrows()}

    # 写入Excel文件
    write_excel(sampled_samples, output_file, response_dict)
