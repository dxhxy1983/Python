import os
import shutil
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
import configparser

from pystray import Icon, MenuItem

# 默认的更新间隔（秒）
default_interval = 3600  # 每小时检查一次

# 获取当前运行文件的路径和配置文件路径
current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, 'paths.ini')

# 读取配置文件中的路径
def load_paths():
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        if 'Paths' in config:
            return config['Paths']['SharedFolder'], config['Paths']['LocalFolder']
    # 如果配置文件不存在或者没有定义'Paths'节，则返回默认路径
    return 'C:/SharedFolder', 'D:/LocalFolder'

# 保存路径到配置文件
def save_paths(shared_folder, local_folder):
    config = configparser.ConfigParser()
    config['Paths'] = {
        'SharedFolder': shared_folder,
        'LocalFolder': local_folder
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)

# 加载图标文件并创建图像对象
def load_icon(icon_path):
    with open(icon_path, 'rb') as f:
        image = Image.open(f)
        return image

# 创建系统托盘图标
def create_tray_icon(shared_folder, local_folder, icon_path):
    icon_image = load_icon(icon_path)
    icon = Icon("文件同步应用", icon=icon_image)
    icon.menu = (MenuItem("立即更新", lambda: sync_now(shared_folder, local_folder)), MenuItem("退出", on_quit))
    return icon

# 同步文件
def sync_files(shared_folder, local_folder):
    # 遍历共享文件夹中的所有文件
    for filename in os.listdir(shared_folder):
        src_path = os.path.join(shared_folder, filename)
        dest_path = os.path.join(local_folder, filename)
        # 检查文件是否已经存在于本地目标文件夹中
        if not os.path.exists(dest_path) or os.stat(src_path).st_mtime > os.stat(dest_path).st_mtime:
            # 如果文件不存在或者共享文件夹中的文件修改时间晚于本地文件的修改时间，则进行同步
            shutil.copy(src_path, dest_path)
            print(f"Synced: {src_path} -> {dest_path}")

    # 检查目标文件夹中的文件是否在共享文件夹中存在，如果不存在则删除
    for filename in os.listdir(local_folder):
        dest_path = os.path.join(local_folder, filename)
        src_path = os.path.join(shared_folder, filename)
        if not os.path.exists(src_path):
            os.remove(dest_path)
            print(f"Deleted: {dest_path}")

# 立即同步
def sync_now(shared_folder, local_folder):
    sync_files(shared_folder, local_folder)

# 更新间隔设置
def update_interval():
    global check_interval
    check_interval = interval_var.get()

# 开始同步
def start_sync():
    shared_folder = shared_folder_var.get()
    local_folder = local_folder_var.get()
    if shared_folder and local_folder and os.path.isdir(shared_folder) and os.path.isdir(local_folder):
        # 保存路径到配置文件
        save_paths(shared_folder, local_folder)
        thread = threading.Thread(target=main, args=(shared_folder, local_folder))
        thread.daemon = True
        thread.start()
    else:
        messagebox.showerror("错误", "请输入有效的文件夹路径！")

# 主同步功能
def main(shared_folder, local_folder):
    while True:
        # 定期检查共享文件夹并同步文件
        sync_files(shared_folder, local_folder)
        # 等待一段时间后再次检查
        time.sleep(check_interval)

# 退出程序
def on_quit(icon, item):
    icon.stop()
    os._exit(0)

# 创建主窗口
root = tk.Tk()
root.title("文件同步应用")

# 获取上一次保存的路径
shared_folder, local_folder = load_paths()

# 创建网络文件夹路径输入框
shared_folder_frame = ttk.Frame(root)
shared_folder_frame.pack(pady=10, fill='x')
shared_folder_label = ttk.Label(shared_folder_frame, text="网络文件夹路径:")
shared_folder_label.pack(side='left', padx=5)
shared_folder_var = tk.StringVar(value=shared_folder)
shared_folder_entry = ttk.Entry(shared_folder_frame, textvariable=shared_folder_var)
shared_folder_entry.pack(side='left', padx=5, fill='x', expand=True)

# 创建本地文件夹路径输入框
local_folder_frame = ttk.Frame(root)
local_folder_frame.pack(pady=10, fill='x')
local_folder_label = ttk.Label(local_folder_frame, text="本地文件夹路径:")
local_folder_label.pack(side='left', padx=5)
local_folder_var = tk.StringVar(value=local_folder)
local_folder_entry = ttk.Entry(local_folder_frame, textvariable=local_folder_var)
local_folder_entry.pack(side='left', padx=5, fill='x', expand=True)

# 创建更新间隔设置框架
interval_frame = ttk.Frame(root)
interval_frame.pack(pady=10, fill='x')
interval_label = ttk.Label(interval_frame, text="更新间隔（秒）:")
interval_label.pack(side='left', padx=5)
interval_var = tk.IntVar(value=default_interval)
interval_entry = ttk.Entry(interval_frame, textvariable=interval_var)
interval_entry.pack(side='left', padx=5, fill='x', expand=True)
update_button = ttk.Button(interval_frame, text="更新", command=update_interval)
update_button.pack(side='left', padx=5)

# 创建开始同步按钮
start_button = ttk.Button(root, text="开始同步", command=start_sync)
start_button.pack(pady=10)

# 显示窗口
root.mainloop()

# 获取输入路径
shared_folder = shared_folder_var.get()
local_folder = local_folder_var.get()
icon_path = os.path.join(current_path, 'favicon.ico')  # 图标文件路径

# 创建系统托盘图标并运行主循环
def run_tray_icon():
    if os.name == "nt":
        icon = create_tray_icon(shared_folder, local_folder, icon_path)
        icon.run()
    else:
        messagebox.showerror("错误", "系统托盘仅在Windows系统下支持。")

thread = threading.Thread(target=run_tray_icon)
thread.daemon = True
thread.start()
