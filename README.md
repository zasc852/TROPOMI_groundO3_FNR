TROPOMI의 HCHO, NO2 와 지상 오존 농도 자료를 사용해 FNR 임계값과 오존 생성 민감도 영역의 산출, 분석하는 코드

TROPOMI, 지상 오존 자료의 전처리과정은 포함되지 않음
FNR 임계값 산출과 그에 따른 오존 생성 민감도 영역 산출물에 관한 코드로 구성됨
Shell Script와 python 코드로 구성되었음

data 설명
1. SMA_HCHO_NO2_TROPOMI.csv
: TROPOMI(https://www.earthdata.nasa.gov/)의 HCHO, NO2를 다운받은 후
한국 SMA(서울,인천,경기도)에 대해 가공하고 재격자화한 파일

2. SMA_O3_AirKorea.csv
: AirKorea(https://www.airkorea.or.kr/)의 지상 오존을 다운받은 후
한국 SMA(서울,인천,경기도)에 대해 가공한 파일

참고 사항
SHEL 폴더의 0.path_def.sh의 경우, 자신의 현재 경로로 바꿔야함
(WORKDIR, PYTHON)
