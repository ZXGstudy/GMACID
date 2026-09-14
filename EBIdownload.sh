#!/bin/bash

# 使用ascp下载文件，例如FASTQ文件
ascp -vQT -l 500M -P33001 -k 1 -i ~/.aspera/connect/etc/asperaweb_id_dsa.openssh \
     --host fasp.sra.ebi.ac.uk --user era-fasp --mode=recv \
     --file-list /home/zxg/sh/file_list /home/zxg/GMACID/RAWDATA
