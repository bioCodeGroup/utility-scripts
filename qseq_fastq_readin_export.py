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
                        metavar='INPUT FILES', help='fastq, qseq, or SAM file')
    parser.add_argument('-o', '--output-file',
                        metavar='OUTPUT FILES', help='fastq filenames')
    parser.add_argument('-m', '--metadata-file',
                        metavar='METADATAFILES', help='metadata filenames')
    parser.add_argument('-d', '--discard-file',
                        metavar='DISCARDFILE', help='file containing sequences discarded by QC')


    args = parser.parse_args()
    return args


def qseq_readin(input_file):
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
                    pass_list = pass_list + [fields]
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


    try:
        #take info from all lines passing qc
        with open(input_file) as f:
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






# Write to the qseq export file
def qseq_export():
    with open(export_file, 'w') as output:
        for item in pass_list:
            output.writelines(item)


# Write to the fastq export file
def fastq_export():
    with open(output_file, 'w') as output:
        for item in pass_list:
            output.writelines('@'+":".join(item[:8])+'\n'+item[8]+'\n+\n'+item[9]+'\n')


# Write the metadata to metadata_file
def mdat_export():
    with open(metadata_file, 'w') as mdat:
            mdat.writelines(['Input qseq file: ' , str(input_file),
                            '\n' , 'Output fastq file: ' , str(export_file),
                            '\n' , 'Number of lines passing Quality Control: ',
                            str(pass_count), '\n',
                            'Number of lines failing Quality Control or not proper qseq file lines: ',
                            str(fail_count)])


# Write to the discard export file
def discard_export():
    with open(discard_file, 'w') as disc:
        for item in fail_list:
            disc.writelines('@'+":".join(item[:8])+'\n'+item[8]+'\n+\n'+item[9]+'\n')




qseq_readin(qseq_file)



def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()
    qseq_to_fastq(args.input_file, args.output_file, args.metadata_file, args.discard_file)

if __name__ == '__main__':
    main()
