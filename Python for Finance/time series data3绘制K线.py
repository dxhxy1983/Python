import pandas as pd
import mplfinance as mpf

file_path=r"F:\myDoc\github\Python\000001.csv"
# 加载CSV文件
data = pd.read_csv(file_path)

# 删除不需要的列（ts_code, pre_close, change, pct_chg, amount）
data = data.drop(columns=['ts_code', 'pre_close', 'change', 'pct_chg', 'amount'])

# 将日期列转换为 datetime 类型，并设置为索引
data['trade_date'] = pd.to_datetime(data['trade_date'], format='%Y%m%d')
data.set_index('trade_date', inplace=True)

# 重命名列以符合 mplfinance 要求
data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'vol': 'Volume'}, inplace=True)

# 确保数据按日期排序
data = data.sort_index()

# 绘制 K 线图
mpf.plot(data, type='candle', style='charles', title='Stock K-Line', ylabel='Price', volume=True)
