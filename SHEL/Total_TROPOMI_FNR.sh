#!/bin/bash
set -e

source "/D/정리/코드 포토폴리오/TROPOMI_groundO3_FNR/SHEL/0.path_def.sh"

start_year=2019
end_year=2024

run_calulate_FNR_Threshold=true
run_FNR_Threshold_heatmap=true
run_O3_formation_sensitivity=true

# 각 작업 실행
if [ "$run_calulate_FNR_Threshold" = true ]; then
    echo '====== program 1(FNR_Threshold) ======'
    "$FNR_SHEL/1.TROPOMI_FNR_Threshold.sh" $start_year $end_year 
fi
echo ''

if [ "$run_FNR_Threshold_heatmap" = true ]; then
    echo '====== program 2(FNR_Threshold heatmap) ======'
    "$FNR_SHEL/2.TROPOMI_FNR_Threshold_heatmap.sh" $start_year $end_year 
fi
echo ''

if [ "$run_O3_formation_sensitivity" = true ]; then
    echo '====== program 3(O3_formation_sensitivity) ======'
    "$FNR_SHEL/3.TROPOMI_FNR_O3_Formation_Sensitivity.sh" $start_year $end_year 
fi
echo ''

