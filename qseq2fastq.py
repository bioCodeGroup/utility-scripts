#!/usr/bin/env python

from __future__ import absolute_import
import argparse

def get_args():
    """
    Get input arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input-file',
                        metavar='QSEQFILES', help='qseq files')
    parser.add_argument('-o', '--output-file',
                        metavar='FASTQFILES', help='fastq filenames')

    args = parser.parse_args()

    return args


def qseq_to_fastq(qseq_file, fastq_file):
    """
    convert qseq file to fastq file
    """
    # list into which the qseq file will be read, 
    # and from which the fastq file will be built
    qseq_list = []
    sep = ":"
    try:
        with open(qseq_file) as f:
            #loop that populates qseq_list
            for line in f:  
                fields = line.split()
                # excludes entries that aren't in qseq 
                # format 
                if len(fields) != 11:  
                    continue
                if fields[10] == '0':   #excludes sequences that didn't meet quality standards
                    continue
                qseq_list = qseq_list + [fields]
    except:
        return 'Unable to open input file'
    
    with open(fastq_file, 'w') as output:
        for item in qseq_list:
            output.writelines('@'+sep.join(item[:8])+'\n'+item[8]+'\n+\n'+item[9]+'\n')

def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    qseq_to_fastq(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
