#!/bin/bash
set -e

source "/D/정리/코드 포토폴리오/TROPOMI_groundO3_FNR/SHEL/0.path_def.sh"


mkdir -p "${LOGDIR}" "${OUTDIR}"

cd "${WORKDIR}" || exit 1

export WORKDIR OUTDIR O3_FILE TROPOMI_FILE FONT_PATH

echo "======================================================="
echo "==== Show O3 Formation Sensitivity (ALLYEAR) ===="
echo "======================================================="
echo "Running    : 3.TROPOMI_FNR_O3_Formation_Sensitivity.py"
echo "Python     : ${PYTHON}"
echo "======================================================="

"${PYTHON}" "${FNR_PYTD}/3.TROPOMI_FNR_O3_Formation_Sensitivity.py" \
    > "${LOGDIR}/3.py_out" 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR] O3 Formation Sensitivity failed."
    echo "Check log file: ${LOGDIR}/3.py_out"
    exit 1
fi


echo "======================================================="
echo "O3 Formation Sensitivity completed successfully"
echo "Log file : ${LOGDIR}/3.py_out"
echo "======================================================="

exit 0
