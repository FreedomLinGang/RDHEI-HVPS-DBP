"""Multiprocess batch evaluation used for BOSSBase / BOWS-2 / UCID.

Example:
    python run_batch.py --image_dir D:/datasets/BOSSbase_1.01 --workers 8
"""

import argparse
import os
import time
import multiprocessing

import numpy as np

import config
from hide_recover import hide_infor_recover
from hide_stage import secret_infor_hide
from utils import get_image_files


def parse_args():
    parser = argparse.ArgumentParser(description="Batch evaluation of the proposed RDHEI method")
    parser.add_argument("--image_dir", required=True, help="dataset folder")
    parser.add_argument("--s1", type=int, default=config.S1)
    parser.add_argument("--s2", type=int, default=config.S2)
    parser.add_argument("--seed", type=int, default=config.SEED)
    parser.add_argument("--workers", type=int, default=max(os.cpu_count() - 1, 1))
    parser.add_argument("--log", default=config.OUTPUT_LOG)
    return parser.parse_args()


def process_one(item):
    name_img, index, image_dir, s1, s2, seed = item
    config.SEED = seed
    img_path = os.path.join(image_dir, name_img)

    embed_img, str_hide, _, gray_img, row_mark, diff_auc = secret_infor_hide(img_path, s1, s2)
    recover_img, decrypt_str, auc_hide_bin = hide_infor_recover(embed_img, row_mark, s1, s2)

    h, w = gray_img.shape
    true_secret = str_hide[: len(decrypt_str)]
    embed_rate = float(np.round(len(decrypt_str + auc_hide_bin) / (h * w), 4))
    err_count = 0 if (decrypt_str == true_secret and np.array_equal(gray_img, recover_img)) else 1

    report = "\n".join(
        [
            "image {}: {}".format(index, name_img),
            "secret extracted: {}".format("OK" if decrypt_str == true_secret else "FAIL"),
            "image recovered: {}".format("OK" if np.array_equal(gray_img, recover_img) else "FAIL"),
            "auxiliary leftover bits: {}".format(diff_auc),
            "embedding rate: {} bpp".format(embed_rate),
            "=" * 50,
        ]
    )
    print(report)
    return report, embed_rate, name_img, err_count


def main():
    args = parse_args()
    config.SEED = args.seed
    os.makedirs(os.path.dirname(os.path.abspath(args.log)) or ".", exist_ok=True)

    name_files, _ = get_image_files(args.image_dir)
    if not name_files:
        raise FileNotFoundError("No images found in {}".format(args.image_dir))

    tasks = [
        (name, i, args.image_dir, args.s1, args.s2, args.seed)
        for i, name in enumerate(name_files)
    ]

    start_time = time.time()
    all_rate = []
    all_name = []
    err_counts = 0
    total_rate = 0.0

    with open(args.log, "w", encoding="utf-8") as txt_file:
        with multiprocessing.Pool(processes=args.workers) as pool:
            for report, rate, name, err in pool.imap(process_one, tasks, chunksize=1):
                txt_file.write(report + "\n")
                txt_file.flush()
                all_rate.append(rate)
                all_name.append(name)
                err_counts += err
                total_rate += rate

        max_value = max(all_rate)
        min_value = min(all_rate)
        avg_value = np.round(total_rate / len(all_rate), 4)
        elapsed = time.time() - start_time
        summary = "\n".join(
            [
                "max ER: {} ({})".format(max_value, all_name[all_rate.index(max_value)]),
                "min ER: {} ({})".format(min_value, all_name[all_rate.index(min_value)]),
                "mean ER: {}".format(avg_value),
                "extraction/recovery errors: {}".format(err_counts),
                "elapsed seconds: {}".format(elapsed),
            ]
        )
        print(summary)
        txt_file.write(summary + "\n")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
