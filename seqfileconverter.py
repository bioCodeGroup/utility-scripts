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
    parser.add_argument('-t', '--file-type',
                        metavar='FILETYPE', help='type of input and output files qf=qseq2fastq fq=fastq2qseq sf=sam2fastq fs=fastq2qseq')


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

def fastq_to_sam(fastq_file, sam_file):
    """
    convert fastq file to sam file
    """
    #list into which the fastq file will be read
    #and from which the sam file will be written
    sam_list = []
    try:
        #loop that populates sam_list
        with open(fastq_file) as f:
            while True:
                header = f.readline().strip()
                seq = f.readline().strip()
                com = f.readline().strip()
                qual = f.readline().strip()
                if not qual:
                    break
                # Create lines in sam format
                sam_list += [header[1:], '\t', '4', '\t', '*', '\t', '0', '\t', '0', '\t', '*', '\t', '*', '\t', '0', '\t', '0', '\t', seq, '\t', qual, '\n']
    except IOError:
        print('Unable to open input file')
    # Write the output to output_file
    with open(sam_file, 'w') as output:
        for item in sam_list:
            output.writelines(item)

#def whichfileisit

def main():
    """
    Main routine

    Convert input file to specified output file type
    """

    args = get_args()
    if args.file_type == 'qf':
        qseq_to_fastq(args.input_file, args.output_file, args.metadata_file, args.discard_file)
    elif args.file_type == 'fq':
        fastq_to_qseq(args.input_file, args.output_file, args.metadata_file, args.discard_file)
    elif args.file_type == 'sf':
        sam2fastq(args.input_file, args.output_file)
    elif args.file_type == 'fs':
        fastq_to_sam(args.input_file, args.output_file)
    else:
        print('Your file type input does not match existing types, try again using qf, fq, sf, or fs. ')
if __name__ == '__main__':
    main()
