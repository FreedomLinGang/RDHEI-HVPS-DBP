from collections import Counter
import numpy as np
import heapq

def compute_min_rev(total_v,flatten_crop_random,h,w):

    a_array = np.array(total_v).reshape((h,w))
    b_array = np.array(flatten_crop_random).reshape((h,w))
    new_value = np.bitwise_xor(a_array, b_array)
    # 遍历两个列表，计算差值并求平方和
    # 水平方向（行方向）差分平方和
    horizontal_diff_squared = np.sum(np.diff(new_value, axis=1) ** 2)

    # 垂直方向（列方向）差分平方和
    vertical_diff_squared = np.sum(np.diff(new_value, axis=0) ** 2)
    total_sum = horizontal_diff_squared + vertical_diff_squared
    return total_sum


def mark_f_embed_rev(crop_f,random_crop,stride):

    h,w = crop_f.shape
    crop_f_len = crop_f.size
    differ_value = []

    diff_value = []

    secret_value = []

    for i in range(crop_f_len):

        flatten_crop_f_c = crop_f.flatten(order='F')
        flatten_crop_random = random_crop.flatten(order='C')
        total_v_c = flatten_crop_f_c[i:].tolist() + flatten_crop_f_c[:i].tolist()
        resize_crop_c = np.array(total_v_c).reshape((h,w)).T
        # square_sum = compute_min(total_v_c, flatten_random_crop)
        # square_sum = compute_min(total_v,flatten_crop_random)
        # diff_value.append(square_sum)
        # differ_value.append(total_v)
        for j in range(crop_f_len):


            flatten_crop_f = resize_crop_c.flatten(order='C')
            # flatten_crop_random = crop_random.flatten(order='F')
            total_v_f = flatten_crop_f[j:].tolist() + flatten_crop_f[:j].tolist()


            square_sum = compute_min_rev(total_v_f, flatten_crop_random,h,w)
            diff_value.append(square_sum)
            differ_value.append(total_v_f)
            true_i = (h*w-i) % (h*w)
            true_j = (h*w-j) % (h*w)
            secret_value.append([true_j,true_i])

    # bool_mark_f = has_duplicate_rows(differ_value)
    min_value = min(diff_value)
    min_index = np.argmin(diff_value)
    min_secret_value = secret_value[min_index]

    first_secret = min_secret_value[0]
    second_secret = min_secret_value[1]

    first_secret_srt = bin(first_secret)[2:].zfill(stride)
    second_secret_srt = bin(second_secret)[2:].zfill(stride)

    total_str = first_secret_srt + second_secret_srt

    min_crop_v = differ_value[min_index]
    resize_crop_v = np.array(min_crop_v).reshape((h,w))
    fiall_crop_v = np.bitwise_xor(resize_crop_v, random_crop)
    # print(f"水平移动和垂直移动数据分别为{first_secret},{second_secret}")
    # print(f"平滑度为{ min_value}")
    return total_str,fiall_crop_v

def embed_infor(crop_f,embed_str,stride):
    h,w = crop_f.shape

    hide_str_1 = embed_str[:stride]
    hide_str_2 = embed_str[stride:]

    decimal_number_1 = int(hide_str_1, 2)
    decimal_number_2 = int(hide_str_2, 2)

    flatten_crop_f_c = crop_f.flatten(order='C')
    total_v_c = flatten_crop_f_c[decimal_number_1:].tolist() + flatten_crop_f_c[:decimal_number_1].tolist()
    resize_crop_c = np.array(total_v_c).reshape((h,w))
    flatten_crop_f = resize_crop_c.flatten(order='F')
    # flatten_crop_random = crop_random.flatten(order='F')
    total_v_f = flatten_crop_f[decimal_number_2:].tolist() + flatten_crop_f[:decimal_number_2].tolist()
    resize_crop_f = np.array(total_v_f).reshape((h,w)).T

    return resize_crop_f

def decimal_to_binary(hide_img):
    hide_img_flatten = hide_img.reshape(-1)
    binary_str = ''
    for decimal in hide_img_flatten:
        binary = f"{decimal:08b}"
        # binary = bin(decimal)[2:]  # 将十进制转换为二进制字符串，去除开头的'0b'
        binary_str += binary

    # print(binary_str)
    return binary_str



def binary_to_decimal(binary_file_list):
    decimal_numbers = []
    # for binary in binary_file_list:
    for i in range(0,len(binary_file_list), 8):
        # print(i)
        binary_chunk = binary_file_list[i:i + 8]
        binary_string = ''.join([str(item) for item in binary_chunk])
        decimal_value = int(binary_string, 2)
        decimal_numbers.append(decimal_value)

    # auc_img = np.array(decimal_numbers).reshape(-1,512)
    return decimal_numbers


def num2binary(num, length):

    binary_str = bin(int(num))[2:].zfill(length)

    return binary_str



def dict_2_binary(dict_value):
    dict_length = len(dict_value)
    mark_count = 0
    length = 4
    dict_total_bin = num2binary(dict_length, length)
    total_str = ''+dict_total_bin
    for key, value in dict_value.items():

        dict_key_bin = num2binary(key, length)


        if isinstance(value, str):
            dict_value_len = len(value)
            dict_value_bin = num2binary(dict_value_len, length)
            # binary_bum = num_to_binary(value, length)
            total_str += (dict_key_bin + dict_value_bin + value)

        else:
            dict_value_bin = num2binary(int(value), length)
            total_str += (dict_key_bin + dict_value_bin)

    return  total_str


def binary2num(binary):

    decimal_result = int(binary, 2)

    return decimal_result



def binary_2_dict(bianry_value):
    dict_len_str = bianry_value[:4]
    dict_len = binary2num(dict_len_str)
    index = 4
    hoffman_dict = {}
    for j in range(dict_len):
        dict_key_str = bianry_value[index:index+4]
        dict_key = binary2num(dict_key_str)
        dict_value_len_str = bianry_value[index+4:index+8]
        dict_value_len = binary2num(dict_value_len_str)
        dict_value_str = bianry_value[index+8:index+8+dict_value_len]
        hoffman_dict[dict_key] = dict_value_str
        index += (8+dict_value_len)



    return  hoffman_dict



def hufuman_encode(F):
    counts = Counter(F.flatten())
    # new_total_count = sum(counts.values())
    # new_labels, new_values = zip(*counts.items())
    # # 计算总的出现次数
    # new_total_count = sum(counts.values())
    counts[3] += 1

    # new_rate_space = []
    # new_len_space = 0
    # new_access_space = 0



    # sorted_percentage = dict(sorted(rate_percentage.items(), key=lambda item: item[1], reverse=True))





    heap = [[weight, [symbol, ""]] for symbol, weight in counts.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    huffman_dict = dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))

    print(huffman_dict)


    # 将F列表中的index转换为霍夫曼编码
    encoded_F = []
    str_encodes = ''
    for index in F.flatten():
        if index in huffman_dict:
            encoded_F.append(huffman_dict[index])
            str_encodes+=huffman_dict[index]

    # print(encoded_F)
    len_encodes = len(str_encodes)
    return str_encodes,len_encodes,huffman_dict



def get_huffman_binary(hoffman_binary_list,hoffman_dict):
    temp = ''
    temp_index = 0
    total_mark = []
    for bit in hoffman_binary_list:
        # bit = total_remain_list[tt]
        temp += str(bit)
        temp_index += 1
        if temp in hoffman_dict:
            temp_f = hoffman_dict[temp]

            total_mark.append(temp_f)
            temp =''



    return total_mark