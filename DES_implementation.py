# -*- coding: iso-8859-1 -*-


# Authors: Jeisson Andres Prieto Velandia
#          David Santiago Barrera

# Supplementary Material DES.
# https://en.wikipedia.org/wiki/DES_supplementary_material


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

# Rotate n bits to the left
def shiftLbyn(arr, n):
    return arr[n::] + arr[:n:]

# PC - 2,
def PC_2(key_Ci_Di):
    permutation_matrix = [[14, 17, 11, 24, 1, 5],
                          [3, 28, 15, 6, 21, 10],
                          [23, 19, 12, 4, 26, 8],
                          [16, 7, 27, 20, 13, 2],
                          [41, 52, 31, 37, 47, 55],
                          [30, 40, 51, 45, 33, 48],
                          [44, 49, 39, 56, 34, 53],
                          [46, 42, 50, 36, 29, 32]]

    pc_2_key = []
    for rows in permutation_matrix:
        for cols in rows:
            pc_2_key.append(key_Ci_Di[cols-1])

    return "".join(pc_2_key)

# Key generator.
def key_generator(key):
    twice_rotations = [1, 2, 9, 16]
    key_prime = PC_1(key)
    dict_keys_c = {}
    dict_keys_d = {}

    complete_dict = {}

    current_key_c = key_prime[:28]
    current_key_d = key_prime[28:]

    for index in xrange(1,17):
        if index in twice_rotations:
            dict_keys_c[index] = shiftLbyn(current_key_c, 1)
            dict_keys_d[index] = shiftLbyn(current_key_d, 1)
        else:
            dict_keys_c[index] = shiftLbyn(current_key_c, 2)
            dict_keys_d[index] = shiftLbyn(current_key_d, 2)

        current_key_c = dict_keys_c[index]
        current_key_d = dict_keys_d[index]

        complete_dict[index] = PC_2(current_key_c + current_key_d)

    return complete_dict

# Initial Permutation IP.
def initial_permutation(message):
    initial_permutation_matrix = [[58, 50,	42, 34,	26, 18, 10, 2],
                                  [60, 52,	44, 36,	28, 20, 12, 4],
                                  [62, 54,	46, 38,	30, 22, 14, 6],
                                  [64, 56,	48, 40,	32, 24, 16, 8],
                                  [57, 49,	41, 33,	25, 17, 9, 1],
                                  [59, 51,	43, 35,	27, 19, 11, 3],
                                  [61, 53,	45, 37,	29, 21, 13, 5],
                                  [63, 55,	47, 39,	31, 23, 15, 7]]

    message_prime = []
    for row in initial_permutation_matrix:
        for col in row:
            message_prime.append(message[col-1])

    return "".join(message_prime)



#####################
# NO ELIMINAR!!
#####################
message_test = "0000000100100011010001010110011110001001101010111100110111101111"

key_test = "".join([chr(19), chr(52), chr(87), chr(121), chr(155), chr(188), chr(223), chr(241)])

test_key_prime = "11110000110011001010101011110101010101100110011110001111"

tmp = key_generator(key_test)
#for i in tmp:
#    print tmp[i]

print initial_permutation(message_test)



