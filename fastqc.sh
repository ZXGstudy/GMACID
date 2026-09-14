input_dir="/home/zxg/GMACID/fastpdeal_4"
output_dir="/home/zxg/GMACID/fastpdeal/fastqc_4"


if [ ! -d "$output_dir" ]; then
    # 如果目录不存在，则创建它
    mkdir -p "$output_dir"
fi

cd "$input_dir"

for fp in ERR*_clean1.fq.gz
do
    # 生成对应的 _clean2.fq.gz 文件名
    fp1=$(basename "$fp")
    fp2=$(basename "$fp" | sed 's/_clean1.fq.gz/_clean2.fq.gz/')
    # 运行 fastqc
    fastqc -o "$output_dir" "$fp1" "$fp2"
done