import tushare as ts

# 设置你的API Token（需要在Tushare官网注册获取）
ts.set_token('6f72112367529da65bc1e025e6f6449b9d545101dff3d19a32a49790')

# 初始化pro接口
pro = ts.pro_api()

# 获取某只股票的历史K线数据（日K线）
df = pro.daily(ts_code='000001.SZ', start_date='20230101', end_date='20240101')

# 打印数据
df.to_csv("000001.csv")

