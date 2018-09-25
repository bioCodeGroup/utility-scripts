#!/usr/bin/env python
"""
This code imports a qseq file and exports a fastq file
"""
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

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def qseq_to_fastq(qseq_file, fastq_file):
    """
    convert qseq file to fastq file
    """ 
    # list into which the qseq file will be read,
    # and from which the fastq file will be built
    qseq_list = []
    try:
        with open(qseq_file) as f:
            #loop that populates qseq_list
            for line in f:
                fields = line.split()
                # excludes entries that aren't in qseq
                # format that didn't meet quality standards
                sequence = fields[8]
                n_sequence = sequence.replace(".", "N")
                fields[8] = n_sequence
                if len(fields) == 11 and fields[10] == '1' and len(fields[8]) == len(fields[9]) and isfloat(fields[4]) == True and isfloat(fields[5]) == True:
                    qseq_list = qseq_list + [fields]
    except:
        return 'Unable to open input file'

    with open(fastq_file, 'w') as output:
        for item in qseq_list:
            output.writelines('@'+":".join(item[:8])+'\n'+item[8]+'\n+\n'+item[9]+'\n')

def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    qseq_to_fastq(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
