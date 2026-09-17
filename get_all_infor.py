
from public_file import *
import numpy as np



def get_auc_infor(auc_img,s1):
    h,w = auc_img.shape
    get_auc_infor_bin = decimal_to_binary(auc_img)

    cut_point = 0

    get_huffman_dict_len = get_auc_infor_bin[cut_point:cut_point+8]
    get_class_encodes_lens = get_auc_infor_bin[cut_point+8:cut_point + 24]
    get_three_loc_len_bin = get_auc_infor_bin[cut_point+24:cut_point+40]
    get_three_loc_infor_len = get_auc_infor_bin[cut_point+40:cut_point+56]
    get_eight_loc_infor_len = get_auc_infor_bin[cut_point+56:cut_point+72]

    cut_point += 72

    get_huffman_dict_dec = binary2num(get_huffman_dict_len)
    get_class_encodes_dec = binary2num(get_class_encodes_lens)
    get_three_loc_len_dec = binary2num(get_three_loc_len_bin)
    get_three_loc_infor_dec = binary2num( get_three_loc_infor_len)
    get_eight_loc_infor_dec = binary2num(get_eight_loc_infor_len)

    huffman_dict_bin = get_auc_infor_bin[cut_point:cut_point+get_huffman_dict_dec]
    cut_point += get_huffman_dict_dec

    class_encodes_bin = get_auc_infor_bin[cut_point:cut_point + get_class_encodes_dec]
    cut_point += get_class_encodes_dec

    three_loc_len_bin = get_auc_infor_bin[cut_point:cut_point + get_three_loc_len_dec]
    cut_point += get_three_loc_len_dec

    get_three_loc_infor_bin = get_auc_infor_bin[cut_point:cut_point + get_three_loc_infor_dec]
    cut_point += get_three_loc_infor_dec

    eight_loc_infor_bin = get_auc_infor_bin[cut_point:cut_point + get_eight_loc_infor_dec]
    cut_point += get_eight_loc_infor_dec

    remain_hide_infor = get_auc_infor_bin[cut_point:]

    huffman_dict = binary_2_dict(huffman_dict_bin)
    reversed_hoffman_dict = {value: key for key, value in huffman_dict.items()}

    mark_hide_img = np.array(get_huffman_binary(class_encodes_bin, reversed_hoffman_dict)).reshape(-1, w//s1)




    return [mark_hide_img,three_loc_len_bin,get_three_loc_infor_bin,eight_loc_infor_bin,remain_hide_infor]




def get_hide_infor(infor_img,all_auc_infor,random_array,s1,s2):
    mark_hide_img = all_auc_infor[0]
    three_loc_len_bin = all_auc_infor[1]
    three_loc_infor_bin = all_auc_infor[2]
    eight_loc_infor_bin = all_auc_infor[3]
    remain_hide_infor = all_auc_infor[4]

    mark_w,mark_h = mark_hide_img.shape

    decrypt_str = ''
    three_loc_count =0
    three_loc_infor_count =0
    eight_loc_count = 0

    hide_s1 = int(2*np.log2(s1*s1))
    hide_s2 = int(2*np.log2(s2*s2))

    decrypt_img = infor_img.copy()
    for i in range(mark_w):

        for j in range(mark_h):



            temp_mark = mark_hide_img[i,j]

            crop_f_4 = infor_img[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1]
            random_crop_4 = random_array[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1]




            if temp_mark == 1:
                decrypt_str += eight_loc_infor_bin[eight_loc_count:eight_loc_count+hide_s1]
                rev_crop_v_4 = np.bitwise_xor(crop_f_4, random_crop_4)

                eight_loc_count += hide_s1
                decrypt_img[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = rev_crop_v_4
            elif temp_mark == 2:
                hide_rev_str_4, fiall_crop_v_4 = mark_f_embed_rev(crop_f_4, random_crop_4, hide_s1//2)
                decrypt_str += hide_rev_str_4
                decrypt_img[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = fiall_crop_v_4
            elif temp_mark == 3:


                temp_3_loc_bin = three_loc_len_bin[three_loc_count:three_loc_count+2]
                temp_3_loc_mark = binary2num(temp_3_loc_bin)



                temp_rev_2 = np.zeros((s1, s1))
                temp_3_infor_bin = three_loc_infor_bin[three_loc_infor_count:three_loc_infor_count+hide_s2]
                for p in range(2):
                    for q in range(2):
                        temp_index = p * 2 + q


                        crop_f_2 = crop_f_4[p * s2:(p + 1) * s2, q * s2:(q + 1) * s2]
                        random_crop_2 = random_crop_4[p * s2:(p + 1) *s2, q * s2:(q + 1) * s2]
                        if temp_index == temp_3_loc_mark:

                            rev_crop_v_2 = np.bitwise_xor(crop_f_2,random_crop_2)

                            temp_rev_2[p*s2:(p+1)*s2,q*s2:(q+1)*s2] = rev_crop_v_2
                            decrypt_str += temp_3_infor_bin
                        else:

                            hide_rev_str_2, fiall_crop_v_2 = mark_f_embed_rev(crop_f_2, random_crop_2, hide_s2//2)
                            temp_rev_2[p * s2:(p + 1) * s2, q * s2:(q + 1) * s2] = fiall_crop_v_2
                            decrypt_str += hide_rev_str_2
                three_loc_count += 2
                three_loc_infor_count += hide_s2
                decrypt_img[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = temp_rev_2
            elif temp_mark == 4:






                temp_rev_2 = np.zeros((s1, s1))

                for p in range(2):
                    for q in range(2):



                        crop_f_2 = crop_f_4[p * s2:(p + 1) * s2, q * s2:(q + 1) * s2]
                        random_crop_2 = random_crop_4[p * s2:(p + 1) * s2, q * s2:(q + 1) * s2]



                        hide_rev_str_2, fiall_crop_v_2 = mark_f_embed_rev(crop_f_2, random_crop_2, hide_s2//2)
                        temp_rev_2[p * s2:(p + 1) * s2, q * s2:(q + 1) * s2] = fiall_crop_v_2
                        decrypt_str += hide_rev_str_2
                decrypt_img[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = temp_rev_2


    return decrypt_img, decrypt_str,remain_hide_infor