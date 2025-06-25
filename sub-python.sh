#!/bin/bash
#SBATCH -p intel                # 指定分区（Partition）
#SBATCH -N 1                    # 申请 1 个节点
#SBATCH -n 1                    # 启动 1 个任务（MPI rank）
#SBATCH -t 02:00:00             # 最长运行时间 2 小时（HH:MM:SS）
#SBATCH -J python_job           # 作业名称
#SBATCH -o out                  # 标准输出
#SBATCH -e err                  # 标准错误

## （可选）加载环境模块
#module load intel/intelcompiler/2020.4

# -------------------------------
# 加载 conda 命令
# -------------------------------
source /online1/paratera_wx_group/pwx_share/soft/conda/etc/profile.d/conda.sh

# -------------------------------
# 激活你要用的环境
# -------------------------------
conda activate mp_api

# -------------------------------
# 下面写你要执行的 Python 脚本
# -------------------------------
python test.py
