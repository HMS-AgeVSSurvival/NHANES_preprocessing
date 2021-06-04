#!/bin/bash

rm out/casting/demographics/demographics.out
sbatch -J casting/demographics/demographics -o out/casting/demographics/demographics.out casting/shell_script/unit_casting.sh -mc "demographics" -c "demographics"