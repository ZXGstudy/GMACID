from Bio import SeqIO
from collections import defaultdict

def count_sequences(file):
    seq_count = defaultdict(int)
    for seq_record in SeqIO.parse(file, "fasta"):
        seq_str = str(seq_record.seq)
        seq_count[seq_str] += 1
    return seq_count

# 统计每个文件中的序列出现次数
test_seq_count = count_sequences("testcombined.fa")
train_seq_count = count_sequences("traincombined.fa")

# 合并结果
all_sequences = set(test_seq_count.keys()).union(set(train_seq_count.keys()))

# 输出结果
with open("sequence_counts.txt", "w") as output_file:
    output_file.write("Sequence\tTestCount\tTrainCount\n")
    for seq in all_sequences:
        test_count = test_seq_count.get(seq, 0)
        train_count = train_seq_count.get(seq, 0)
        output_file.write(f"{seq}\t{test_count}\t{train_count}\n")

print("统计完成，结果已保存到 sequence_counts.txt")
