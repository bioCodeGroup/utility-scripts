#!/usr/bin/env python
""" This is a template for python scripts """

# add package imports here, for example we import future to make our code "future-proof" (ie py2 -> py3):
# and argparse to add options to our tool. 
from __future__ import absolute_import
import argparse

def get_args():
    """ this function grabs input arguments from the command line """

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', help="The input file to use")
    parser.add_argument('-o', '--output-file', help="The output file to write to")

    args = parser.parse_args()

    return args

def my_function(input_file, output_file):
    """ A sample function """
    
    print("This is my input file: %s" % input_file)
    print("\nThis is my output file: %s" % output_file)

def main():
    """ The main routine to run """

    # Get the parameters
    args = get_args()

    # Run the function
    my_function(args.input_file, args.output_file)

# Define what to do when the script is run and not imported as a module
if __name__ == '__main__':
    main()
