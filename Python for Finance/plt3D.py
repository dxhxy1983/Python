import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
strikes = np.linspace(50, 150, 24) # 24个Strike
maturities = np.linspace(0.5, 2.5, 24) # 24个Maturity
strike, maturity = np.meshgrid(strikes, maturities) # 生成网格
# 生成数据
iv = (strike - 100) ** 2 / (100 * strike) /maturity
# # 创建画布
fig = plt.figure(figsize=(10, 6))
# 绘制图形
ax = fig.add_subplot(1, 1, 1, projection='3d') # 3D图
surf=ax.plot_surface(strike, maturity, iv, rstride=2, cstride=2, cmap=plt.cm.coolwarm, linewidth=0.5, antialiased=True) # 绘制3D图
ax.set_xlabel('Strike') # 设置x轴标签
ax.set_ylabel('time-to-maturity') # 设置y轴标签
ax.set_zlabel('implied volatility') # 设置z轴标签
fig.colorbar(surf, shrink=0.8, aspect=20);
plt.show()
