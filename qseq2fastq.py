#!/usr/bin/env python

from __future__ import absolute_import
import argparse

def get_args():
    """
    Get input arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input-file', nargs="+",
                        metavar='QSEQFILES', help='qseq files')
    parser.add_argument('-o', '--output-file', nargs="+",
                        metavar='FASTQFILES', help='fastq filenames')

    args = parser.parse_args()

    return args


def qseq_to_fastq (input_file, output_file):
    
    with open(qseq_file) as f:
        # do stuff with f 
    
    
    try:
        input = open(input_file)
    except:
        return 'Unable to open input file'
    output = open(output_file, 'w')
    qseq_list = []      #list into which the qseq file will be read, and from which the fastq file will be built
    for line in input:  #loop that populates qseq_list
        fields = line.split()
        if len(fields) != 11:   #excludes entries that aren't in qseq format from the output without stopping the whole program
            continue
        if fields[10] == '0':   #excludes sequences that didn't meet quality standards
            continue
        qseq_list = qseq_list + [fields]

    f = open(args.input_file,"r")
    lib = {}
    sep = ":"
    for line in f:
        a = line.split()
        headers = "@" + sep.join(a[0:8])
        seq = a[8]
        qual = a[9]
        filtering = a[21].strip()
    #print(headers)
    #print (seq)
    #print(qual)
    #print (filtering)
## add function to filter out bad entries
##
def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    print(args)
    qseq_to_fastq(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
