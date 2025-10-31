import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import trapezoid

# 데이터 읽기
bins, count = [], []
with open("hist2.csv", "r") as f:
    for line in f.readlines():
        _b, _c = [float(i) for i in line.split(",")]
        bins.append(_b)
        count.append(_c)

# 모델 함수
def particle(x, a, b, c):
    return a*np.exp(-((x-b)**2)/(2*c**2))

def double_particle(x, a1, b1, c1, a2, b2, c2):
    return particle(x, a1, b1, c1) + particle(x, a2, b2, c2)

# 초기 추정값 설정
p0 = [max(count), bins[np.argmax(count)], 0.2, max(count)/2, bins[np.argmax(count)]+1, 0.2]

params, _ = curve_fit(double_particle, bins, count, p0=p0)

# A, B 각 입자별 fitting
bins = np.array(bins)
_x = np.linspace(bins.min(), bins.max(), 1000)
fit_A = particle(_x, params[0], params[1], params[2])
fit_B = particle(_x, params[3], params[4], params[5])
fit_total = fit_A + fit_B

# A, B 각 적분값(빈도수 총합) 구하기
area_A = trapezoid(fit_A, _x)
area_B = trapezoid(fit_B, _x)
ratio = area_A / area_B

print(f"A의 적분값: {area_A:.3f}")
print(f"B의 적분값: {area_B:.3f}")
print(f"생성비 (A:B) = {ratio:.3f}:1")

# 그래프 출력
plt.bar(bins, count, width=0.05, alpha=0.5, color='gray', label='Hist Data')
plt.plot(_x, fit_total, 'k-', label='fit: Total')
plt.plot(_x, fit_A, 'r-', label='fit: A')
plt.plot(_x, fit_B, 'b-', label='fit: B')
plt.xlabel('Energy')
plt.ylabel('Counts')
plt.legend()
plt.grid()
plt.show()