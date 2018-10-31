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
    # list into which the qseq file will be read,
    # and from which the fastq file will be built
    # Also, pass_count and fail_count count the
    # input file's lines which either pass/fail
    # quality control and testing to make sure
    # the line is actually part of the qseq file

    qseq_list = []
    pass_count = 0
    fail_count = 0
    count = 0

    try:
        #take info from all lines passing qc
        with open(fastq_file) as f:
            while True:
                header = f.readline().strip()
                #if len(fields) == 11 and fields[10] == '1' and len(fields[8]) == len(fields[9]) and val.isfloat(fields[4]) == True and val.isfloat(fields[5]) == True and val.isdna(fields[8]) == True:
                seq = f.readline().strip()
                com = f.readline().strip()
                qual = f.readline().strip()
                qc = str(header.split(':'))
                if len(seq) == len(qual):
                    for fields in str(header.split(':')):
                        if len(fields) == 11 and fields[10] == '1' and val.isfloat(fields[4]) == True and val.isfloat(fields[5]) == True:
                            qseq_list += [header.replace(':','\t') + '\t' + seq + '\t' + qual + '\t1' + '\n']

                qseq_list += [header + '\t' + seq + '\t' + qual + '\t1' + '\n']
                pass_count += 1
                if not qual:
                    break
    except IOError:
        print('Unable to open input file')

        #take info from all lines failing qc
        #with open(discard_file) as f:
            #loop that populates qseq_list with failed reads

                    #fail_count += 1
                #if fail_count == 0:
                    #print("Unable to convert any lines in discard file")

    try:
        #take info from all lines passing qc
        with open(discard_file) as f:
            while True:
                header = f.readline().strip()
                seq = f.readline().strip()
                com = f.readline().strip()
                qual = f.readline().strip()
                qseq_list += [header.replace(':','\t') + '\t' + seq + '\t' + qual + '\t0' + '\n']
                fail_count += 1
                if not qual:
                    break
        #print (qseq_list)
    except IOError:
        print('Unable to open input file')

    with open(qseq_file, 'w') as output:
        for item in qseq_list:
            output.writelines(item)

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
