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

# 重采样为周线数据（以每周的最后一天数据为准）
weekly_data = data.resample('W').agg({
    'open': 'first',  # 每周的开盘价是该周的第一天的开盘价
    'high': 'max',    # 每周的最高价是该周的最高价
    'low': 'min',     # 每周的最低价是该周的最低价
    'close': 'last',  # 每周的收盘价是该周的最后一天的收盘价
    'vol': 'sum'      # 每周的成交量是该周所有天数的成交量总和
})

# 填充缺失值，使用前向填充方法（可以根据需要选择其他填充方法）
weekly_data.fillna(method='ffill', inplace=True)

# 重采样为月线数据（以每月的最后一天数据为准）
monthly_data = data.resample('M').agg({
    'open': 'first',  # 每月的开盘价是该月的第一天的开盘价
    'high': 'max',    # 每月的最高价是该月的最高价
    'low': 'min',     # 每月的最低价是该月的最低价
    'close': 'last',  # 每月的收盘价是该月的最后一天的收盘价
    'vol': 'sum'      # 每月的成交量是该月所有天数的成交量总和
})

# 绘制周线数据图（收盘价）
plt.figure(figsize=(10, 6))
plt.plot(weekly_data.index, weekly_data['close'], label='Weekly Close Price', color='b')
plt.title('Weekly Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 绘制月线数据图（收盘价）
plt.figure(figsize=(10, 6))
plt.plot(monthly_data.index, monthly_data['close'], label='Monthly Close Price', color='g')
plt.title('Monthly Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
