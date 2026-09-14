output_dir="/home/heart6/rawdata/fastqc"
input_dir="/home/heart6/rawdata"

if [ ! -d "$output_dir" ]; then
    # 如果目录不存在，则创建它
    mkdir -p "$output_dir"
fi

cd "$input_dir"

for fp in ~/rawdata/*_1.fastq.gz
do
	fp1=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_1.fastq.gz'/)  #ERR1018189_1.fastq.gz
    fp2=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_2.fastq.gz'/)  #ERR1018189_2.fastq.gz
	fp=$(basename "$fp" | cut -d '_' -f 1)  #ERR1018189

	fastqc -o "$output_dir" "$fp1" "$fp2"

	fastp -i "$fp1" -I "$fp2" -u 45 -q 20 -u 5 -o ${fp}_clean1.fq.gz -O ${fp}_clean2.fq.gz	
	bowtie2 --quiet -p 12 -x hs1 -1 ${fp}_clean1.fq.gz -2 ${fp}_clean2.fq.gz --un-conc ${fp}_rmhost.fq > /dev/null
	#bowtie2 --quiet -p 12 -x hs1 -1 ${fp}_clean1.fq.gz -2 ${fp}_clean2.fq.gz --un-conc-gz ${fp}_rmhost.fq.gz > /dev/null
	pigz -p 12 ${fp}_rmhost.1.fq
	pigz -p 12 ${fp}_rmhost.2.fq
	#mv ${fp}_rmhost.fq.1.gz ${fp}_rmhost_1.fq.gz
	#mv ${fp}_rmhost.fq.2.gz ${fp}_rmhost_2.fq.gz




done
echo "Finish!"