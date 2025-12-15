TROPOMI의 HCHO, NO2 와 지상 오존 농도 자료를 사용해 FNR 임계값과 오존 생성 민감도 영역의 산출, 분석하는 코드

TROPOMI, 지상 오존 자료의 전처리과정은 포함되지 않음
FNR 임계값 산출과 그에 따른 오존 생성 민감도 영역 산출물에 관한 코드로 구성됨
Shell Script와 python 코드로 구성되었음

data 설명
1. SMA_HCHO_NO2_TROPOMI_test.csv
: TROPOMI(https://www.earthdata.nasa.gov/) 의 HCHO, NO2를 다운받은 후
한국 SMA(서울,인천,경기도)에 대해 가공하고 재격자화한 파일

2. SMA_O3_AirKorea_test.csv
: AirKorea(https://www.airkorea.or.kr/) 의 지상 오존을 다운받은 후
한국 SMA(서울,인천,경기도)에 대해 가공한 파일

참고 사항
1. SHEL 폴더의 0.path_def.sh의 경우, 자신의 현재 경로로 바꿔야함(WORKDIR, PYTHON)
2. SHP파일, 폰트는 제공하지 않음 사용자의 편의대로 추가 필요


프로젝트 구성
```text
TROPOMI_groundO3_FNR/
├─ README.md
│
├─ SHEL/                                   # Shell 실행 스크립트
│  ├─ 0.path_def.sh                        # 경로 및 환경 변수 정의
│  ├─ 1.TROPOMI_FNR_Threshold.sh
│  ├─ 2.TROPOMI_FNR_Threshold_heatmap.sh
│  ├─ 3.TROPOMI_FNR_O3_Formation_Sensitivity.sh
│  └─ Total_TROPOMI_FNR.sh                 # 전체 파이프라인 실행 스크립트
│
├─ PYTD/                                   # Python code
│  ├─ 1.TROPOMI_FNR_Threshold_allyear.py
│  ├─ 2.TROPOMI_FNR_Threshold_Threshold_allyear_heatmap.py
│  └─ 3.TROPOMI_FNR_O3_Formation_Sensitivity.py
│
├─ OUTD/SMA/                                    # 결과 
│  ├─ GEMS_FNR_Threshold_SMA.txt
│  ├─ TROPOMI_FNR_Threshold_SMA.png
│  ├─ TROPOMI_FNR_heatmap_SMA.png
│  └─ FNR_O3_Formation_Sensitivity_SMA.png

```



