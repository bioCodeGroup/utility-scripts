#!/usr/bin/env python
"""
This code imports a file, determines its type, and exports it
into the user specified file type.
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

def qseq_to_fastq(qseq_file, fastq_file, metadata_file, discard_file):
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
                if len(fields) == 11 and fields[10] == '1' and len(fields[8]) == len(fields[9]) and val.isfloat(fields[4]) == True and val.isfloat(fields[5]) == True and val.isdna(fields[8]) == True:
                    qseq_list = qseq_list + [fields]
                    pass_count += 1
                else:
                    fail_list = fail_list + [fields]
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

    with open(discard_file, 'w') as disc:
        for item in fail_list:
            disc.writelines('@'+":".join(item[:8])+'\n'+item[8]+'\n+\n'+item[9]+'\n')


#def fastq2qseq

def sam2fastq(sam_file, fastq_file):
    """
    convert a sam file to a fastq file
    """
    #list into which the sam file will be read and from which the fastq file will be built
    sam_list = []
    try:
        #loop that populates sam_list
        with open(sam_file) as sam:
            for line in sam:
                sam_fields = line.split()
                #excludes header lines (which start with '@' in sam files)
                if '@' not in sam_fields[0]:
                    sam_list += [sam_fields]
    except IOError:
        print('Unable to open input file')
    with open(fastq_file, 'w') as fq:
        for entry in sam_list:
            #writes fastq file using the first column of the sam file as
            #the first line of the fastq file
            fq.writelines('@'+entry[0]+'\n'+entry[9]+'\n+\n'+entry[10]+'\n')       
#def fastq2sam

#def whichfileisit



def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    #qseq_to_fastq(args.input_file, args.output_file, args.metadata_file, args.discard_file)
    sam2fastq(args.input_file, args.output_file)
if __name__ == '__main__':
    main()
