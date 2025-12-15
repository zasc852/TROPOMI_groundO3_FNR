#!/bin/bash
set -e

source "/D/정리/코드 포토폴리오/TROPOMI_groundO3_FNR/SHEL/0.path_def.sh"


mkdir -p "${LOGDIR}" "${OUTDIR}"

cd "${WORKDIR}"

export WORKDIR OUTDIR O3_FILE TROPOMI_FILE FONT_PATH

echo "======================================================="
echo "==== Calculate whole-year FNR threshold (ALLYEAR) ===="
echo "======================================================="
echo "Running    : 1.TROPOMI_FNR_Threshold_allyear.py"
echo "Python : ${PYTHON}"
echo "======================================================="

"${PYTHON}" "${FNR_PYTD}/1.TROPOMI_FNR_Threshold_allyear.py" \
    > "${LOGDIR}/1.py_out" 2>&1

echo "======================================================="
echo "FNR threshold calculation completed successfully"
echo "Log file : ${LOGDIR}/1.py_out"
echo "======================================================="
