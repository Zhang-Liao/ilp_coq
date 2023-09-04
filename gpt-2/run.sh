#!/bin/bash -l
#SBATCH --job-name=ilp

#              d-hh:mm:ss
#SBATCH --time=3-18:00:00
#SBATCH --partition gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=14GB
#SBATCH --nodelist=dgx-5
cd /home/zhanglia/gpt-2
conda activate ./conda
sed -i 's/\x0//g' *.py

python eval.py
# python test.py


exit 0
