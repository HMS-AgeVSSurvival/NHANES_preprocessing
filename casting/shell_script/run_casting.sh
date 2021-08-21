#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire" "demographics" "mortality"
do
    [ -d out/casting/$MAIN_CATEGORY/ ] || mkdir -p out/casting/$MAIN_CATEGORY/
    [ -d error/casting/$MAIN_CATEGORY/ ] || mkdir -p error/casting/$MAIN_CATEGORY/

    for PATH_CATEGORY in cleaning/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        echo -n > out/casting/$MAIN_CATEGORY/$CATEGORY.out
        echo -n > error/casting/$MAIN_CATEGORY/$CATEGORY.out

        sbatch -J casting/$MAIN_CATEGORY/$CATEGORY -o out/casting/$MAIN_CATEGORY/$CATEGORY.out -e error/casting/$MAIN_CATEGORY/$CATEGORY.out casting/shell_script/unit_casting.sh -mc $MAIN_CATEGORY -c $CATEGORY
    done
done