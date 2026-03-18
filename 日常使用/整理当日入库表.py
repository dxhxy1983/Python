# 重新优化数据提取，过滤掉非采购明细行，只保留真正的物料数据
import os
import sys
import re
import pandas as pd

# 获取当前文件夹路径（兼容exe和脚本模式）
if getattr(sys, 'frozen', False):
    # 如果是exe文件运行
    current_dir = os.path.dirname(sys.executable)
else:
    # 如果是py脚本运行
    current_dir = os.path.dirname(os.path.abspath(__file__))

# 自动查找当前文件夹下的Excel文件（排除输出文件）
excel_files = [f for f in os.listdir(current_dir) if (f.endswith('.xlsx') or f.endswith('.xls')) and not f.startswith('采购单_有效')]

if not excel_files:
    print("错误：当前文件夹下没有找到Excel文件！")
    import sys
    sys.exit(1)

# 如果有多个Excel文件，选择最新的一个
excel_files.sort(reverse=True)
file_path = os.path.join(current_dir, excel_files[0])

print(f"正在读取文件：{file_path}")
print("="*120)

# 读取Excel文件，尝试不同的读取方式
df = None
file_ext = os.path.splitext(file_path)[1].lower()

if file_ext == '.xls':
    # 对于xls文件，先尝试pandas读取，如果失败则尝试转换
    try:
        # 尝试正常读取
        temp_df = pd.read_excel(file_path)
        if len(temp_df) > 0 and temp_df.shape[1] > 0:
            df = temp_df
        else:
            raise Exception("空文件")
    except Exception as e:
        print(f"[注意：pandas读取xls文件遇到问题: {str(e)[:50]}...]")
        print("[尝试使用Excel COM组件读取并转换...]")
        try:
            import win32com.client as win32
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            excel.Visible = False
            excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(os.path.abspath(file_path))
            output_path = os.path.join(current_dir, "temp_converted.xlsx")
            workbook.SaveAs(output_path, FileFormat=51)  # 51 = xlsx format
            workbook.Close()
            excel.Quit()
            df = pd.read_excel(output_path)
            print("[转换并读取成功！]")
            # 删除临时文件
            try:
                os.remove(output_path)
            except:
                pass
        except Exception as e2:
            print(f"[转换失败: {e2}]")
            print("[尝试使用xlrd读取原始数据...]")
            try:
                import xlrd
                wb = xlrd.open_workbook(file_path)
                sheet = wb.sheet_by_index(0)
                data = []
                for row_idx in range(sheet.nrows):
                    row_data = []
                    for col_idx in range(sheet.ncols):
                        cell = sheet.cell(row_idx, col_idx)
                        value = cell.value
                        # 处理日期类型
                        if cell.ctype == 3:  # xlrd.XL_CELL_DATE
                            try:
                                from xlrd import xldate
                                value = xldate.xldate_as_datetime(value, wb.datemode)
                            except:
                                pass
                        row_data.append(value)
                    data.append(row_data)
                df = pd.DataFrame(data)
                print("[使用xlrd读取成功！]")
            except Exception as e3:
                print(f"[xlrd读取也失败: {e3}]")
                import sys
                sys.exit(1)
else:
    # 对于xlsx文件，直接读取
    df = pd.read_excel(file_path)

# 重新读取原始数据
# df = pd.read_excel(file_path)

# 查找所有采购单的合同号、订单号和单据编号
print("正在分析采购单结构...")

# 找到所有的合同号行
contract_rows = []
for i in range(len(df)):
    val = df.iloc[i, 0]
    if isinstance(val, str) and '合同号' in val:
        contract_value = df.iloc[i, 1] if pd.notna(df.iloc[i, 1]) else ""
        if isinstance(contract_value, str):
            contract_value = contract_value.strip()
        contract_rows.append((i, contract_value))

print(f"   找到 {len(contract_rows)} 个合同号")

# 找到所有的单据编号行
bill_rows = []
for i in range(min(len(df), 1000)):
    val = df.iloc[i, 0]
    if isinstance(val, str) and '单据编号' in val:
        bill_value = df.iloc[i, 1] if pd.notna(df.iloc[i, 1]) else ""
        if isinstance(bill_value, str):
            bill_value = bill_value.strip()
        bill_rows.append((i, bill_value))

print(f"   找到 {len(bill_rows)} 个单据编号")

# 找到所有的订单号行
order_rows = []
for i in range(min(len(df), 1000)):
    val = df.iloc[i, 1]
    if isinstance(val, str) and '订单号' in val:
        # 提取【】中的订单号
        match = re.search(r'【([^】]+)】', val)
        if match:
            order_value = match.group(1)
            order_rows.append((i, order_value))

print(f"   找到 {len(order_rows)} 个订单号")
print("="*120)

# 定义有效的物料编码特征
def is_valid_inventory_code(code):
    """判断是否为有效的物料编码"""
    if pd.isna(code):
        return False
    
    code_str = str(code).strip()
    
    # 排除明显不是物料编码的内容
    exclude_keywords = ['VchCode', '产品信息', '表名', '系统日期', '系统时间', 
                       '登录日期', '操作员', '会计年度', '二维码', '制单日期',
                       '供应商', '结算单位', '收付款', '保存时间', '修改时间']
    
    for keyword in exclude_keywords:
        if keyword in code_str:
            return False
    
    # 物料编码通常是数字或字母数字组合，长度一般在5-20位
    # 匹配纯数字或字母数字组合（可能包含少量特殊字符如-/_）
    code_pattern = r'^[A-Za-z0-9\-_]{5,20}$'
    if re.match(code_pattern, code_str):
        return True
    
    # 也考虑一些特殊格式的物料编码
    # 检查是否包含明显的物料特征（如数字为主，长度适中）
    if len(code_str) >= 4 and len(code_str) <= 30:
        digit_count = sum(1 for c in code_str if c.isdigit())
        # 如果数字占比超过50%，可能是物料编码
        if digit_count / len(code_str) > 0.5:
            return True
    
    return False

# 重新提取有效数据
detail_data = []

# 找到所有物料明细的起始行（包含"行号"和"存货编号"的行）
detail_sections = []
for i in range(len(df)):
    val = df.iloc[i, 0]
    if isinstance(val, str) and '行号' in val:
        # 检查下一列是否是"存货编号"
        next_val = df.iloc[i, 1]
        if isinstance(next_val, str) and '存货编号' in next_val:
            detail_sections.append(i)

print(f"   找到 {len(detail_sections)} 个物料明细段")
print("="*120)

# 如果没有找到任何物料明细段，给出提示并退出
if len(detail_sections) == 0:
    print("[错误：未能找到物料明细表头！]")
    print("[请检查Excel文件格式是否正确]")
    print("[需要包含\"行号\"和\"存货编号\"的表头行]")
    import sys
    sys.exit(1)

# 为每个物料明细段匹配对应的合同号、订单号和单据编号
for section_idx, detail_start_row in enumerate(detail_sections):
    # 确定这个明细段所属的采购单信息
    # 向上查找最近的合同号、订单号和单据编号
    current_contract = ""
    current_order = ""
    current_bill = ""
    
    # 向上查找最近的合同号
    for contract_row, contract_value in reversed(contract_rows):
        if contract_row < detail_start_row:
            current_contract = contract_value
            break
    
    # 向上查找最近的订单号
    for order_row, order_value in reversed(order_rows):
        if order_row < detail_start_row:
            current_order = order_value
            break
    
    # 向上查找最近的单据编号
    for bill_row, bill_value in reversed(bill_rows):
        if bill_row < detail_start_row:
            current_bill = bill_value
            break
    
    print(f"[处理第 {section_idx + 1} 个物料明细段（从第 {detail_start_row} 行开始）]")
    print(f"   合同号：{current_contract}")
    print(f"   订单号：{current_order}")
    print(f"   单据编号：{current_bill}")
    
    # 从明细表头后开始提取数据，但要在遇到下一个明细段之前停止
    next_section_start = detail_sections[section_idx + 1] if section_idx + 1 < len(detail_sections) else len(df)
    
    for i in range(detail_start_row + 1, next_section_start):
        # 获取存货编号（第2列，索引1）
        inventory_code = df.iloc[i, 1]
        
        # 如果遇到空行或下一个表头，停止提取
        if pd.isna(inventory_code) or str(inventory_code).strip() == "":
            continue
        
        # 检查是否为有效的物料编码
        # 排除合同号、订单号、单据编号等非物料行
        if is_valid_inventory_code(inventory_code):
            # 跳过包含"合同号"、"订单号"、"单据编号"等关键字的行
            row_str = str(df.iloc[i, 0]) if df.shape[1] > 0 else ""
            if any(keyword in row_str for keyword in ['合同号', '订单号', '单据编号']):
                continue
                
            # 获取数量（在表头中的位置）
            quantity_col = None
            for j in range(df.shape[1]):
                val = df.iloc[detail_start_row, j]
                if isinstance(val, str) and '数量' in val:
                    quantity_col = j
                    break
            
            if quantity_col is None:
                quantity_col = 16  # 默认第17列
            
            quantity = df.iloc[i, quantity_col] if df.shape[1] > quantity_col else 0
            if pd.isna(quantity) or str(quantity).strip() == "" or str(quantity).lower() == "数量":
                quantity = 0
            else:
                try:
                    quantity = float(quantity)
                except:
                    quantity = 0
            
            # 获取金额（在表头中的位置）
            amount_col = None
            for j in range(df.shape[1]):
                val = df.iloc[detail_start_row, j]
                if isinstance(val, str) and '金额' in val:
                    amount_col = j
                    break
            
            if amount_col is None:
                amount_col = 22  # 默认第23列
            
            amount = df.iloc[i, amount_col] if df.shape[1] > amount_col else 0
            if pd.isna(amount) or str(amount).strip() == "" or str(amount).lower() == "金额":
                amount = 0
            else:
                try:
                    amount = float(amount)
                except:
                    amount = 0
            
            # 获取采购单号（第54列，索引53），如果列数不够则跳过
            vch_code = ""
            if df.shape[1] > 53:
                vch_code = df.iloc[i, 53]
            if pd.isna(vch_code):
                vch_code = ""
            else:
                vch_code = str(vch_code).strip()
                # 提取纯数字的采购单号（去掉可能的前缀）
                vch_match = re.search(r'(\d{5,})', vch_code)
                if vch_match:
                    vch_code = vch_match.group(1)
            
            row_dict = {
                "行号": df.iloc[i, 0] if pd.notna(df.iloc[i, 0]) else "",
                "物料编码(存货编号)": str(inventory_code).strip(),
                "物料名称(存货全名)": df.iloc[i, 2] if pd.notna(df.iloc[i, 2]) else "",
                "仓库": df.iloc[i, 3] if pd.notna(df.iloc[i, 3]) else "",
                "规格": df.iloc[i, 4] if pd.notna(df.iloc[i, 4]) else "",
                "型号": df.iloc[i, 5] if pd.notna(df.iloc[i, 5]) else "",
                "单位": df.iloc[i, 8] if pd.notna(df.iloc[i, 8]) else "",
                "数量": quantity,
                "单价": df.iloc[i, 21] if pd.notna(df.iloc[i, 21]) else 0,
                "金额": amount,
                "价税合计": df.iloc[i, 29] if pd.notna(df.iloc[i, 29]) else 0,
                "采购单号": vch_code,
                "合同号": current_contract,
                "订单号": current_order,
                "单据编号": current_bill
            }
            detail_data.append(row_dict)

# 创建优化后的DataFrame
detail_df = pd.DataFrame(detail_data)

# 如果没有提取到任何数据，给出提示并退出
if len(detail_df) == 0:
    print("[警告：未提取到任何有效物料数据！]")
    print("[可能原因：]")
    print("[1. 物料编码格式不符合要求]")
    print("[2. 数量或金额为0或为空]")
    print("[3. 文件格式异常]")
    import sys
    sys.exit(0)

# 进一步过滤：只保留数量>0或金额>0的行（确保是有效采购数据）
detail_df = detail_df[(detail_df['数量'] > 0) | (detail_df['金额'] > 0)]

# 重置行号
detail_df = detail_df.reset_index(drop=True)

# 显示优化后的结果
print("="*120)
print("优化后的采购物料明细提取结果")
print("="*120)

print(f"\n[数据提取完成！]")
print(f"[共提取到 {len(detail_df)} 行有效采购物料数据]")
print(f"[包含 {detail_df['物料编码(存货编号)'].nunique()} 个不同的物料编码]")
print(f"[涉及 {detail_df['采购单号'].nunique()} 个不同的采购单号]")
print(f"[涉及 {detail_df['合同号'].nunique()} 个不同的合同号]")
print(f"[涉及 {detail_df['单据编号'].nunique()} 个不同的单据编号]")

print(f"\n[数据统计汇总：]")
print(f"   总采购数量：{detail_df['数量'].sum():.2f}")
print(f"   总采购金额：{detail_df['金额'].sum():.2f} 元")
print(f"   总价税合计：{detail_df['价税合计'].sum():.2f} 元")

print(f"\n[仓库分布：]")
warehouse_stats = detail_df['仓库'].value_counts()
for warehouse, count in warehouse_stats.head(10).items():
    if warehouse:
        print(f"   {warehouse}: {count} 项物料")

print(f"\n[前15行有效数据预览：]")
print(detail_df.head(15).to_string(index=False, max_colwidth=30))

# 保存优化后的结果到Excel文件
output_file = os.path.join(current_dir, '采购单_有效物料编码明细_优化版.xlsx')

# 使用ExcelWriter创建更规范的Excel文件
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 写入主要的物料明细
    detail_df.to_excel(writer, sheet_name='物料采购明细', index=False)
    
    # 创建统计汇总表
    summary_data = {
        '统计项目': [
            '总有效物料行数',
            '不同物料编码数量',
            '不同采购单号数量',
            '涉及仓库数量',
            '总采购数量',
            '总采购金额(元)',
            '总价税合计(元)',
            '平均单项金额(元)'
        ],
        '数值': [
            len(detail_df),
            detail_df['物料编码(存货编号)'].nunique(),
            detail_df['采购单号'].nunique(),
            detail_df['仓库'].nunique(),
            f"{detail_df['数量'].sum():.2f}",
            f"{detail_df['金额'].sum():.2f}",
            f"{detail_df['价税合计'].sum():.2f}",
            f"{detail_df['金额'].mean():.2f}" if len(detail_df) > 0 else "0.00"
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='数据统计汇总', index=False)
    
    # 创建物料编码清单（去重）
    inventory_list = detail_df[['物料编码(存货编号)', '物料名称(存货全名)', '规格', '单位']].drop_duplicates()
    inventory_list = inventory_list.sort_values('物料编码(存货编号)').reset_index(drop=True)
    inventory_list.to_excel(writer, sheet_name='物料编码清单', index=False)

print(f"\n[文件保存完成！]")
print(f"   保存路径：{output_file}")
print(f"   包含3个工作表：")
print(f"     1. 物料采购明细 - 所有有效采购数据")
print(f"     2. 数据统计汇总 - 关键指标统计")
print(f"     3. 物料编码清单 - 去重后的物料编码列表")

# 显示物料编码清单预览
print(f"\n[物料编码清单预览（前10个）：]")
inventory_preview = inventory_list.head(10)[['物料编码(存货编号)', '物料名称(存货全名)']]
for idx, row in inventory_preview.iterrows():
    print(f"   {row['物料编码(存货编号)']:15s} - {row['物料名称(存货全名)']}")