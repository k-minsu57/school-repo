import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import sys

# 위성 TLE와 Space weather 정보 cvs 파일 및 추가 위성 정보
TLE_FILE_NAME = 'GOCE_TLE.csv'   # TLE 데이터 파일명
SW_FILE_NAME = 'SW-All.csv'      # Space weather 데이터 파일명

INPUT_MASS = 872     # kg (위성 질량)
INPUT_AREA = 1.0     # m^2 (항력 단면적)
SPLIT_RATIO = 0.5    # 전체 데이터의 앞쪽 50%를 학습에 사용

# 상수 정의
MU = 398600.4418     # 지구 중력 상수 (km^3/s^2)
EARTH_RADIUS = 6371.0 # 지구 평균 반지름 (km)


def calculate_density(altitude_km): # 대기 항력 데이터를 얻기 위한 지수 대기 밀도 모델

    H = 45.0        # Scale Height (km)
    rho0 = 2.7e-10  # 기준 밀도 (kg/m^3) at h0
    h0 = 200.0      # 기준 고도 (km)
    
    # 밀도 rho = rho0 * exp(-(h - h0) / H)
    density = rho0 * np.exp(-(altitude_km - h0) / H)
    return density

def load_and_process():
    print(f">> 데이터 파일 로드 중... ({TLE_FILE_NAME})")
    
    # TLE 데이터 로드
    try:
        df_tle = pd.read_csv(TLE_FILE_NAME)
    except FileNotFoundError:
        print(f"\n[Error] '{TLE_FILE_NAME}' 파일을 찾을 수 없습니다.")
        sys.exit(1)

    # Space weather 데이터 로드
    try:
        df_sw = pd.read_csv(SW_FILE_NAME)
        has_sw = True
    except FileNotFoundError:
        print(f">> 알림: '{SW_FILE_NAME}' 파일이 없어 기상 데이터 없이 진행합니다.")
        has_sw = False

    # 고도(Altitude) 계산
    # 공식: Altitude = (mu / n^2)^(1/3) - R_earth : Gemini에게 TLE 정보를 바탕으로 고도를 계산하는 공식과 코드를 요청하여 받았습니다.
    df_tle['n_rad_s'] = df_tle['MEAN_MOTION'] * (2 * np.pi / 86400)
    df_tle['semi_major_axis_km'] = (MU / (df_tle['n_rad_s'] ** 2)) ** (1/3)
    df_tle['Altitude'] = df_tle['semi_major_axis_km'] - EARTH_RADIUS
    
    # TLE 데이터 날짜 문자열을 datatime 객체로 변환
    df_tle['EPOCH'] = pd.to_datetime(df_tle['EPOCH'])
    
    # Space weather 데이터 병합 : TLE 정보와 Space weather의 date가 일치하지 않는 문제를 해결할 방법을 Gemini에게 물어 얻은 코드입니다.
    if has_sw:
        df_tle['date_short'] = df_tle['EPOCH'].dt.strftime('%Y-%m-%d')
        df_sw['DATE'] = pd.to_datetime(df_sw['DATE']).dt.strftime('%Y-%m-%d')
        
        df_merged = pd.merge(df_tle, df_sw[['DATE', 'F10.7_OBS', 'AP_AVG']], 
                             left_on='date_short', right_on='DATE', how='left')
        
        # 빈칸 앞의 값으로 채우기
        df_merged['F10.7_OBS'] = df_merged['F10.7_OBS'].ffill().bfill()
        df_merged['AP_AVG'] = df_merged['AP_AVG'].ffill().bfill()
        df = df_merged
    else:
        df = df_tle

    # 데이터 정제 및 정렬
    df = df.sort_values(by='EPOCH').reset_index(drop=True)
    
    # 이동 평균으로 노이즈 완화(TLE 데이터의 오차로 인한 노이즈)
    df['Altitude_Smooth'] = df['Altitude'].rolling(window=5, center=True).mean()
    
    # 계산 불가능한 행(NaN) 제거
    df = df.dropna(subset=['Altitude_Smooth'])
    
    print(f">> 데이터 로드 완료: 총 {len(df)}개 샘플")
    print(f"   기간: {df['EPOCH'].min()} ~ {df['EPOCH'].max()}")
    
    return df

def train_evaluate_and_predict(df):

    # 시간 간격(dt) 및 하강량(drop) 계산
    df['dt'] = df['EPOCH'].diff().dt.total_seconds() / 86400.0 # 단위: 일(day)
    df['drop_km'] = -df['Altitude_Smooth'].diff()              # 양수 = 하강
    df['decay_rate'] = df['drop_km'] / df['dt']                # 단위: km/day
    
    # 대기 밀도 계산
    df['density'] = calculate_density(df['Altitude_Smooth'])
    
    # 궤도 속도 제곱(v^2) 계산
    # v^2 = mu / r
    df['r_km'] = EARTH_RADIUS + df['Altitude_Smooth']
    df['velocity_sq'] = MU / df['r_km']
    
    # Drag Equation: a = (1/2) * rho * v^2 * (Cd * A / m)
    df['Drag_term'] = df['density'] * df['velocity_sq'] * (INPUT_AREA / INPUT_MASS)
    
    # diff 계산으로 생긴 첫 행 NaN 제거
    df_clean = df.dropna(subset=['decay_rate', 'Drag_term'])

    # train 데이터와 test 데이터 분할
    split_idx = int(len(df_clean) * SPLIT_RATIO)
    
    train_df = df_clean.iloc[:split_idx]  # train
    test_df = df_clean.iloc[split_idx:]   # test
    
    X_train = train_df[['Drag_term']]
    y_train = train_df['decay_rate']
    
    ### 선형 회귀 학습
    model = LinearRegression(fit_intercept=False)
    model.fit(X_train, y_train)


    ### 예측
    last_epoch = train_df['EPOCH'].iloc[-1]
    current_alt = train_df['Altitude_Smooth'].iloc[-1]
    
    sim_epochs = [last_epoch]
    sim_alts = [current_alt]
    
    step_days = 0.1  # 시뮬레이션 시간 간격(day)
    
    # 테스트 데이터 기간 + 10일 여유분까지 예측
    end_date = test_df['EPOCH'].max() + pd.Timedelta(days=10)

    while last_epoch < end_date:
        # 현재 상태 계산 (밀도, 속도)
        curr_r = EARTH_RADIUS + current_alt
        curr_density = calculate_density(current_alt)
        curr_velocity_sq = MU / curr_r # 중력 효과 반영
        
        # 탄도 계수 포함한 항 계산
        curr_physics_term = curr_density * curr_velocity_sq * (INPUT_AREA / INPUT_MASS)
        
        # 모델 예측
        input_df = pd.DataFrame([[curr_physics_term]], columns=['Drag_term'])
        pred_rate = model.predict(input_df)[0]
        
        # 상태 업데이트
        drop_amount = pred_rate * step_days
        current_alt -= drop_amount
        last_epoch += pd.Timedelta(days=step_days)
        
        # 기록
        sim_epochs.append(last_epoch)
        sim_alts.append(current_alt)
        
        # 추락(100km 이하) 시 종료
        if current_alt < 100:
            print(f"   -> 예측된 추락 시점: {last_epoch}")
            break


    ### 성능 평가 (Evaluation)
    # 시뮬레이션 결과를 테스트 데이터 시간에 맞춰 보간(Interpolation)
    # 비교 기준 고도 설정 (실제 데이터의 마지막 고도)
    target_alt = test_df['Altitude_Smooth'].iloc[-1]
    actual_arrival_time = test_df['EPOCH'].iloc[-1]
    
    # 시뮬레이션 데이터 준비 (Numpy array 변환)
    sim_alts_arr = np.array(sim_alts)
    sim_epochs_series = pd.Series(sim_epochs)
    
    # 예측된 시간 계산을 위한 변수 초기화
    pred_arrival_time = None
    
    # 예측이 해당 고도(target_alt)에 도달했는지 확인 : 둘 중 더 낮은 최종 고도에서 성능 검사를 할 수 있도록 코드를 보완하는 과정에서 Gemini의 도움을 받았습니다.
    if sim_alts_arr[-1] <= target_alt:
        # 도달함: 시뮬레이션 데이터에서 target_alt일 때의 시간을 보간(Interpolation)으로 찾음
        
        # np.interp를 쓰기 위해 x축(고도)이 증가하는 순서로 정렬해야 함
        # 위성은 고도가 감소하므로 배열을 뒤집어줌(reverse)
        sim_alts_sorted = sim_alts_arr[::-1]
        
        # 날짜를 숫자로 변환 (timestamp)
        sim_times_sorted = sim_epochs_series.map(pd.Timestamp.timestamp).values[::-1]
        
        # 보간 수행: target_alt일 때의 예측 Timestamp
        pred_timestamp = np.interp(target_alt, sim_alts_sorted, sim_times_sorted)
        pred_arrival_time = pd.to_datetime(pred_timestamp, unit='s')
        
    else:
        # 도달 못 함: 시뮬레이션이 실제보다 덜 떨어짐 (예측 감쇠가 느림)
        # 이 경우 '최종 같은 고도'는 예측의 마지막 고도가 됨
        print(f"\n[Warning] 시뮬레이션이 실제 최종 고도({target_alt:.2f}km)까지 도달하지 못했습니다.")
        
        target_alt = sim_alts_arr[-1] # 기준 고도를 시뮬레이션 끝으로 변경
        pred_arrival_time = sim_epochs_series.iloc[-1]
        
        # 실제 데이터에서 이 고도(더 높은 고도)에 도달했던 시간을 역추적
        test_alts_sorted = test_df['Altitude_Smooth'].values[::-1]
        test_times_sorted = test_df['EPOCH'].map(pd.Timestamp.timestamp).values[::-1]
        
        actual_ts = np.interp(target_alt, test_alts_sorted, test_times_sorted)
        actual_arrival_time = pd.to_datetime(actual_ts, unit='s')

    # 시간 차이 계산 (예측 시간 - 실제 시간)
    time_diff = pred_arrival_time - actual_arrival_time
    diff_seconds = time_diff.total_seconds()
    diff_hours = diff_seconds / 3600.0
    diff_days = diff_seconds / 86400.0
    
    print("-" * 60)
    print(f"[성능 평가 결과 - 최종 공통 고도 도달 시간 차이]")
    print(f"  * 기준 고도 (Target Altitude) : {target_alt:.4f} km")
    print(f"  * 실제 도달 시간 (Actual)     : {actual_arrival_time}")
    print(f"  * 예측 도달 시간 (Predicted)  : {pred_arrival_time}")
    print(f"  * 시간 오차 (Diff)            : {diff_hours:.2f} hours ({diff_days:.2f} days)")
    
    if diff_seconds > 0:
        print(f"    >> 예측이 실제보다 {abs(diff_days):.2f}일 늦음 (대기 항력 과소평가 가능성)")
    else:
        print(f"    >> 예측이 실제보다 {abs(diff_days):.2f}일 빠름 (대기 항력 과대평가 가능성)")
    print("-" * 60)

    ### 그래프 그리기

    plt.figure(figsize=(12, 6))

    # 실제 데이터: 회색 점
    plt.scatter(df['EPOCH'], df['Altitude'], color='gray', label='Actual Data', s=10, alpha=0.5)

    # 학습 데이터 구간: 파란 실선
    plt.plot(train_df['EPOCH'], train_df['Altitude_Smooth'], color='blue', label='Training Data', linewidth=2)

    # 미래 예측 구간: 빨간 점선
    plt.plot(sim_epochs, sim_alts, color='red', linestyle='--', label='Prediction', linewidth=2)

    plt.axvline(x=train_df['EPOCH'].iloc[-1], color='black', linestyle=':')
    plt.axhline(y=130, color='green', linestyle='--', linewidth=1.5, label='Re-entry Interface (130km)')

    plt.xlabel("Date")
    plt.ylabel("Altitude (km)")
    plt.title(f"Satellite Decay Prediction (Train on first {int(SPLIT_RATIO*100)}%)")
    plt.legend()
    plt.grid(True)
    plt.show()

# 메인 실행
if __name__ == "__main__":
    df_final = load_and_process()
    train_evaluate_and_predict(df_final)
