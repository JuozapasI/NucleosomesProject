#!/bin/bash

bam=$1
output=$2
chr=$3

samtools view -f 0x2 -F 0x4 ${bam} ${chr} | awk -F'\t' 'BEGIN {OFS = FS} $9 > 0 {print $3, $4, $4 + $9 -1;}' > ${output}

