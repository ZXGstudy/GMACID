input_dir="/home/zxg/GMACID/cutkmer/cutok"
output_dir="/home/zxg/GMACID/cutkmer/cutok/unique"


if [ ! -d "$output_dir" ]; then
    # 如果目录不存在，则创建它
    mkdir -p "$output_dir"
fi

cd "$input_dir"

for fp1 in ERR*.fa
do
    fp=$(basename "$fp1" | cut -d '_' -f 1,2 | sed 's/$/_unique.fa'/)   # 提取前两个用下划线分隔的部分
	vsearch --derep_fulllength $fp1 --output $output_dir/$fp --sizeout
	#echo "$fp2"
	#echo "$fp"

done
echo "Finish!"