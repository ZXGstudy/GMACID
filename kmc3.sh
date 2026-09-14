#!/bin/bash

# 健康人文件夹
HEALTHY_DIR="/home/zxg/GMACID/cutkmer20/all/test/healthy"
# 癌症患者文件夹
CANCER_DIR="/home/zxg/GMACID/cutkmer20/all/test/cancer"

# K-mer 长度
KMER_SIZE=20
# 临时目录
TMP_DIR="/home/zxg/GMACID/cutkmer20/all/test/kmc_tmp"
# 输出目录
OUT_DIR="/home/zxg/GMACID/cutkmer20/all/test/kmc_output"

# 创建输出目录和临时目录
mkdir -p $OUT_DIR
mkdir -p $TMP_DIR

# 处理健康人文件
for file in $HEALTHY_DIR/*.fa; do
    base=$(basename $file .fa)
    kmc -k$KMER_SIZE -ci1 -cs10000 -fm $file $OUT_DIR/healthy_${base} $TMP_DIR
done

# 合并所有健康人的k-mer计数文件
kmc_tools union $OUT_DIR/healthy_* $OUT_DIR/merged_healthy

# 处理癌症患者文件
for file in $CANCER_DIR/*.fa; do
    base=$(basename $file .fa)
    kmc -k$KMER_SIZE -ci1 -cs10000 -fm $file $OUT_DIR/cancer_${base} $TMP_DIR
done

# 合并所有癌症患者的k-mer计数文件
kmc_tools union $OUT_DIR/cancer_* $OUT_DIR/merged_cancer

# 导出k-mer计数为文本格式
kmc_tools transform $OUT_DIR/merged_healthy dump -s $OUT_DIR/merged_healthy.txt
kmc_tools transform $OUT_DIR/merged_cancer dump -s $OUT_DIR/merged_cancer.txt
