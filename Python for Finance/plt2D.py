import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import seaborn as sns

# 生成数据
x = np.linspace(0, 20, 100)
y = np.sin(x)
z = np.cos(x**2)

# 创建画布
plt.figure(figsize=(8, 4))
# fig, ax1 = plt.subplots()
# 绘制图形
plt.plot(y, label="$sin(x)$", color="red", linewidth=2)

plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.legend(loc=8)

axis2=plt.twinx()
# 添加图例
plt.plot(z, "y-o", label="$cos(x^2)$")
# 添加x轴和y轴的标签

plt.ylabel("Volt2")
plt.legend(loc=1)
# 添加标题
plt.title("PyPlot First Example")
# 显示图形
plt.show()