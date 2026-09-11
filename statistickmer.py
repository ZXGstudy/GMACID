import pandas as pd
from scipy.stats import chi2_contingency

def load_kmers(filename):
    kmers = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            kmers[parts[0]] = int(parts[1])
    return kmers

# 加载k-mer数据
healthy_kmers = load_kmers('jellyfish_output/merged_healthy.txt')
cancer_kmers = load_kmers('jellyfish_output/merged_cancer.txt')

# 找到共有的k-mer和特有的k-mer
common_kmers = {}
unique_healthy = {}
unique_cancer = {}

for kmer, count in healthy_kmers.items():
    if kmer in cancer_kmers:
        common_kmers[kmer] = (count, cancer_kmers[kmer])
    else:
        unique_healthy[kmer] = count

for kmer, count in cancer_kmers.items():
    if kmer not in healthy_kmers:
        unique_cancer[kmer] = count

# 保存结果
with open('common_kmers.txt', 'w') as f:
    for kmer, counts in common_kmers.items():
        f.write(f"{kmer}\t{counts[0]}\t{counts[1]}\n")

with open('unique_healthy_kmers.txt', 'w') as f:
    for kmer, count in unique_healthy.items():
        f.write(f"{kmer}\t{count}\n")

with open('unique_cancer_kmers.txt', 'w') as f:
    for kmer, count in unique_cancer.items():
        f.write(f"{kmer}\t{count}\n")

# 卡方检验
chi2_results = []
for kmer, counts in common_kmers.items():
    table = [[counts[0], sum(healthy_kmers.values()) - counts[0]],
             [counts[1], sum(cancer_kmers.values()) - counts[1]]]
    chi2, p, _, _ = chi2_contingency(table)
    chi2_results.append((kmer, chi2, p))

# 转换为DataFrame并筛选
chi2_df = pd.DataFrame(chi2_results, columns=['kmer', 'chi2', 'p'])
chi2_df['adjusted_p'] = chi2_df['p'] * len(chi2_df)  # 多重检验校正
significant_kmers = chi2_df[chi2_df['adjusted_p'] < 0.05]

# 保存卡方检验结果
significant_kmers.to_csv('significant_kmers.csv', index=False)