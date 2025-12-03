import numpy as np
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
from matplotlib import rcParams
import tkinter as tk
from tkinter import ttk
import pyperclip  # 用于复制到剪贴板
import sys
import os

def resource_path(relative_path):
    """获取资源的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class PolyFitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("传感器数据多项式拟合")
        self.root.geometry("600x400")  # 设置初始窗口大小
        self.root.minsize(400, 300)   # 设置最小窗口尺寸
        
        # 设置图标
        try:
            icon_path = resource_path('favicon.ico')
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except Exception as e:
            print(f"无法加载图标: {e}")
        
        # 创建主框架，用于布局管理
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入区域框架
        input_frame = ttk.LabelFrame(self.main_frame, text="输入数据", padding=10)
        input_frame.pack(fill=tk.X, pady=(0,10))
        
        # A传感器输入
        ttk.Label(input_frame, text="X传感器值(逗号分隔):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.a_entry = ttk.Entry(input_frame)
        self.a_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # B传感器输入
        ttk.Label(input_frame, text="Y传感器值(逗号分隔):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.b_entry = ttk.Entry(input_frame)
        self.b_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # 多项式阶数选择
        ttk.Label(input_frame, text="多项式阶数:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.degree_var = tk.IntVar(value=2)
        self.degree_spin = ttk.Spinbox(input_frame, from_=1, to=10, textvariable=self.degree_var)
        self.degree_spin.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # 配置输入区域的列权重
        input_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(0,10))
        
        self.fit_btn = ttk.Button(button_frame, text="执行拟合", command=self.fit_data)
        self.fit_btn.pack(side=tk.LEFT, padx=5)
        
        self.copy_btn = ttk.Button(button_frame, text="复制公式", command=self.copy_formula)
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(self.main_frame, text="拟合结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 配置主框架的权重
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
    def fit_data(self):
        try:
            a_values = np.array([float(x) for x in self.a_entry.get().split(",")])
            b_values = np.array([float(x) for x in self.b_entry.get().split(",")])
            degree = self.degree_var.get()
            
            # 多项式拟合
            poly_coeffs = Polynomial.fit(a_values, b_values, deg=degree)
            coeffs = poly_coeffs.convert().coef
            formula = " + ".join([f"{coeff:.4f} * x^{i}" for i, coeff in enumerate(coeffs)])
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"拟合公式: b = {formula}\n\n")
            self.result_text.insert(tk.END, f"使用方法: 将X传感器值代入x计算得到修正后的Y传感器值")

            # 绘制图形
            rcParams['font.sans-serif'] = ['SimHei']
            rcParams['axes.unicode_minus'] = False
            
            x_fit = np.linspace(min(a_values), max(a_values), 100)
            y_fit = poly_coeffs(x_fit)
            
            plt.figure()
            plt.scatter(a_values, b_values, color="red", label="实际值")
            plt.plot(x_fit, y_fit, color="blue", label=f"拟合曲线 (degree={degree})")
            plt.xlabel("A传感器值")
            plt.ylabel("B传感器值")
            plt.title("多项式拟合效果")
            plt.legend()
            plt.grid()
            plt.show()
            
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"错误: {str(e)}")
    
    def copy_formula(self):
        """将拟合公式复制到剪贴板"""
        formula = self.result_text.get(1.0, tk.END).strip()
        if formula and not formula.startswith("错误"):
            pyperclip.copy(formula.split("\n")[0])  # 只复制第一行公式
            self.result_text.insert(tk.END, "\n\n公式已复制到剪贴板！")
    def evaluate_fit(self, a_values, b_values, poly_coeffs):
        #  """评估拟合结果"""
        # 计算拟合值
        b_fit = poly_coeffs(a_values)
        
        # 决定系数 R^2
        ss_total = np.sum((b_values - np.mean(b_values))**2)
        ss_residual = np.sum((b_values - b_fit)**2)
        r_squared = 1 - (ss_residual / ss_total)
        
        # 均方根误差 RMSE
        rmse = np.sqrt(np.mean((b_values - b_fit)**2))
        # 自动评估拟合结果
        r_squared, rmse = self.evaluate_fit(a_values, b_values, poly_coeffs)
        self.result_text.insert(tk.END, f"\n\n拟合评估:\nR^2 = {r_squared:.4f}\nRMSE = {rmse:.4f}")
        return r_squared, rmse
if __name__ == "__main__":
    root = tk.Tk()
    app = PolyFitApp(root)
    root.mainloop()

    