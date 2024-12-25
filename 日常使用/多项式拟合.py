import numpy as np
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']  # 黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 数据输入
a_sensor_values = np.array([0,0.98, 1.94, 2.97, 3.9, 4.97, 6.0, 6.9, 7.9, 8.9, 9.9, 10.9])  # a传感器的读数
b_sensor_values = np.array([0,1.5, 3.5, 5.3, 7.2, 9.2, 11.1, 12.9, 14.7, 16.6, 18.5, 20.4])  # b传感器的实际值

# 多项式拟合（选择适当的阶数，通常从低阶开始，避免过拟合）
degree = 3  # 选择3阶多项式
poly_coeffs = Polynomial.fit(a_sensor_values, b_sensor_values, deg=degree)

# 显示多项式公式
coeffs = poly_coeffs.convert().coef
formula = " + ".join([f"{coeff:.4f} * x^{i}" for i, coeff in enumerate(coeffs)])
print(f"拟合出的多项式公式: b_corrected = {formula}")

# 测试修正
a_raw = 6.5  # 示例a传感器值
b_corrected = poly_coeffs(a_raw)
print(f"原始a传感器值: {a_raw}, 修正后的值: {b_corrected:.4f}")

# 可视化拟合效果
x_fit = np.linspace(min(a_sensor_values), max(a_sensor_values), 100)
y_fit = poly_coeffs(x_fit)

plt.scatter(a_sensor_values, b_sensor_values, color="red", label="实际值")
plt.plot(x_fit, y_fit, color="blue", label=f"拟合曲线 (degree={degree})")
plt.xlabel("a传感器值")
plt.ylabel("b传感器值")
plt.title("多项式拟合效果")
plt.legend()
plt.grid()
plt.show()
