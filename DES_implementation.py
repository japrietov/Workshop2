# -*- coding: iso-8859-1 -*-

from itertools import repeat

# Convert each letter to binary
def convert_letter_to_binary(char):
    char_bin = bin(ord(char))[2:]
    if len(char_bin) < 8: char_bin = list(repeat("0", 8-len(char_bin))) + list(char_bin)
    return "".join(char_bin)

# From a given bitstring key of length 64, compress into 56 bits
def PC_1():
    pass


