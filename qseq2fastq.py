#!/usr/bin/env python

from __future__ import absolute_import
import argparse

def get_args():
    """
    Get input arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input-file', nargs="+",
                        metavar='QSEQFILES', help='qseq files')
    parser.add_argument('-o', '--output-file', nargs="+",
                        metavar='FASTQFILES', help='fastq filenames')

    args = parser.parse_args()

    return args

## To do:

f = open("sampleqseq2.txt","r")
lib = {}
sep = ":"
for line in f:
    a = line.split('|')
    headers = "@" + sep.join(a[0:8])
    seq = a[8]
    qual = a[9]
    filtering = a[21].strip()
    #print(headers)
    #print (seq)
    #print(qual)
    #print (filtering)
## add function to filter out bad entries
##


def main():
    """
    Main routine

    Convert qseq file to fastq file
    """

    args = get_args()

if __name__ == '__main__':
    main()
