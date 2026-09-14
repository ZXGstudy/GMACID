#!/bin/bash

# 健康人文件夹
HEALTHY_DIR="/home/zxg/GMACID/cutkmer20/all/test/healthy"
# 癌症患者文件夹
CANCER_DIR="/home/zxg/GMACID/cutkmer20/all/test/cancer"

# K-mer 长度
KMER_SIZE=20
# 哈希表大小，单位是字节，可以根据实际情况调整
HASH_SIZE=2G
# 使用的线程数，根据你的机器的CPU核心数调整
THREADS=2

# 创建输出目录
OUTPUT_DIR="/home/zxg/GMACID/cutkmer20/all/test/jellyfish_output"
mkdir -p $OUTPUT_DIR

# 处理健康人文件
echo "Processing healthy files..."
for file in $HEALTHY_DIR/*.fa; do
    base=$(basename $file .fa)
    echo "Processing $file"
    if ! jellyfish count -m $KMER_SIZE -s $HASH_SIZE -t $THREADS -C -o $OUTPUT_DIR/healthy_${base}.jf $file; then
        echo "Error processing $file"
        exit 1
    fi
done

# 处理癌症患者文件
echo "Processing cancer files..."
for file in $CANCER_DIR/*.fa; do
    base=$(basename $file .fa)
    echo "Processing $file"
    if ! jellyfish count -m $KMER_SIZE -s $HASH_SIZE -t $THREADS -C -o $OUTPUT_DIR/cancer_${base}.jf $file; then
        echo "Error processing $file"
        exit 1
    fi
done

# 合并所有健康人和癌症患者的k-mer计数文件
echo "Merging k-mer count files..."
if ls $OUTPUT_DIR/healthy_*.jf 1> /dev/null 2>&1; then
    jellyfish merge -o $OUTPUT_DIR/merged_healthy.jf $OUTPUT_DIR/healthy_*.jf
else
    echo "No healthy .jf files to merge."
    exit 1
fi

if ls $OUTPUT_DIR/cancer_*.jf 1> /dev/null 2>&1; then
    jellyfish merge -o $OUTPUT_DIR/merged_cancer.jf $OUTPUT_DIR/cancer_*.jf
else
    echo "No cancer .jf files to merge."
    exit 1
fi

# 导出k-mer计数为文本格式
echo "Dumping k-mer counts to text files..."
if [ -f $OUTPUT_DIR/merged_healthy.jf ]; then
    jellyfish dump -c -t $OUTPUT_DIR/merged_healthy.jf > $OUTPUT_DIR/merged_healthy.txt
else
    echo "Merged healthy .jf file not found."
    exit 1
fi

if [ -f $OUTPUT_DIR/merged_cancer.jf ]; then
    jellyfish dump -c -t $OUTPUT_DIR/merged_cancer.jf > $OUTPUT_DIR/merged_cancer.txt
else
    echo "Merged cancer .jf file not found."
    exit 1
fi

echo "All processing completed successfully."

