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

## add function to read entries from qseq 
##
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
