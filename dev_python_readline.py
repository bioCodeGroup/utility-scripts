#!/usr/bin/env python
"""
This code imports a qseq file and exports a fastq file
"""
from __future__ import absolute_import
import argparse
from itertools import islice


def get_args():
    """
    Get input arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input-file',
                        metavar='QSEQFILES', help='qseq files')
    parser.add_argument('-o', '--output-file',
                        metavar='FASTQFILES', help='fastq filenames')
    parser.add_argument('-m', '--metadata-file',
                        metavar='METADATAFILES', help='metadata filenames')
    parser.add_argument('-d', '--discard-file',
                        metavar='DISCARDFILE', help='file containing sequences discarded by QC')


    args = parser.parse_args()

    return args

def fastq_to_qseq(fastq_file, qseq_file, metadata_file, discard_file):
    """
    convert fastq file to qseq file
    """
    # list into which the qseq file will be read,
    # and from which the fastq file will be built
    # Also, pass_count and fail_count count the
    # input file's lines which either pass/fail
    # quality control and testing to make sure
    # the line is actually part of the qseq file

    qseq_list = []
    fail_list = []
    pass_count = 0
    fail_count = 0
    a = ''
    count = 0

    try:
        #take info from all lines passing qc
        with open(fastq_file) as f:
            #loop that populates qseq_list
            for line in f:
                if ":" in line:
                    fields = line.split(":")
                    line = line.replace(':','\t')
                    seq = list(islice(f, 2))[-1]
                    qual = list(islice(f, 3))[-1]
                    a += line.strip()+ '\t' + seq.strip() + qual.strip() + '\t1\n'

                    count += 1

        #take info from all lines failing qc
        with open(discard_file) as f:
            #loop that populates qseq_list
            for line in f:
                if ":" in line:
                    fields = line.split(":")
                    line = line.replace(':','\t')
                    seq = list(islice(f, 2))[-1]
                    qual = list(islice(f, 3))[-1]
                    a += line.strip()+ '\t' + seq.strip() + qual.strip() + '\t0\n'
                    count += 1

#print statements just for development
        print(a)
        print (count)
    except IOError:
        print('Unable to open input file')





def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    fastq_to_qseq(args.input_file, args.output_file, args.metadata_file, args.discard_file)

if __name__ == '__main__':
    main()
