#!/bin/bash
set -e

export WORKDIR="/D/정리/코드 포토폴리오/TROPOMI_groundO3_FNR" 
export FNR_SHEL="${WORKDIR}/SHEL"
export FNR_PYTD="${WORKDIR}/PYTD"
export LOGDIR="${WORKDIR}/LOGO"
export OUTDIR="${WORKDIR}/OUTD"
export DATADIR="${WORKDIR}/DATA"

export FONT_PATH="${DATADIR}/TimesNewerRoman-Regular.otf"
export O3_FILE="${DATADIR}/SMA_O3_AirKorea_test.csv"
export TROPOMI_FILE="${DATADIR}/SMA_HCHO_NO2_TROPOMI_test.csv"

export PYTHON="/c/Users/lab1/anaconda3/python.exe"