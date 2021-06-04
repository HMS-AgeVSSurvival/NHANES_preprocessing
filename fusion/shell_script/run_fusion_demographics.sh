#!/bin/bash

rm out/fusion/demographics/demographics.out
sbatch -J fusion/demographics/demographics -o out/fusion/demographics/demographics.out fusion/shell_script/unit_fusion.sh -mc "demographics" -c "demographics"
