input_dir="/home/zxg/GMACID/mega"
output_dir="/home/zxg/GMACID/mega/test"

cd "$input_dir"

for fp in ERR*.fq
do
    fp1=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_host.1.fq'/)
    fp2=$(basename "$fp" | cut -d '_' -f 1 | sed 's/$/_host.2.fq'/) 
    fp=$(basename "$fp" | cut -d '_' -f 1)  #ERR1018189
    megahit -1 ${fp}_host.1.fq -2 ${fp}_host.2.fq -o output/${fp} 1> log 2>err
done

echo "done" 
