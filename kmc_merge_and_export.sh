#!/bin/bash

# 输出目录
OUT_DIR="/home/zxg/GMACID/cutkmer20/all/test/kmc_output"

# 创建临时目录用于中间文件
TMP_DIR="$OUT_DIR/tmp"
mkdir -p $TMP_DIR

# 合并所有健康人的k-mer计数文件
FILES=($OUT_DIR/healthy_*.kmc_pre)
MERGED_FILE=$TMP_DIR/merged_healthy

# 初始化合并文件
cp ${FILES[0]} $MERGED_FILE.kmc_pre
cp ${FILES[0]/.kmc_pre/.kmc_suf} $MERGED_FILE.kmc_suf

# 两两合并健康人的k-mer计数文件
for ((i=1; i<${#FILES[@]}; i++)); do
    TMP_MERGED=$TMP_DIR/tmp_merged
    kmc_tools simple $MERGED_FILE ${FILES[$i]/.kmc_pre/} union $TMP_MERGED
    mv $TMP_MERGED.kmc_pre $MERGED_FILE.kmc_pre
    mv $TMP_MERGED.kmc_suf $MERGED_FILE.kmc_suf
done

mv $MERGED_FILE.kmc_pre $OUT_DIR/merged_healthy.kmc_pre
mv $MERGED_FILE.kmc_suf $OUT_DIR/merged_healthy.kmc_suf

# 合并所有癌症患者的k-mer计数文件
FILES=($OUT_DIR/cancer_*.kmc_pre)
MERGED_FILE=$TMP_DIR/merged_cancer

# 初始化合并文件
cp ${FILES[0]} $MERGED_FILE.kmc_pre
cp ${FILES[0]/.kmc_pre/.kmc_suf} $MERGED_FILE.kmc_suf

# 两两合并癌症患者的k-mer计数文件
for ((i=1; i<${#FILES[@]}; i++)); do
    TMP_MERGED=$TMP_DIR/tmp_merged
    kmc_tools simple $MERGED_FILE ${FILES[$i]/.kmc_pre/} union $TMP_MERGED
    mv $TMP_MERGED.kmc_pre $MERGED_FILE.kmc_pre
    mv $TMP_MERGED.kmc_suf $MERGED_FILE.kmc_suf
done

mv $MERGED_FILE.kmc_pre $OUT_DIR/merged_cancer.kmc_pre
mv $MERGED_FILE.kmc_suf $OUT_DIR/merged_cancer.kmc_suf

# 删除临时目录
rm -rf $TMP_DIR

# 导出k-mer计数为文本格式
kmc_tools transform $OUT_DIR/merged_healthy dump -s $OUT_DIR/merged_healthy.txt
kmc_tools transform $OUT_DIR/merged_cancer dump -s $OUT_DIR/merged_cancer.txt
