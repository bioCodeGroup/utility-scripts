#!/usr/bin/env python
"""
This code imports a fastq file and exports a qseq file
"""
from __future__ import absolute_import
import argparse
import QCvalidate as val


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

    qseq_list = []
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
                    qseq_list += '\t'.join([header[0][1:], '\t'.join(header[1:]), seq, qual, '1\n'])
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
                    qseq_list += '\t'.join([header[0][1:], '\t'.join(header[1:]), seq, qual, '0\n'])
                    fail_count += 1

    except IOError:
        print('Unable to open input file')

    # Write the output to output_file
    with open(qseq_file, 'w') as output:
        for item in qseq_list:
            output.writelines(item)

    # Write the metadata to metadata_file
    with open(metadata_file, 'w') as mdat:
            mdat.writelines(['Input qseq file: ' , str(fastq_file),
                            '\n' , 'Output fastq file: ' , str(qseq_file),
                            '\n' , 'Number of lines extracted from fastq file: ',
                            str(pass_count),
                            '\n' , 'Number of lines extracted from discard file: ',
                            str(fail_count)])
def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    fastq_to_qseq(args.input_file, args.output_file, args.metadata_file, args.discard_file)

if __name__ == '__main__':
    main()
