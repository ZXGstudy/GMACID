input_dir="/mnt/f/nuohe_meta_pre4/cleandata"
output_dir="/home/zxg/skinm/rmhost"


if [ ! -d "$output_dir" ]; then
    # 如果目录不存在，则创建它
    mkdir -p "$output_dir"
fi

cd "$input_dir"

for fp in ST*.clean.fq.gz
do
	fp1=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_1.clean.fq.gz'/)
    fp2=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_2.clean.fq.gz'/) 
	fp=$(basename "$fp" | cut -d '_' -f 1)  #ERR1018189
	#未比对到宿主的：bowtie2 -p 2 -x /home/zxg/GMACID/hg38/human38 -1 ${fp}_clean1.fq.gz -2 ${fp}_clean2.fq.gz -S $output_dir/${fp}.sam --un-conc $output_dir/${fp}_rm.fq > $output_dir/${fp}.rm_log
	#bowtie2 -p 4 -x /mnt/f/hg38/human38 --end-to-end --sensitive -I 200 -X 400 -1 ${fp}_1.clean.fq.gz -2 ${fp}_2.clean.fq.gz -S $output_dir/${fp}.sam --al-conc $output_dir/${fp}_host.fq > $output_dir/${fp}.rm_log 2>&1
	bowtie2 -p 4 -x /mnt/f/hg38/human38 -1 ${fp}_1.clean.fq.gz -2 ${fp}_2.clean.fq.gz -S $output_dir/${fp}.sam --un-conc $output_dir/${fp}_rm.fq > $output_dir/${fp}.rm_log 2>&1
	#rm $output_dir/${fp}.sam
done
	#bowtie2 -p 20 -x /home/zxg/GMACID/human/human -1 ${fp}_clean1.fq.gz -2 ${fp}_clean2.fq.gz -S $output_dir/${fp}.sam --un-conc $output_dir/${fp}_rm.fq > $output_dir/${fp}.rm_log 2>&1



