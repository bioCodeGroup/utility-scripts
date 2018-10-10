!/usr/bin/env python
"""
This code contains functions that are used in file conversion codes.
"""

#isfloat queries whether a value in quesion is a number or not
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

#isdna queries whether a sequence "maybeseq" is a DNA sequence or not 
# by looking for A, T, C, or G in the sequence
def isdna(maybeseq):
    if 'A' in maybeseq or 'C' in maybeseq or 'T' in maybeseq or 'G' in maybeseq:
        return True
    else:
        return False

if __name__ == '__main__':
    main()
