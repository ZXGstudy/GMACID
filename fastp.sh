input_dir="/home/zxg/GMACID/RAWDATA"
output_dir="/home/zxg/GMACID/fastpdeal_4"


if [ ! -d "$output_dir" ]; then
    # 如果目录不存在，则创建它
    mkdir -p "$output_dir"
fi

cd "$input_dir"

for fp in ERR*.fastq.gz
do
	fp1=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_1.fastq.gz'/)  #ERR1018189_1.fastq.gz
    fp2=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_2.fastq.gz'/)  #ERR1018189_2.fastq.gz
	fp=$(basename "$fp" | cut -d '_' -f 1)  #ERR1018189
	fastp -i "$fp1" -I "$fp2" -w 10 -u 45 -q 20 -l 70 -y -D --trim_poly_g -o "$output_dir/${fp}_clean1.fq.gz" -O "$output_dir/${fp}_clean2.fq.gz" -h "$output_dir/${fp}_fastp.html"
	#fastp -i ./0.Rawdata/$1.R1.fq.gz -I ./0.Rawdata/$1.R2.fq.gz -o ./1.Cleandata/$1_clean.1.fq.gz -O ./1.Cleandata/$1_clean.2.fq.gz -w 10 -u 40 -q 20 -l 100 -y --trim_poly_g
done
echo "Finish!"