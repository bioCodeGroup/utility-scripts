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
    parser.add_argument('-m', '--metadata-file',
                        metavar='METADATAFILES', help='metadata filenames')


    args = parser.parse_args()

    return args

def qseq_to_fastq(qseq_file, fastq_file, metadata_file):
    """
    convert qseq file to fastq file
    """
    # list into which the qseq file will be read,
    # and from which the fastq file will be built
    # Also, pass_count and fail_count count the
    # input file's lines which either pass/fail
    # quality control and testing to make sure
    # the line is actually part of the qseq file

    qseq_list = []
    pass_count = 0
    fail_count = 0

    try:
        with open(qseq_file) as f:
            #loop that populates qseq_list
            for line in f:
                fields = line.split()
                # excludes entries that aren't in qseq
                # format that didn't meet quality standards
                if len(fields) == 11 and fields[10] == '1':
                    qseq_list = qseq_list + [fields]
                    pass_count += 1
                else:
                    fail_count += 1
    except IOError:
        print('Unable to open input file')

    with open(fastq_file, 'w') as output:
        for item in qseq_list:
            output.writelines('@'+":".join(item[:8])+'\n'+item[8]+'\n+\n'+item[9]+'\n')

    with open(metadata_file, 'w') as mdat:
            mdat.writelines(['Input qseq file: ' , str(qseq_file),
                            '\n' , 'Output fastq file: ' , str(fastq_file),
                            '\n' , 'Number of lines passing Quality Control: ',
                            str(pass_count), '\n',
                            'Number of lines failing Quality Control or not proper qseq file lines: ',
                            str(fail_count)])

def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    qseq_to_fastq(args.input_file, args.output_file, args.metadata_file)

if __name__ == '__main__':
    main()
