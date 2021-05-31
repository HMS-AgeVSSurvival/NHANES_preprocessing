#!/bin/bash

for CATEGORY in "body" "eyes" "ears" "nose_mouth" "lungs" "heart" "liver" "bones" "nerves" "muscles" "skin" "other"
do
    rm out/fusion/examination/$CATEGORY.out
    sbatch -J fusion/examination/$CATEGORY -o out/fusion/examination/$CATEGORY.out fusion/shell_script/unit_fusion_examination.sh -c $CATEGORY
done

rm out/fusion/examination/physical_activity.out
sbatch -J fusion/examination/physical_activity -o out/fusion/examination/physical_activity.out fusion/shell_script/unit_fusion_examination_deep_mem.sh -c physical_activity