
import numpy as np
from public_file import *
from auc_infor_process import *







def hide_infor(F,str_hide,random_infor_array,row_mark,s1,s2):


    hide_s1 = int(2*np.log2(s1*s1))
    hide_s2 = int(2*np.log2(s2*s2))

    # true_coords_argwhere = np.argwhere(mark_embed)
    h,w = F.shape
    mark_h,mark_w = F.shape[0]//s1, F.shape[1]//s1
    embed_F = np.zeros_like(F)
    total_count = 0


    mark_data = np.zeros((mark_h,mark_w))

    new_embed_data = F.copy()

    three_loc = ''
    three_loc_infor = ''
    eight_loc_infor = ''


    for i in range(mark_h):
        for j in range(mark_w):
            # print(i,j)
            # if i == 41 and j ==57:
            #     print('==============')
            hide_str = str_hide[total_count:total_count + hide_s2*4]
            hide_str_4 = str_hide[total_count:total_count + hide_s1]

            crop_f = F[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1]
            random_crop = random_infor_array[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1]

            true_crop = np.bitwise_xor(crop_f, random_crop)
            # if j == 1:
            #     print(f"隐藏的信息为{hide_str}")
            #     print(f"真实值为{true_crop}")
            #     print(f"随机值为{random_crop}")
            #     print(f"加密值为{crop_f}")





            temp_embed_2 = np.zeros((s1,s1))
            temp_mark_2 =  np.ones((2,2))
            for p in range(2):
                for q in range(2):
                    temp_index = p*2+q
                    hide_str_2 = hide_str[temp_index*hide_s2:(temp_index+1)*hide_s2]
                    crop_f_2 = crop_f[p*s2:(p+1)*s2,q*s2:(q+1)*s2]
                    random_crop_2 = random_crop[p*s2:(p+1)*s2,q*s2:(q+1)*s2]


                    embed_corp_f_2 = embed_infor(crop_f_2, hide_str_2,hide_s2//2)
                    hide_rev_str_2, fiall_crop_v_2 = mark_f_embed_rev(embed_corp_f_2, random_crop_2,hide_s2//2)
                    if hide_str_2 != hide_rev_str_2:
                        # rev_crop_v_2 = np.bitwise_xor(crop_f_2, random_crop_2)
                        temp_mark_2[p,q] = 0
                        temp_embed_2[p*s2:(p+1)*s2,q*s2:(q+1)*s2] = crop_f_2
                    else:
                        temp_embed_2[p * s2:(p + 1) * s2, q * s2:(q + 1) * s2] = embed_corp_f_2

            temp_sum_2 = np.sum(temp_mark_2)

            if temp_sum_2 == 3:
                temp_mark_flat = temp_mark_2.flatten(order='C')
                zeros_index = int((np.where(temp_mark_flat==0)[0]))
                three_save_infor = hide_str[zeros_index*hide_s2:(zeros_index+1)*hide_s2]

                zeros_index_bin = bin(zeros_index)[2:].zfill(2)
                three_loc += zeros_index_bin

                three_loc_infor += three_save_infor

                new_embed_data[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = temp_embed_2

                mark_data[i, j] =3
                total_count += hide_s2*4
            elif temp_sum_2 == 4:
                mark_data[i, j] = 4
                new_embed_data[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = temp_embed_2
                total_count += hide_s2*4

            else:

                embed_corp_f_4 = embed_infor(crop_f, hide_str_4,hide_s1//2)
                hide_rev_str_4, fiall_crop_v_4 = mark_f_embed_rev(embed_corp_f_4, random_crop, hide_s1//2)
                if hide_str_4 != hide_rev_str_4:
                    mark_data[i, j] = 1

                    eight_loc_infor += hide_str_4
                    new_embed_data[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = crop_f
                else:
                    mark_data[i, j] = 2
                    new_embed_data[i * s1:(i + 1) * s1, j * s1:(j + 1) * s1] = embed_corp_f_4
                total_count += hide_s1

    sum_1 = np.sum((mark_data == 1))
    sum_2 = np.sum((mark_data == 2))
    sum_3 = np.sum((mark_data == 3))
    sum_4 = np.sum((mark_data == 4))

    print("non-embeddable 4x4 blocks: {}".format(sum_1), flush=True)
    print("4x4 blocks embedding {} bits: {}".format(hide_s1, sum_2), flush=True)
    print("blocks embedding {} bits (3 of 4 sub-blocks): {}".format(hide_s2 * 3, sum_3), flush=True)
    print("blocks embedding {} bits (4 sub-blocks): {}".format(hide_s2 * 4, sum_4), flush=True)
    # a = len(three_loc_infor)
    # b = len(eight_loc_infor)
    auc_infor_bin,auc_total_str_len = auc_infor2_bin(mark_data, three_loc, three_loc_infor, eight_loc_infor)


    # print(f'图像的辅助信息长度为：{auc_total_str_len}')

    diff_auc = row_mark*w*8 - auc_total_str_len

    if diff_auc < 0:
        print("auxiliary information exceeds reserved room by {} bits".format(-diff_auc), flush=True)
        auc_infor_bin = auc_infor_bin[:row_mark*w*8]

    remain_infor_len = max(row_mark*w*8 - auc_total_str_len,0)


    print("-------------------------------------------")

    remain_random_array = np.random.randint(0, 2,remain_infor_len , dtype=np.uint8)
    remain_str_hide = ''.join(map(str, remain_random_array))
    total_auc_bin = auc_infor_bin + remain_str_hide

    auc_embed_img = np.array(binary_to_decimal(total_auc_bin)).reshape((-1,w))
    fiall_embed_result = np.vstack((auc_embed_img, new_embed_data))



    return fiall_embed_result, diff_auc