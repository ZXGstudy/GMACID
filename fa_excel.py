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

def sort_sequence(sequence):
    return ''.join(sorted(sequence))

def random_sort_samples(input_files, num_samples=200):
    samples = []

    for file in input_files:
        sequences = read_fasta(file)
        num_sequences = len(sequences)
        if num_sequences < 100:
            print(f"Skipping file {file}: Not enough sequences.")
            continue

        # 随机抽取100条序列并按ACGT次序排序
        sampled_indices = random.sample(range(num_sequences), 100)
        sampled_sequences = [sequences[i] for i in sampled_indices]
        sorted_sequences = [sort_sequence(seq) for seq in sampled_sequences]

        # 提取文件名中的信息作为patient列的值
        file_name = os.path.basename(file)
        patient_value = file_name # 提取第二个下划线前面的内容

        # 将排序后的样本加入样本列表，前后添加标识符
        annotated_sample = f"### Instruction:\nAnnotate the following sequence.\n\n### Input:\n{' '.join(sorted_sequences)}\n\n### Response:"
        samples.append((annotated_sample, '', patient_value))

    # 随机抽取num_samples个样本
    sampled_samples = random.sample(samples, min(len(samples), num_samples))

    return sampled_samples

def write_excel(samples, output_file):
    data = {'Annotated Sequence': [sample[0] for sample in samples], 'Output': [sample[1] for sample in samples], 'Patient': [sample[2] for sample in samples]}
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == '__main__':
    input_dir = '/home/zxg/GMACID/cutkmer20/test'
    output_file = '/home/zxg/GMACID/cutkmer20/test/output_file.xlsx'

    # 获取指定目录下的所有文件
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # 随机抽取并排序样本
    sampled_samples = random_sort_samples(input_files)

    # 写入Excel文件
    write_excel(sampled_samples, output_file)
