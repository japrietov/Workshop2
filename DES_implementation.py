# -*- coding: iso-8859-1 -*-

from itertools import repeat
import re

# Convert each letter to binary
def convert_letter_to_binary(char):
    char_bin = bin(ord(char))[2:]
    if len(char_bin) < 8: char_bin = list(repeat("0", 8-len(char_bin))) + list(char_bin)
    return "".join(char_bin)

# Check length of the key
def check_len_key(key):
    if len(key) == 8:
        return "".join([convert_letter_to_binary(letter) for letter in list(key)])
    else:
        return ""

# From a given bitstring key of length 64, compress into 56 bits
def PC_1(key):
    if check_len_key(key) != "":

        current_key = check_len_key(key)
        # current_key = "0001001100110100010101110111100110011011101111001101111111110001"
        # test_key = "11110000110011001010101011110101010101100110011110001111"
        chunks_key = list(reversed(re.findall('........', current_key)))

        # Left part of the key
        key_prime_left = []
        for i in xrange(4):
            for chunk in chunks_key:
                key_prime_left.append(chunk[i])

        # Right part of the key
        key_prime_right = []
        for j in xrange(6,2,-1):
            for chunk in chunks_key:
                key_prime_right.append(chunk[j])

        # Join between left and right part, deleting the last 4 bits.
        return "".join(key_prime_left[:len(key_prime_left)-4] + key_prime_right[:len(key_prime_right)-4])

    else:
        return "Wrong length key"


