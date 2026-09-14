#!/bin/bash

# 进入包含唯一序列文件的文件夹
cd "/home/zxg/GMACID/cutkmer/cutok/unique"

# 提取每个唯一序列文件的重叠序列
for file in *.fa; do
    mmseqs easy-cluster $file $file.cluster tmp_dir
    mmseqs createtsv $file $file $file.cluster $file.tsv
done
echo "共有序列已保存"