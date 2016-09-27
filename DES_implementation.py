# -*- coding: iso-8859-1 -*-


# Authors: Jeisson Andres Prieto Velandia
#          David Santiago Barrera

# Supplementary Material DES.
# https://en.wikipedia.org/wiki/DES_supplementary_material



## -*- coding: latin-1 -*-
from itertools import repeat
import math
import re
import random

def fill_to8(string_to_expand):
    size = int( math.ceil( len( string_to_expand )/ float(8)) * 8)
    return (string_to_expand * ((size/len(string_to_expand))+1))[:size]

# Convert each letter to binary
def convert_letter_to_binary(char):
    char_bin = bin(ord(char))[2:]
    if len(char_bin) < 8: char_bin = list(repeat("0", 8-len(char_bin))) + list(char_bin)
    return "".join(char_bin)

def convert_binary_to_letter(string):
    num = int(string,2)
    letter = chr(num)
    #letter = str(num)+'-'
    return letter

# Check length of the key
def check_len_key(key):
    return "".join([convert_letter_to_binary(letter) for letter in list(key)])

# From a given bitstring key of length 64, compress into 56 bits
def PC_1(key):
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

# Rotate n bits to the left
def shiftLbyn(arr, n):
    return arr[n::] + arr[:n:]

# Rotate n bits to the right
def shiftRbyn(arr, n=0):
    n = len(arr) - n
    return arr[n::] + arr[:n:]


# Permutation P
def permutation_P(f_inner):
    matrix_f_inner = [[16, 7, 20, 21, 29, 12, 28, 17],
                      [1, 15, 23, 26, 5, 18, 31, 10],
                      [2, 8, 24, 14, 32, 27, 3, 9],
                      [19, 13, 30, 6, 22, 11, 4, 25]]

    p_out = []
    for rows in matrix_f_inner:
        for cols in rows:
            p_out.append(f_inner[cols - 1])

    return "".join(p_out)

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

# Final permutation IP-1
def final_permutation(l_last, r_last):
    matrix_final_permutation = [[40, 8, 48, 16, 56, 24, 64, 32],
                                [39, 7, 47, 15, 55, 23, 63, 31],
                                [38, 6, 46, 14, 54, 22, 62, 30],
                                [37, 5, 45, 13, 53, 21, 61, 29],
                                [36, 4, 44, 12, 52, 20, 60, 28],
                                [35, 3, 43, 11, 51, 19, 59, 27],
                                [34, 2, 42, 10, 50, 18, 58, 26],
                                [33, 1, 41, 9, 49, 17, 57, 25]]


    message_final = r_last + l_last
    cipher_text = []
    for row in matrix_final_permutation:
        for col in row:
            cipher_text.append(message_final[col-1])

    return "".join(cipher_text)

# Expansion Function E
def expansion(right_part):
    matrix_expansion = [[32, 1, 2, 3, 4, 5],
                        [4, 5, 6, 7, 8, 9],
                        [8, 9, 10, 11, 12, 13],
                        [12, 13, 14, 15, 16, 17],
                        [16, 17, 18, 19, 20, 21],
                        [20, 21, 22, 23, 24, 25],
                        [24, 25, 26, 27, 28, 29],
                        [28, 29, 30, 31, 32, 1]]

    right_expanded = []
    for row in matrix_expansion:
        for col in row:
            right_expanded.append(right_part[col-1])

    return "".join(right_expanded)

# S-box
def S_box(B_i, i_box):
    row_index = int(B_i[0]+B_i[5],2)
    col_index = int(B_i[1:5],2)

    sBox = []

    sBox.append([[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])

    sBox.append([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])

    sBox.append([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])

    sBox.append([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])

    sBox.append([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])

    sBox.append([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])

    sBox.append([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])

    sBox.append([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])

    value = bin(sBox[i_box][row_index][col_index])[2:]
    if len(value) < 4: value = list(repeat("0", 4 - len(value))) + list(value)
    return "".join(value)

# Compute R_i, L_i
def compute_next_R_L(left_0, right_0, key_dict):
    dict_Li = {}
    dict_Ri = {}
    current_L_i = left_0
    current_R_i = right_0

    for index in xrange(1, 17):
        dict_Li[index] = current_R_i
        tmp_solution_Ri = bin(int(current_L_i, 2) ^ int(inner_function(current_R_i, key_dict[index]),2))[2:]
        if len(tmp_solution_Ri) < 32: tmp_solution_Ri = list(repeat("0", 32 - len(tmp_solution_Ri))) + list(tmp_solution_Ri)
        dict_Ri[index] = "".join(tmp_solution_Ri)

        current_L_i = dict_Li[index]
        current_R_i = dict_Ri[index]

    return dict_Li, dict_Ri


def d_compute_next_R_L(left_0, right_0, key_dict):
    dict_Li = {}
    dict_Ri = {}
    current_L_i = left_0
    current_R_i = right_0

    for index in xrange(16,0,-1):
        dict_Li[index] = current_R_i
        tmp_solution_Ri = bin(int(current_L_i, 2) ^ int(inner_function(current_R_i, key_dict[index]),2))[2:]
        if len(tmp_solution_Ri) < 32: tmp_solution_Ri = list(repeat("0", 32 - len(tmp_solution_Ri))) + list(tmp_solution_Ri)
        dict_Ri[index] = "".join(tmp_solution_Ri)

        current_L_i = dict_Li[index]
        current_R_i = dict_Ri[index]

    return dict_Li, dict_Ri

# Inner function f
def inner_function(right_part, key_i):
    right_expansion = expansion(right_part)
    k_xor_right = bin(int(right_expansion,2) ^ int(key_i,2))[2:]
    if len(k_xor_right) < 48: k_xor_right = list(repeat("0", 48 - len(k_xor_right))) + list(k_xor_right)

    B_i_list  =re.findall('......', "".join(k_xor_right))

    B_list_S_box = []
    for i in xrange(8):
        B_list_S_box.append(S_box(B_i_list[i], i))

    return permutation_P("".join(B_list_S_box))

def check_plain_text(plain_text):
    completed_string = plain_text if len(plain_text) % 8 == 0 else fill_to8(plain_text)
    return list(re.findall('........', completed_string))

def string_to_bin(strings):
    binary_strings = []
    for string in strings:
        binary_strings.append("".join([convert_letter_to_binary(letter) for letter in list(string)]))
    return binary_strings

def array_to_string(binary_array):
    string = ""
    for array in binary_array:
        to_print = re.findall('........', array)
        for item in to_print:
            string += convert_binary_to_letter(item)
    return string.decode("latin-1")

def Cipher_Block_Chaining_encoder(cipher_text, message):
    part_tmp = bin(int(cipher_text, 2) ^ int(message, 2))[2:]
    if len(part_tmp) < 64: part_tmp = list(repeat("0", 64 - len(part_tmp))) + list(part_tmp)
    current_cipher = "".join(shiftLbyn(part_tmp, 32))
    return current_cipher


def Cipher_Block_Chaining_decoder(cipher_text_i, cipher_text_iplus1):
    part_tmp = bin(int(cipher_text_i, 2) ^ int("".join(shiftRbyn(cipher_text_iplus1, 32)), 2))[2:]
    if len(part_tmp) < 64: part_tmp = list(repeat("0", 64 - len(part_tmp))) + list(part_tmp)
    return part_tmp


initial_value = "1111010100011010101011110001001110000000001100000001000100011000"


def DES_Encryption(plain_text, key):
    text = check_plain_text(plain_text)
    binary_strings = string_to_bin(text)

    encrypted_strings = []

    key = key[:8] if len(key) >= 8 else fill_to8(key)
    generated_keys = key_generator(key)

    current_value = initial_value
    print binary_strings
    for string in binary_strings:
        in_perm = initial_permutation(Cipher_Block_Chaining_encoder(current_value, string))
        dic_l, dic_r = compute_next_R_L(in_perm[:len(string) / 2], in_perm[len(string) / 2:], generated_keys)
        cipher_text = final_permutation(dic_l[16], dic_r[16])

        current_value = cipher_text

        encrypted_strings.append(cipher_text)

    return encrypted_strings, len(plain_text)


def DES_Decryption(cipher_text, key):

    decrypted_strings = []

    key = key[:8] if len(key) >= 8 else fill_to8(key)
    generated_keys = key_generator(key)

    current_value = initial_value
    cipher_text = [convert_letter_to_binary(x) for x in cipher_text]
    cipher_text_1 = re.findall('.{64}', "".join(cipher_text))
    print len(cipher_text_1)
    for string in cipher_text_1:
        in_perm = initial_permutation(string)
        dic_l, dic_r = d_compute_next_R_L(in_perm[:len(string) / 2], in_perm[len(string) / 2:], generated_keys)

        cipher_text = final_permutation(dic_l[1], dic_r[1])
        decrypted_strings.append("".join(Cipher_Block_Chaining_decoder(current_value, cipher_text)))
        current_value = string
    return decrypted_strings

#####################
# NO ELIMINAR!!
#####################

import sys
import codecs

if __name__ == "__main__":
    input_text = codecs.open(sys.argv[1], "r", "iso-8859-1").read()
    key = codecs.open(sys.argv[2],"r", "iso-8859-1").read()
    x = raw_input("What would you like to do encrypt(1)/decrypt(2): ")
    if x == "1":
        print "Your input was: ", input_text
        print "with the key: ", key
        print
        print "The cipher text is: "
        print
        encrypted, length = DES_Encryption(input_text, key)
        file = codecs.open('cipher_text.txt', "w", "iso-8859-1")
        file.write(array_to_string(encrypted))
        file.close()
        print array_to_string(encrypted)
        print
    elif x == "2":
        print "Your cipher text was: ", input_text
        print "with the key: ", key
        print
        print "The message is: "
        print
        decrypt = DES_Decryption(input_text, key)
        print array_to_string(decrypt)
        print
    else:
        print "Wrong choice"



