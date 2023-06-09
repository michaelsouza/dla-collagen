#!/bin/bash
#SBATCH --job-name=collagen
#SBATCH --output=collagen.out
#SBATCH --error=collagen.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --time=24:00:00

cat commands_collagen.txt | parallel -j $SLURM_CPUS_PER_TASK