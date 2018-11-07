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


    args = parser.parse_args()
    return args


def qseq_readin(qseq_file):
    """
    read in a qseq file and turn important features into variables in a list
    """
    # list into which the qseq file will be read,
    # and from which a future output file will be built
    # Also, pass_count and fail_count count the
    # input file's lines which either pass/fail
    # quality control and testing to make sure
    # the line is actually part of the qseq file

    pass_list = []
    fail_list = []
    pass_count = 0
    fail_count = 0

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
                # dnaverify = isdna(n_sequence)
                if len(fields) == 11 and fields[10] == '1' and len(fields[8]) == len(fields[9]) and isfloat(fields[4]) == True and isfloat(fields[5]) == True and isdna(fields[8]) == True:
                    pass_list = qseq_list + [fields]
                    pass_count += 1
                else:
                    fail_list = fail_list + [fields]
                    fail_count += 1
    except IOError:
        print('Unable to open input file')

def fastq_readin(fastq_file):
    """
    convert fastq file to qseq file
    """
    # After importing a fastq file, this code creates
    # a list into which the fastq file will be read,
    # and from which the qseq file will be built.
    # The file also adds failed reads from a discard
    # file and appends failed reads to the end of
    # the list for qseq conversion.
    # Also, pass_count and fail_count count the
    # input file's lines which either pass/fail
    # quality control and testing to make sure
    # the line is actually part of the qseq file.
    # Lastly, this code creates a metadata file.

    pass_list = []
    pass_count = 0
    fail_count = 0
    count = 0

    try:
        #take info from all lines passing qc
        with open(fastq_file) as f:
            while True:
                header = f.readline().strip().split(':')
                seq = f.readline().strip()
                com = f.readline().strip()
                qual = f.readline().strip()
                if not qual:
                    break
                # Create lines of qseq formatted files
                if len(seq) == len(qual) and val.isfloat(header[4]) == True and val.isfloat(header[5]) == True and val.isdna(seq) == True:
                    pass_list += '\t'.join([header[0][1:], '\t'.join(header[1:]), seq, qual, '1\n'])
                    pass_count += 1

    except IOError:
        print('Unable to open input file')

    try:
        #take info from all lines passing qc
        with open(discard_file) as f:
            while True:
                header = f.readline().strip().split(':')
                seq = f.readline().strip()
                com = f.readline().strip()
                qual = f.readline().strip()
                if not qual:
                    break
                # Create lines of qseq formatted files
                if len(seq) == len(qual) and val.isfloat(header[4]) == True and val.isfloat(header[5]) == True and val.isdna(seq) == True:
                    fail_list += '\t'.join([header[0][1:], '\t'.join(header[1:]), seq, qual, '0\n'])
                    fail_count += 1

    except IOError:
        print('Unable to open input file')


def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    qseq_to_fastq(args.input_file, args.output_file, args.metadata_file, args.discard_file)

if __name__ == '__main__':
    main()
