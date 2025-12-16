# 1. 프로젝트 목적

   Shell Script를 이용하여 TROPOMI의 HCHO, NO2 와 지상 오존 농도 자료로 FNR 임계값과 오존 생성 민감도 영역의 산출, 분석

# 2. data 설명
TROPOMI, 지상 오존 자료의 전처리과정은 포함되지 않음, 
FNR 임계값 산출과 그에 따른 오존 생성 민감도 영역 산출물에 관한 코드로 구성됨

1. SMA_HCHO_NO2_TROPOMI_test.csv
: TROPOMI(https://www.earthdata.nasa.gov/) 의 HCHO, NO2를 다운받은 후
한국 SMA(서울,인천,경기도)에 대해 가공하고 재격자화한 파일

2. SMA_O3_AirKorea_test.csv
: AirKorea(https://www.airkorea.or.kr/) 의 지상 오존을 다운받은 후
한국 SMA(서울,인천,경기도)에 대해 가공한 파일

# 3. 실행 환경 설정
1. SHEL 폴더의 0.path_def.sh의 경우, 자신의 현재 경로로 바꿔야함(WORKDIR, PYTHON)
2. SHP파일, 폰트는 제공하지 않음 사용자의 편의대로 추가 필요

      
# 4. 프로젝트 구조
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
├─ DATA/
│  ├─ SMA_HCHO_NO2_TROPOMI_test.csv
│  └─ SMA_O3_AirKorea_test.csv
│
├─ OUTD/SMA/                                    # 결과 
│  ├─ GEMS_FNR_Threshold_SMA.txt
│  ├─ TROPOMI_FNR_Threshold_SMA.png
│  ├─ TROPOMI_FNR_heatmap_SMA.png
│  └─ FNR_O3_Formation_Sensitivity_SMA.png
│
├─ LOGO/                                    # 결과에 따른 error log 파일
│  ├─ 1.py_out
│  ├─ 2.py_out
│  └─ 3.py_out
```

# 5. 결과 예시  
<img width="600" height="450" alt="TROPOMI_FNR_Threshold_SMA" src="https://github.com/user-attachments/assets/3d4059b3-56dc-45a5-adcd-697c99380eab" />

TROPOMI(HCHO, NO2)와 지상 오존농도를 통한 FNR 임계치 산출

<img width="613" height="546" alt="TROPOMI_FNR_heatmap_SMA" src="https://github.com/user-attachments/assets/d34e6db8-fc08-442d-978d-06c456ff7bff" />

FNR 임계치 기반 오존 생성 민감도 영역로 나눈 TROPOMI(HCHO, NO2)와 지상 오존농도 분포(heatmap)

<img width="689" height="578" alt="FNR_O3_Formation_Sensitivity_SMA" src="https://github.com/user-attachments/assets/abdf5d45-2c29-4677-b150-8f5b6767482f" />

FNR 임계치 기반 오존 생성 민감도 영역 및 지상 오존 농도 공간 분포도 








