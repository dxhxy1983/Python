import pandas as pd
import matplotlib.pyplot as plt

# 加载CSV文件
file_path = r"F:\myDoc\github\Python\000001.csv"
data = pd.read_csv(file_path)

# 删除不需要的列（ts_code, pre_close, change, pct_chg, amount）
data = data.drop(columns=['ts_code', 'pre_close', 'change', 'pct_chg', 'amount'])

# 将日期列转换为 datetime 类型，并设置为索引
data['trade_date'] = pd.to_datetime(data['trade_date'], format='%Y%m%d')
data.set_index('trade_date', inplace=True)

# 绘制收盘价的线图
plt.figure(figsize=(10, 6))  # 设置图形大小
plt.plot(data.index, data['close'], label='Close Price', color='b', marker='o')

# 添加标题和标签
plt.title('Stock Close Price Over Time')
plt.xlabel('Date')
plt.ylabel('Close Price')

# 显示图例
plt.legend()

# 显示网格
plt.grid(True)
plt.xticks(rotation=45)  # 旋转x轴标签
plt.tight_layout()  # 调整布局以防止标签重叠

# 显示图形
plt.show()
