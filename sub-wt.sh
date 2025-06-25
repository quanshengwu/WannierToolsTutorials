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
