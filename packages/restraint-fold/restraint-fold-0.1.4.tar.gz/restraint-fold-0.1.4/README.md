## 简化版蛋白质二级结构分类器
### 使用方法
- 首先通过pip进行安装：
```bash
$ python3 -m pip install restraint-fold --upgrade -i https://pypi.org/simple
```
- 然后直接在命令行进行使用：
```bash
$ python3 -m fold -h
usage: __main__.py [-h] [-i I] [-o O] [-oh OH] [--simplified SIMPLIFIED] [--addh ADDH]

optional arguments:
  -h, --help            show this help message and exit
  -i I                  Set the input pdb file path.
  -o O                  Set the output txt file path.
  -oh OH                Write the hbonds into txt file.
  --simplified SIMPLIFIED
                        Return the simplified information, default to be 0.
  --addh ADDH           Decide to rebuild hydrogen atoms or not, default to be 0.
```

### 示例
- 执行一个生成完整的alpha和beta序列的命令：
```bash
$ python3 -m fold -i examples/pdb/case2-optimized.pdb -o examples/case2-secondary.txt
Analysing alpha:
100%|████████████████████████████████████████████████████████████████████████████████████████████| 154/154 [00:00<00:00, 14563.23it/s]
Analysing beta:
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 746/746 [00:00<00:00, 6425.08it/s]
```
得到的结果如下所示：
```txt
# case2-secondary.txt
alpha:
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 31 32 33 34 35 36 37 39 40 41 42 43 44 45 46 78 79 80 81 82 83 84 85 86 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109
beta:
23 24 25 26 27 28 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 93 94 95 96 97 98 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157
```

```bash
$ python3 -m fold -i examples/pdb/case2-optimized.pdb -o examples/case2-secondary.txt --simplified 1
Analysing alpha:
100%|████████████████████████████████████████████████████████████████████████████████████████████| 154/154 [00:00<00:00, 17623.61it/s]
Analysing beta:
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 746/746 [00:00<00:00, 6416.04it/s]
```
得到的结果如下所示：
```txt
# case2-secondary.txt
alpha:
1~25
31~37
39~46
78~86
94~109

beta:
23~28
46~72
93~98
118~157
```
### 提示
如果输入的pdb文件中氢原子有缺失，需要加上`--addh 1`自动补充氢原子的选项，或者手动通过Xponge或者Hadder等工具进行补氢，然后再对结构进行解析：
```bash
$ python3 -m fold -i examples/pdb/case2.pdb -o examples/case2-secondary.txt --simplified 1 --addh 1
1 H-Adding task with 2529 atoms complete in 0.09 seconds.
The new pdb file path is in: /tmp/restraint-fold/92de3be6-12f6-11ee-b491-b07b25070cd2.pdb
Analysing alpha:
100%|████████████████████████████████████████████████████████████████████████████████████████████| 154/154 [00:00<00:00, 15845.42it/s]
Analysing beta:
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 746/746 [00:00<00:00, 6003.69it/s]
```
