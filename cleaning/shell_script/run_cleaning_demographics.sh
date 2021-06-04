#!/bin/bash

rm out/cleaning/demographics/demographics.out
sbatch -J cleaning/demographics/demographics -o out/cleaning/demographics/demographics.out cleaning/shell_script/unit_cleaning.sh -mc "demographics" -c demographics
