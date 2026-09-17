import numpy as np

import config
from get_all_infor import get_auc_infor, get_hide_infor
from public_file import binary_to_decimal


def hide_infor_recover(embed_result, row_mark, s1, s2):
    height, width = embed_result.shape
    yushu_w = width % s1

    np.random.seed(config.SEED)
    random_array = np.random.randint(0, 256, (height, width), dtype=np.uint8)

    auc_img = embed_result[:row_mark, :]
    infor_img = embed_result[row_mark:, :]
    auc_random_array = random_array[:row_mark, :]
    hide_random_array = random_array[row_mark:, :]

    all_auc_infor = get_auc_infor(auc_img, s1)
    decrypt_img, decrypt_str, remain_hide_infor = get_hide_infor(
        infor_img, all_auc_infor, hide_random_array, s1, s2
    )

    auc_ori_img_bin = decrypt_str[: width * 8 * row_mark]
    secret_infor_bin = decrypt_str[width * 8 * row_mark :]

    auc_encrypt_img = np.array(binary_to_decimal(auc_ori_img_bin)).reshape((-1, width))
    auc_ori_img = np.bitwise_xor(auc_encrypt_img, auc_random_array)

    result_ori_img = np.vstack((auc_ori_img, decrypt_img))
    final_ori_img = result_ori_img.copy()

    if yushu_w != 0:
        remain_region = result_ori_img[row_mark:, -yushu_w:]
        remain_radom = random_array[row_mark:, -yushu_w:]
        remain_xor = np.bitwise_xor(remain_region, remain_radom)
        final_ori_img[row_mark:, -yushu_w:] = remain_xor

    return final_ori_img, secret_infor_bin, remain_hide_infor
