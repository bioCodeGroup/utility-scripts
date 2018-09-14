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


def qseq_to_fastq (qseq_file, fastq_file):
    
    
    try:
        with open(qseq_file) as f:

            qseq_list = []      #list into which the qseq file will be read, and from which the fastq file will be built
            sep = ":"
    
            for line in f:  #loop that populates qseq_list
                fields = line.split()
                if len(fields) != 11:   #excludes entries that aren't in qseq format from the output without stopping the whole program
                    continue
                if fields[10] == '0':   #excludes sequences that didn't meet quality standards
                    continue
                qseq_list = qseq_list + [fields]
    except:
        return 'Unable to open input file'
    
    with open(fastq_file, 'w') as output:
        for item in qseq_list:
            output.writelines('@'+sep.join(item[:8]+'\n'+item[8]+'\n+\n'+item[9]+'\n')

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
