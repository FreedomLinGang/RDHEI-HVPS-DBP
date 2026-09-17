# RDHEI-HVPS-DBP

Official implementation of:

**Reversible data hiding in encrypted images based on horizontal and vertical pixel shifting and dynamic block partitioning**

Gang Lin, Xianquan Zhang, Chunqiang Yu, Xuemao Zhang  
*Journal of King Saud University Computer and Information Sciences*, 2026, 38:184  
DOI: [10.1007/s44443-026-00558-0](https://doi.org/10.1007/s44443-026-00558-0)

本仓库只包含**本文提出方法**的复现代码，不包含 PSA / MPSA / rotation 等对比方案，也不包含消融实验代码。

---

## 方法简介

该方法在加密域完成可逆信息隐藏，包含两个核心模块：

1. **水平–垂直双向像素移位（HVPS）**  
   将加密图像块分别视为水平和垂直循环队列，通过像素置换嵌入信息，不改像素值，从而保持加密图像的直方图与信息熵。
2. **动态分块（DBP）**  
   以 `4×4` 为外层块，按可恢复性自适应决定：
   - 作为整体 `4×4` 嵌入，或
   - 再分成 4 个 `2×2` 子块嵌入  

论文默认参数：`s1=4, s2=2`，加密密钥与秘密信息随机种子均为 **42**。

当前 Python 实现对每块做穷举移位搜索，一张 `512×512` 图像大约需要 1–2 分钟（与机器有关）。论文报告的批量平均嵌入时间更短，但数量级仍明显高于 PSA 等单向移位方法。

在 BOWS-2、BOSSBase、UCID 上的平均嵌入率分别为 **0.7156 / 0.7241 / 0.6290 bpp**。

---

## 仓库结构

```text
RDHEI-HVPS-DBP/
├── main.py                 # 单进程演示 / 小规模测试
├── run_batch.py            # 多进程批量评测（BOSSBase / BOWS-2 / UCID）
├── hide_stage.py           # 图像加密 + 嵌入入口
├── hide_record.py          # 动态分块嵌入
├── hide_recover.py         # 信息提取与图像恢复
├── public_file.py          # 水平/垂直像素移位与平滑度判定
├── auc_infor_process.py    # 位置图 Huffman 辅助信息编码
├── get_all_infor.py        # 辅助信息解析与数据提取
├── config.py               # 论文默认参数
├── utils.py                # 读图工具
├── imgs/                   # 3 张示例图像
├── results/                # 运行输出
├── requirements.txt
├── LICENSE
└── CITATION.cff
```

---

## 环境

- Python 3.8+
- numpy
- opencv-python

```bash
pip install -r requirements.txt
```

---

## 快速开始

在仓库根目录运行：

```bash
python main.py --image_dir ./imgs --save_images
```

输出：

- 终端与 `results/output.txt`：每张图的嵌入率、秘密信息是否提取正确、图像是否可逆恢复
- `--save_images` 时在 `results/` 下保存：
  - `*_ori.png` 原始灰度图
  - `*_encrypt.png` 加密图
  - `*_stego.png` 载密图
  - `*_recover.png` 恢复图

自定义数据集：

```bash
python main.py --image_dir /path/to/images --seed 42
```

大规模评测（论文中的三个数据集）：

```bash
python run_batch.py --image_dir /path/to/BOSSbase_1.01 --workers 8 --log results/output_BOSS.txt
python run_batch.py --image_dir /path/to/BOWS2OrigEp3 --workers 8 --log results/output_BOWS2.txt
python run_batch.py --image_dir /path/to/UCID --workers 8 --log results/output_UCID.txt
```

支持的图像格式：`.png .jpg .bmp .tif .pgm` 等。

---

## 主要参数

| 参数 | 默认值 | 含义 |
| --- | --- | --- |
| `--s1` | 4 | 外层块大小（论文动态分块为 4×4） |
| `--s2` | 2 | 内层子块大小（2×2） |
| `--seed` | 42 | 加密密钥与秘密信息的随机种子 |

论文主实验固定 `seed=42`。文中 Table 10 另用 37–46 十组种子做了稳健性验证。

---

## 代码对应关系

| 文件 | 论文内容 |
| --- | --- |
| `public_file.py` 中 `embed_infor` / `mark_f_embed_rev` | 水平与垂直像素移位、最小平滑度恢复 |
| `hide_record.py` | 动态 4×4 / 2×2 分块嵌入与位置图 |
| `hide_stage.py` | XOR 加密、预留辅助信息行、嵌入流程 |
| `hide_recover.py` + `get_all_infor.py` | 辅助信息解码、数据提取、原图恢复 |

---

## 版本说明

工作目录中有多代实验代码。与本文最终方法对应的是：



- 恢复论文主实验的 `seed=42`（加密与恢复在函数内独立播种，保证密钥一致）
- 去掉对比方案、消融实验、调试脚本、大批量日志
- 增加命令行参数、`README`、`requirements.txt`、`.gitignore`



---

## Citation

```bibtex
@article{lin2026reversible,
  title   = {Reversible data hiding in encrypted images based on horizontal and vertical pixel shifting and dynamic block partitioning},
  author  = {Lin, Gang and Zhang, Xianquan and Yu, Chunqiang and Zhang, Xuemao},
  journal = {Journal of King Saud University Computer and Information Sciences},
  volume  = {38},
  pages   = {184},
  year    = {2026},
  doi     = {10.1007/s44443-026-00558-0}
}
```

---

## License

This code is released under the [MIT License](LICENSE).  
Please cite the paper if you use it in academic work.
