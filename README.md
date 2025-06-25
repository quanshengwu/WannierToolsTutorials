# README

## 目录结构

```bash
wt2025/
├── bin/                              # 可执行文件目录，包含 wt.x, wannier90.x 等（在自己的集群上需要自己编译安装）
├── examples/                         # 示例输入文件和教程资料
├── WannierTools_tutorial_2024_liyang.pdf  # 中文版 WannierTools 使用教程
├── WannierTools理论基础和软件介绍-吴泉生.pdf # 理论基础及软件介绍
├── env.sh                            # 环境配置脚本，配置python环境，并将模块加载和 PATH 设置添加到 ~/.bashrc
├── sub-wt.sh                         # SLURM 提交脚本，用于在计算节点运行 wt.x
├── sub-w90.sh                        # SLURM 提交脚本，用于在计算节点运行 wannier90.x
├── sub-vasp_std.sh                   # SLURM 提交脚本，用于在计算节点运行 vasp_std
├── sub-vasp_ncl.sh                   # SLURM 提交脚本，用于在计算节点运行 vasp_ncl
├── sub-python.sh                     # SLURM 提交脚本，用于在计算节点运行 python
└── README.md                         # 本文档
```

---

## 环境配置（env.sh）（仅仅适用于本次培训会使用的并行科技集群，自己集群需要自己配置）

`env.sh` 脚本将以下内容追加到用户的 `~/.bashrc` 中，并自动执行 `source ~/.bashrc`：

```bash
# 1) 加载 MPI & ARPACK
module load intel/intelcompiler/2020.4

# 2) 加载 codna 的 base 环境（conda）
source /online1/paratera_wx_group/pwx_share/soft/conda/etc/profile.d/conda.sh

# 3) 将可执行文件加入 PATH (包括 wt.x, vasp_std, vasp_ncl, vasp_gam, wannier90.x, tgtbgen)
export PATH="$HOME/data/wt2025/bin/:$PATH"
```


### 使用方法

1. 在 `wt2025/` 目录下，执行脚本：

   ```bash
   source env.sh
   ```
2. 脚本会自动激活conda的base环境，并提示即将追加到 `~/.bashrc` 的内容，按回车继续。
3. 运行完成后，配置立即生效（此时命令行提示符会出现`（base）`前缀）。


确认下面命令可用：

```bash
module list      # 查看已加载的模块
which wt.x       # 应能找到 wt.x 可执行路径 （～/data/wt2025/bin/wt.x）
which python     # 查看python路径 (base环境下应该在此处/online1/paratera_wx_group/pwx_share/soft/conda/bin/python)
```

---

## 提交作业（需根据自己集群的实际情况修改）

`sub-wt.sh` 是一个简洁的 SLURM 提交脚本，用于将 `wt.x` 并行任务提交到集群 (类似的，还有sub-python.sh, sub-w90.sh, sub-vasp_std.sh等等)：

```bash
#!/bin/bash
#SBATCH -p intel                # 分区
#SBATCH -N 1                    # 节点数
#SBATCH -n 64                   # MPI 进程数
#SBATCH -t 02:00:00             # 最长运行时间
#SBATCH -J wanniertools         # 作业名
#SBATCH -o out                  # 标准输出
#SBATCH -e err                  # 标准错误

module load intel/intelcompiler/2020.4
export PATH=~/data/wt2025/bin/:$PATH
# 并行运行 wt.x
mpirun wt.x
```

### 提交命令

1. 确保已配置好环境：

   ```bash
   source ~/.bashrc   # 确保 module 和 PATH 已更新
   ```
2. 提交作业：

   ```bash
   sbatch sub-wt.sh
   ```
3. 查看作业运行情况：

   ```bash
   squeue         # 查看当前用户的作业列表
   ```
4. 日志文件在提交目录下：

   * `out`：标准输出日志
   * `err`：标准错误日志

---

## 示例（examples/）

`examples/` 目录下包含多种示例文件夹，以及 PDF 教程：

* `3DWeyl-model/`, `BHZ-model/`, `Bi2Se3/`, `Graphene/` 等子目录，里面分别存放对应材料的输入文件、控制脚本和运行说明。
* `WannierTools_tutorial_2025_liyang.pdf`：中文教程，可结合示例练习。
* `README.md`：简要说明示例目录结构。

### 使用示例

1. 进入某个示例目录：

   ```bash
   cd examples/Bi2Se3
   ```
2. 仔细阅读该目录下的 `README.txt`（如果有），确认输入文件命名规则及运行步骤。
3. 在示例目录下执行：

   ```bash
   cp ~/data/wt2025/sub-wt.sh .
   sbatch sub-wt.sh
   ```
4. 等待任务完成，查看输出结果，并对照教程分析。

---

## 可执行文件（bin/）

`bin/` 目录下包含（在自己的集群上需要自己编译安装）：

* `wt.x`：WannierTools 主程序（并行版、MPI 支持）
* `wannier90.x`：Wannier90 程序，可进行 Wannier 函数构建
* `vasp_std`、`vasp_ncl`、`vasp_gam` ：VASP可执行文件
* `tgtbgen` ：生成石墨烯转角/非转角的POSCAR/哈密顿量
确保：

```bash
ls ~/wt2025/bin/   # 应列出以上可执行文件
```

---

## PDF 教程

* `WannierTools_tutorial_2025_liyang.pdf`：2025年 WannierTools 溧阳会议的中文教程，涵盖安装、基本用法和常见示例。
* `WannierTools理论基础和软件介绍-吴泉生.pdf`：理论基础与软件介绍，可结合学习 WannierTools 的原理。

---

## 联系方式

* 如有疑问，可联系：

  * 吴泉生：[quansheng.wu@iphy.ac.cn](mailto:quansheng.wu@iphy.ac.cn)

欢迎大家一起交流，共同学习 WannierTools 软件！
