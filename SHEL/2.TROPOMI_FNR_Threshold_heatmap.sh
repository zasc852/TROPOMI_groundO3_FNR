#!/bin/bash
set -e

source "/D/정리/코드 포토폴리오/TROPOMI_groundO3_FNR/SHEL/0.path_def.sh"

mkdir -p "${LOGDIR}" "${OUTDIR}"

cd "${WORKDIR}" || exit 1

export WORKDIR OUTDIR O3_FILE TROPOMI_FILE FONT_PATH

echo "======================================================="
echo "==== Show whole-year FNR threshold heatmap (ALLYEAR) ===="
echo "======================================================="
echo "Running    : 2.TROPOMI_FNR_Threshold_allyear_heatmap.py"
echo "Python     : ${PYTHON}"
echo "======================================================="

"${PYTHON}" "${FNR_PYTD}/2.TROPOMI_FNR_Threshold_allyear_heatmap.py" \
    > "${LOGDIR}/2.py_out" 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR] FNR threshold heatmap failed."
    echo "Check log file: ${LOGDIR}/2.py_out"
    exit 1
fi


echo "======================================================="
echo "FNR threshold heatmap completed successfully"
echo "Log file : ${LOGDIR}/2.py_out"
echo "======================================================="

exit 0
