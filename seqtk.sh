input_dir="/mnt/g/rmhost"
output_dir="/home/zxg/GMACID/seqtk1M"

cd "$input_dir"

for fp in ERR*_rm.1.fq
do
	fp1=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_1.fastq.gz'/)  #ERR1018189_1.fastq.gz
    fp2=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_2.fastq.gz'/)  #ERR1018189_2.fastq.gz
	fp=$(basename "$fp" | cut -d '_' -f 1)  #ERR1018189
	
	seqtk sample -s100 ${fp}_rm.1.fq 1000000 > $output_dir/${fp}_seq1.fq
	seqtk sample -s100 ${fp}_rm.2.fq 1000000 > $output_dir/${fp}_seq2.fq
	
done
echo "Finish!"