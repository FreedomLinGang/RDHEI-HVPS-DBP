
from public_file import *



def auc_infor2_bin(mark_data,three_loc,three_loc_infor,eight_loc_infor):
    class_str_index ,class_encodes_lens ,huffman_dict = hufuman_encode(mark_data)



    three_loc_len = len(three_loc)
    three_loc_infor_len = len(three_loc_infor)
    eight_loc_infor_len = len(eight_loc_infor)

    huffman_dict_bin = dict_2_binary(huffman_dict)
    huffman_dict_len = len(huffman_dict_bin)
    # huffman_dict_rev = binary_2_dict(huffman_dict_bin)

    three_loc_len_bin = num2binary(three_loc_len, 16)
    three_loc_infor_len_bin = num2binary(three_loc_infor_len, 16)
    eight_loc_infor_len_bin = num2binary(eight_loc_infor_len, 16)
    huffman_dict_len_bin = num2binary( huffman_dict_len, 8)
    class_encodes_lens_bin = num2binary(class_encodes_lens,16)


    auc_total_str = huffman_dict_len_bin + class_encodes_lens_bin+three_loc_len_bin+three_loc_infor_len_bin+eight_loc_infor_len_bin\
                +huffman_dict_bin+class_str_index+three_loc +three_loc_infor+eight_loc_infor


    auc_total_str_len = len(auc_total_str)

    temp_auc_total_str_len = auc_total_str_len-eight_loc_infor_len-three_loc_infor_len
    print("auxiliary information length: {}".format(temp_auc_total_str_len), flush=True)
    # np.random.seed(42)
    #
    # # 生成512x512的二维数组，元素在0到255之间
    # auc_random_array = np.random.randint(0, 256,auc_total_str_len , dtype=np.uint8)
    # # 进行按位异或操作
    # auc_encry_result = np.bitwise_xor(auc_total_str, auc_random_array)


    return auc_total_str,auc_total_str_len