import pandas as pd
import random
import os

def read_fasta(file_path):
    """
    读取FASTA文件并提取序列
    :param file_path: FASTA文件路径
    :return: 序列列表
    """
    sequences = []
    with open(file_path, 'r') as file:
        entries = file.read().split('>')[1:]  # 分割每个条目
        for entry in entries:
            lines = entry.split('\n')
            sequence = ''.join(lines[1:])  # 获取序列并连接
            sequences.append(sequence)
    return sequences

def random_sort_samples(sequences, num_samples_per_file=100, num_repeats=100):
    """
    从序列列表中随机抽取样本
    :param sequences: 原始序列列表
    :param num_samples_per_file: 每次抽样的序列数
    :param num_repeats: 抽样次数
    :return: 抽样结果列表
    """
    samples = []

    for _ in range(num_repeats):
        if len(sequences) < num_samples_per_file:
            print("Not enough sequences left for another sample.")
            break

        sampled_indices = random.sample(range(len(sequences)), num_samples_per_file)
        sampled_sequences = [sequences[i] for i in sampled_indices]

        # Remove sampled sequences from the pool to ensure no replacement
        for i in sorted(sampled_indices, reverse=True):
            del sequences[i]

        sorted_sequences = ' '.join(sorted(sampled_sequences))
        samples.append(sorted_sequences)

    return samples

def append_samples_to_list(all_samples, samples, sample_id, response_dict):
    """
    将样本添加到总列表中
    :param all_samples: 所有样本的总列表
    :param samples: 当前样本列表
    :param sample_id: 样本ID
    :param response_dict: Response字典
    """
    output_values = [response_dict.get(sample_id, '') for _ in samples]
    for sample, response in zip(samples, output_values):
        text = f"### Instruction:\nAnnotate the following sequence.\n\n### Input:\n{sample}.\n\n### Response:\n{response}."
        all_samples.append((text, response, sample_id))

if __name__ == '__main__':
    input_dir = '/home/zxg/GMACID/hostDNA/cutkmer20/train'
    output_file = '/home/zxg/GMACID/hostDNA/cutkmer20/combined_output.xlsx'
    sample_csv = '/home/zxg/GMACID/hostDNA/cutkmer20/sample.csv'
    final_output_file = '/home/zxg/GMACID/hostDNA/cutkmer20/train-data.csv'
    # 读取 sample.csv 文件并创建 response 字典
    sample_df = pd.read_csv(sample_csv, dtype=str).fillna('')
    response_dict = {row['SampleID'].strip(): row['response'].strip() for index, row in sample_df.iterrows()}

    # 获取指定目录下的所有文件
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    all_samples = []

    # 处理每个文件
    for file_path in input_files:
        print(f"Processing file: {file_path}")
        sequences = read_fasta(file_path)
        file_name = os.path.basename(file_path)
        sample_id = file_name.split('_')[0]  # 提取第一个下划线前面的内容

        # 随机抽取并排序样本
        sampled_samples = random_sort_samples(sequences)

        # 将样本添加到总列表中
        append_samples_to_list(all_samples, sampled_samples, sample_id, response_dict)

    # 打乱所有样本的顺序
    random.shuffle(all_samples)

    # 写入Excel文件
    data = {
        'text': [sample[0] for sample in all_samples],
        'output': [sample[1] for sample in all_samples],
        'patient': [sample[2] for sample in all_samples]
    }
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    sampled_df = df.sample(n=1000, random_state=1)
    sampled_df.to_csv(final_output_file, index=False)
