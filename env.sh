#!/usr/bin/env bash
#
# 文件名：env.sh
# 作用：将 module 加载以及 PATH 设置追加到 ~/.bashrc，
#       并在追加完成后让当前 shell 生效（如果需要对当前终端生效，建议用 source env.sh）。
#
# 用法：
#   1. 如果希望脚本在子 Shell 中运行，使用：bash env.sh
#      – 这种方式会在当前脚本中新开一个子 Shell 去执行 source ~/.bashrc，但不会直接修改父 Shell 的环境。
#      – 脚本末尾会尝试在子 Shell 中 source ~/.bashrc；如果想让当前交互式终端立即生效，还需要手动执行：source ~/.bashrc
#
#   2. 如果希望脚本直接修改当前交互式终端环境，使用：source env.sh
#      – 这样脚本内部执行的 source ~/.bashrc 会直接对当前 Shell 生效，无需额外操作。
#

set -eo pipefail

# 1. 定义目标文件
BASHRC="$HOME/.bashrc"

echo "================================================================"
echo "      开始将环境配置写入：$BASHRC"
echo "================================================================"
echo ""
source /online1/paratera_wx_group/pwx_share/soft/conda/etc/profile.d/conda.sh

# 2. 如果 ~/.bashrc 不存在，则先创建一个空文件
if [[ ! -f "$BASHRC" ]]; then
    echo "[info] $BASHRC 不存在，正在创建一个空文件..."
    touch "$BASHRC"
    echo "[ok] 已创建：$BASHRC"
    echo ""
fi

# 3. 如果还没做过 conda init，就先初始化
if ! grep -q 'conda initialize' "$BASHRC"; then
    echo "[info] 正在执行: conda init"
    # 使用 bash -lc 保证 conda 命令在完整登录环境下执行
    bash -lc "conda init"
else
    echo "[info] 检测到 conda 已经初始化，跳过 conda init。"
fi

# 4. 预览要追加的内容
cat << '___PREVIEW___'

以下内容将被追加到 ~/.bashrc 末尾：
--------------------------------------------------
# —— 以下部分由 env.sh 自动追加 —— 

# 1) 加载 MPI & ARPACK
module load intel/intelcompiler/2020.4

# 2) 加载 python 环境（conda）
source /online1/paratera_wx_group/pwx_share/soft/conda/etc/profile.d/conda.sh

# 3) 将可执行文件加入 PATH (包括 wt.x, vasp_std, vasp_ncl, vasp_gam, wannier90.x, tgtbgen)
export PATH="$HOME/data/wt2025/bin/:$PATH"
# —— env.sh 自动追加结束 —— 
--------------------------------------------------

请确认无误后按回车继续，或按 Ctrl+C 取消操作。
___PREVIEW___

read -r -p "[确认] 按回车继续，或 Ctrl+C 退出："

echo ""
echo "[info] 正在将配置追加到 $BASHRC …"

# 5. 如果 ~/.bashrc 里还没有这段，就追加；否则跳过
if ! grep -q '—— 以下部分由 env.sh 自动追加 ——' "$BASHRC"; then
    cat << 'EOF' >> "$BASHRC"
# —— 以下部分由 env.sh 自动追加 —— 

# 1) 加载 MPI & ARPACK
module load intel/intelcompiler/2020.4

# 2) 加载 python 环境（conda）
source /online1/paratera_wx_group/pwx_share/soft/conda/etc/profile.d/conda.sh

# 3) 将可执行文件加入 PATH (包括 wt.x, vasp_std, vasp_ncl, vasp_gam, wannier90.x, tgtbgen)
export PATH="$HOME/data/wt2025/bin/:$PATH"
# —— env.sh 自动追加结束 —— 
EOF

    echo "[ok] 已将内容追加到 $BASHRC。"
else
    echo "[info] 检测到该内容已存在，跳过追加。"
fi

echo ""
# 6. 让当前 shell 生效
echo "[info] 准备执行：source $BASHRC"

# 由于可能存在 /etc/bashrc 中引用未定义变量导致 set -u 报错，
# 这里先临时关闭 -u，然后再执行 source，最后恢复 -u 检查。
set +u
source "$BASHRC"
set -u

echo "[ok] 已成功 source $BASHRC，环境变量已更新。"
echo ""
echo "================================================================"
echo "        脚本执行完毕，请检查上述输出，确认无错误。"
echo "================================================================"
