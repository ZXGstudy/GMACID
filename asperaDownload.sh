#!/bin/bash
for i in $(cat srr.list)
do 
x=$(echo $i | cut -b1-6)
y=`echo ${i: -2}`
echo "vol1/fastq/${x}/00${y}/${i}/${i}_1.fastq.gz" >>fastqid_trim.txt
echo "vol1/fastq/${x}/00${y}/${i}/${i}_2.fastq.gz" >>fastqid_trim.txt
done

ascp -v -QT -l 300m -P33001 -k1 -i ~/.aspera/connect/etc/asperaweb_id_dsa.openssh --mode recv --host fasp.sra.ebi.ac.uk --user era-fasp --file-list srr.list ~/GMACID/RAWDATA
#rm fastqid_trim.txt