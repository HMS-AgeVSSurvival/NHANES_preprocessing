#!/bin/bash
#SBATCH --partition short
#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu 10G

module load gcc/6.2.0
module load python/3.7.4
source env_test/bin/activate


fusion $@