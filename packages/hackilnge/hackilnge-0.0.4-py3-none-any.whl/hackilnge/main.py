import time
import halo
from tqdm import tqdm

# 로딩 메시지 표시
with halo.Halo(text='로딩 중...', spinner='dots') as loading_spinner:
    time.sleep(3)
    loading_spinner.succeed('로딩 완료!')

# 패키지 설치 로그 표시
while True:
    with halo.Halo(text='오윤창 컴퓨터 해킹 및 포멧 진행...', spinner='dots') as install_spinner:
        for i in tqdm(range(320), desc='피시 해킹 진행 상황', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
            # API 통신 로그 출력
            print(f'API 통신 중... {i+1}/320')
            time.sleep(0.1)
        install_spinner.succeed('해킹툴 설치 완료!')
    time.sleep(5)
