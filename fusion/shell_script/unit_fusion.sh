#!/bin/bash
#SBATCH --partition short
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu 5G

module load gcc/6.2.0
module load python/3.7.4
source env_test/bin/activate


fusion $@