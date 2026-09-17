import cv2
import numpy as np

import config
from hide_record import hide_infor


def convert_2d_array_to_8bit_binary(arr):
    binary_str = ""
    for row in arr:
        for num in row:
            binary_num = "{:08b}".format(num)
            binary_str += binary_num
    return binary_str


def secret_infor_hide(img_path, s1, s2):
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError("Cannot read image: {}".format(img_path))

    if len(img.shape) == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = img

    height, width = gray_img.shape
    gray_img_array = gray_img.astype(int)

    # Paper: the same seed generates the XOR encryption key
    np.random.seed(config.SEED)
    random_array = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    xor_result = np.bitwise_xor(gray_img_array, random_array)

    h, w = gray_img_array.shape
    yushu_h = h % s1

    row_mark = -1
    if s1 == 4:
        row_mark = s1 * 4 + yushu_h
    elif s1 == 8:
        row_mark = s1 + yushu_h
    elif s1 == 16:
        row_mark = s1 + yushu_h

    auc_img = xor_result[:row_mark, :]
    infor_img = xor_result[row_mark:, :]
    random_infor_array = random_array[row_mark:, :]
    auc_img_bin = convert_2d_array_to_8bit_binary(auc_img)

    total_hide_len = height * width

    # Paper: the same seed independently generates the secret payload
    np.random.seed(config.SEED)
    str_hide_array = np.random.randint(0, 2, total_hide_len, dtype=np.uint8)
    str_hide = "".join(map(str, str_hide_array))
    total_str_hide = auc_img_bin + str_hide

    fiall_embed_result, diff_auc = hide_infor(
        infor_img, total_str_hide, random_infor_array, row_mark, s1, s2
    )

    return fiall_embed_result, str_hide, xor_result, gray_img_array, row_mark, diff_auc
