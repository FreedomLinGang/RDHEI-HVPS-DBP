"""Single-process demo for the proposed RDHEI method.

Example:
    python main.py
    python main.py --image_dir ./imgs --save_images
    python main.py --image_dir D:/datasets/UCID --seed 42
"""

import argparse
import os

import cv2
import numpy as np

import config
from hide_recover import hide_infor_recover
from hide_stage import secret_infor_hide
from utils import get_image_files


def parse_args():
    parser = argparse.ArgumentParser(
        description="RDHEI with horizontal/vertical pixel shifting and dynamic block partitioning"
    )
    parser.add_argument("--image_dir", default=config.IMAGE_DIR, help="input image folder")
    parser.add_argument("--result_dir", default=config.RESULT_DIR, help="output folder")
    parser.add_argument("--s1", type=int, default=config.S1, help="outer block size (paper: 4)")
    parser.add_argument("--s2", type=int, default=config.S2, help="inner block size (paper: 2)")
    parser.add_argument("--seed", type=int, default=config.SEED, help="encryption/payload seed (paper: 42)")
    parser.add_argument("--save_images", action="store_true", help="save original/encrypted/stego/recovered images")
    parser.add_argument("--log", default=config.OUTPUT_LOG, help="text log path")
    return parser.parse_args()


def main():
    args = parse_args()
    config.SEED = args.seed
    os.makedirs(args.result_dir, exist_ok=True)

    name_files, image_files = get_image_files(args.image_dir)
    if not image_files:
        raise FileNotFoundError("No images found in {}".format(args.image_dir))

    embed_list = []
    name_list = []
    total_embed = 0.0

    with open(args.log, "w", encoding="utf-8") as txt_file:
        for i, (file, name_img) in enumerate(zip(image_files, name_files)):
            name_img_split = os.path.splitext(name_img)[0]
            print("[{}/{}] {}".format(i + 1, len(image_files), name_img), flush=True)

            embed_img, str_hide, xor_result, gray_img, row_mark, diff_auc = secret_infor_hide(
                file, args.s1, args.s2
            )
            recover_img, decrypt_str, auc_hide_bin = hide_infor_recover(
                embed_img, row_mark, args.s1, args.s2
            )

            h, w = gray_img.shape
            true_secret = str_hide[: len(decrypt_str)]
            embed_rate = np.round(len(decrypt_str + auc_hide_bin) / (h * w), 4)
            msg_ok = decrypt_str == true_secret
            img_ok = np.array_equal(gray_img, recover_img)

            total_embed += embed_rate
            embed_list.append(embed_rate)
            name_list.append(name_img_split)

            lines = [
                "image {}: {}".format(i, name_img),
                "secret extracted: {}".format("OK" if msg_ok else "FAIL"),
                "image recovered: {}".format("OK" if img_ok else "FAIL"),
                "auxiliary leftover bits: {}".format(diff_auc),
                "embedding rate: {} bpp".format(embed_rate),
                "=" * 50,
            ]
            report = "\n".join(lines)
            print(report, flush=True)
            txt_file.write(report + "\n")

            if args.save_images:
                cv2.imwrite(os.path.join(args.result_dir, name_img_split + "_ori.png"), gray_img)
                cv2.imwrite(os.path.join(args.result_dir, name_img_split + "_encrypt.png"), xor_result)
                cv2.imwrite(os.path.join(args.result_dir, name_img_split + "_stego.png"), embed_img)
                cv2.imwrite(os.path.join(args.result_dir, name_img_split + "_recover.png"), recover_img)

        max_value = max(embed_list)
        min_value = min(embed_list)
        avg_value = np.round(total_embed / len(embed_list), 4)
        summary = [
            "max ER: {} ({})".format(max_value, name_list[embed_list.index(max_value)]),
            "min ER: {} ({})".format(min_value, name_list[embed_list.index(min_value)]),
            "mean ER: {}".format(avg_value),
        ]
        summary_text = "\n".join(summary)
        print(summary_text)
        txt_file.write(summary_text + "\n")


if __name__ == "__main__":
    main()
