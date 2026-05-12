import sys
import os
import threading
from datetime import datetime
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import winreg  # Windows注册表操作
import PIL.Image
import pystray

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("错误: 请先安装watchdog库")
    print("运行: pip install watchdog")
    sys.exit(1)


class FileChangeHandler(FileSystemEventHandler):
    """文件变化处理器"""

    def __init__(self, callback, event_types):
        super().__init__()
        self.callback = callback
        self.event_types = event_types

    def on_created(self, event):
        if not event.is_directory and 'created' in self.event_types:
            self.callback('新增', event.src_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def on_deleted(self, event):
        if not event.is_directory and 'deleted' in self.event_types:
            self.callback('删除', event.src_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def on_modified(self, event):
        if not event.is_directory and 'modified' in self.event_types:
            self.callback('修改', event.src_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def on_moved(self, event):
        if not event.is_directory:
            if 'deleted' in self.event_types:
                self.callback('删除', event.src_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if 'created' in self.event_types:
                self.callback('新增', event.dest_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class FolderMonitorTool:
    """文件夹监控工具"""

    def __init__(self):
        self.watch_paths = []
        self.observers = {}
        self.event_types = {'created', 'deleted', 'modified'}
        self.temp_extensions = {'.tmp', '.temp', '.bak', '.pyc', '.pyo', '~'}
        self.is_monitoring = False
        self.filter_temp = True
        self.auto_start = True  # 默认自动启动监控
        self.tray_icon = None  # 托盘图标
        self.tray_running = False  # 托盘是否正在运行
        self.tray_thread = None  # 托盘线程

        # 获取程序所在目录（兼容打包后的exe）
        if getattr(sys, 'frozen', False):
            # exe打包后使用exe所在目录
            self.app_dir = os.path.dirname(sys.executable)
        else:
            self.app_dir = os.path.dirname(os.path.abspath(__file__))

        self.config_file = os.path.join(self.app_dir, 'monitor_config.json')

        self.root = tk.Tk()
        self.root.title('文件夹监控工具')
        self.root.geometry('950x650')
        self.root.minsize(800, 550)

        # 创建托盘图标
        self.create_tray_icon()

        self.setup_ui()
        self.load_config()
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.root.bind('<Unmap>', self.on_minimize)  # 绑定最小化事件

    def create_tray_icon(self):
        """创建系统托盘图标"""
        # 创建一个简单的图标图像（使用代码生成）
        try:
            # 创建一个32x32的图标
            icon_image = PIL.Image.new('RGB', (32, 32), color='#4CAF50')
            # 在图标上添加一个简单的符号
            from PIL import ImageDraw
            draw = ImageDraw.Draw(icon_image)
            draw.ellipse([4, 4, 28, 28], fill='#FFFFFF', outline='#4CAF50', width=2)
            draw.text((10, 8), 'M', fill='#4CAF50')

            # 创建托盘图标菜单
            menu = pystray.Menu(
                pystray.MenuItem('显示窗口', self.show_window, default=True),
                pystray.MenuItem('开始监控', self.tray_start_monitoring),
                pystray.MenuItem('停止监控', self.tray_stop_monitoring),
                pystray.MenuItem('退出程序', self.exit_program)
            )

            # 创建托盘图标
            self.tray_icon = pystray.Icon(
                'folder_monitor',
                icon_image,
                '文件夹监控工具',
                menu
            )

        except Exception as e:
            print(f"创建托盘图标失败: {e}")
            self.tray_icon = None

    def on_minimize(self, event):
        """窗口最小化事件"""
        if self.root.state() == 'iconic':
            # 窗口被最小化，隐藏到托盘
            self.root.withdraw()
            if self.tray_icon and not self.tray_running:
                # 在新线程中运行托盘图标
                self.tray_thread = threading.Thread(target=self.run_tray_icon, daemon=True)
                self.tray_thread.start()

    def run_tray_icon(self):
        """运行托盘图标（在新线程中）"""
        if self.tray_icon:
            self.tray_running = True
            self.tray_icon.run_detached()
            self.tray_running = False

    def show_window(self, icon=None, item=None):
        """显示主窗口"""
        self.root.after(0, self._show_window)

    def _show_window(self):
        """在主线程中显示窗口"""
        self.root.deiconify()  # 显示窗口
        self.root.state('normal')  # 恢复正常状态
        self.root.lift()  # 提升到最前
        self.root.focus_force()  # 获取焦点

    def tray_start_monitoring(self, icon=None, item=None):
        """托盘菜单开始监控"""
        self.root.after(0, self.start_monitoring)

    def tray_stop_monitoring(self, icon=None, item=None):
        """托盘菜单停止监控"""
        self.root.after(0, self.stop_monitoring)

    def exit_program(self, icon=None, item=None):
        """退出程序"""
        # 停止托盘图标
        if self.tray_icon:
            self.tray_icon.stop()
        # 在主线程中关闭程序
        self.root.after(0, self.force_close)

    def force_close(self):
        """强制关闭程序"""
        if self.is_monitoring:
            self.stop_monitoring()
        self.root.quit()
        self.root.destroy()

    def setup_ui(self):
        """初始化界面"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 左侧面板 - 控制面板
        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.pack(side='left', fill='both', padx=(0, 5))

        # 监控路径标签
        ttk.Label(left_frame, text='监控路径列表:', font=('Arial', 10, 'bold')).pack(anchor='w')

        # 路径列表框
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill='both', expand=True, pady=5)

        self.path_listbox = tk.Listbox(list_frame, height=8, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.path_listbox.yview)
        self.path_listbox.configure(yscrollcommand=scrollbar.set)
        self.path_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # 路径输入
        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill='x', pady=5)

        ttk.Label(input_frame, text='路径:').pack(anchor='w')
        self.path_entry = ttk.Entry(input_frame, font=('Arial', 9))
        self.path_entry.pack(fill='x', pady=2)

        # 按钮框架
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill='x', pady=5)

        ttk.Button(btn_frame, text='添加路径', command=self.add_path).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='浏览...', command=self.browse_folder).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='删除选中', command=self.remove_path).pack(side='left', padx=2)

        # 事件类型过滤
        event_frame = ttk.LabelFrame(left_frame, text='监控事件类型:', padding=5)
        event_frame.pack(fill='x', pady=5)

        self.check_created = tk.BooleanVar(value=True)
        self.check_deleted = tk.BooleanVar(value=True)
        self.check_modified = tk.BooleanVar(value=True)

        ttk.Checkbutton(event_frame, text='新增 (Created)',
                        variable=self.check_created,
                        command=self.update_event_types).pack(anchor='w')
        ttk.Checkbutton(event_frame, text='删除 (Deleted)',
                        variable=self.check_deleted,
                        command=self.update_event_types).pack(anchor='w')
        ttk.Checkbutton(event_frame, text='修改 (Modified)',
                        variable=self.check_modified,
                        command=self.update_event_types).pack(anchor='w')

        # 临时文件过滤
        temp_frame = ttk.LabelFrame(left_frame, text='临时文件过滤:', padding=5)
        temp_frame.pack(fill='x', pady=5)

        self.filter_temp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(temp_frame, text='过滤临时文件 (.tmp, .bak, ~等)',
                        variable=self.filter_temp_var,
                        command=self.toggle_filter).pack(anchor='w')

        ttk.Label(temp_frame, text='排除: .tmp, .temp, .bak, .pyc, ~',
                  foreground='gray', font=('Arial', 8)).pack(anchor='w')

        # 启动选项
        startup_frame = ttk.LabelFrame(left_frame, text='启动选项:', padding=5)
        startup_frame.pack(fill='x', pady=5)

        self.auto_start_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(startup_frame, text='程序启动时自动开始监控',
                        variable=self.auto_start_var,
                        command=self.toggle_auto_start).pack(anchor='w')

        self.auto_run_var = tk.BooleanVar(value=False)
        self.check_auto_run = ttk.Checkbutton(startup_frame, text='开机自启动',
                                               variable=self.auto_run_var,
                                               command=self.toggle_auto_run)
        self.check_auto_run.pack(anchor='w')

        # 更新开机自启动状态
        self.update_auto_run_checkbox()

        # 控制按钮
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill='x', pady=10)

        self.start_btn = ttk.Button(control_frame, text='开始监控', command=self.start_monitoring)
        self.start_btn.pack(side='left', padx=2, expand=True, fill='x')

        self.stop_btn = ttk.Button(control_frame, text='停止监控', command=self.stop_monitoring, state='disabled')
        self.stop_btn.pack(side='left', padx=2, expand=True, fill='x')

        ttk.Button(left_frame, text='保存设置', command=self.save_config).pack(fill='x', pady=2)
        ttk.Button(left_frame, text='清空日志', command=self.clear_log).pack(fill='x', pady=2)

        # 右侧面板 - 日志显示
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='left', fill='both', expand=True)

        ttk.Label(right_frame, text='变化日志:', font=('Arial', 10, 'bold')).pack(anchor='w')

        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(right_frame, font=('Consolas', 9),
                                                  bg='#1e1e1e', fg='#d4d4d4',
                                                  insertbackground='white')
        self.log_text.pack(fill='both', expand=True)
        self.log_text.tag_config('新增', foreground='#4CAF50', font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('删除', foreground='#f44336', font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('修改', foreground='#2196F3', font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('info', foreground='#9e9e9e', font=('Consolas', 9))

        # 状态栏
        self.status_var = tk.StringVar(value='就绪')
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.pack(side='bottom', fill='x')

    def is_in_startup(self):
        """检查是否在开机启动项中"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, "文件夹监控工具")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False

    def add_to_startup(self):
        """添加到开机启动项"""
        try:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "文件夹监控工具", 0, winreg.REG_SZ, f'"{exe_path}"')
            winreg.CloseKey(key)
            return True
        except Exception as e:
            messagebox.showerror('错误', f'添加开机启动失败:\n{str(e)}')
            return False

    def remove_from_startup(self):
        """从开机启动项移除"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_WRITE)
            try:
                winreg.DeleteValue(key, "文件夹监控工具")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            messagebox.showerror('错误', f'移除开机启动失败:\n{str(e)}')
            return False

    def update_auto_run_checkbox(self):
        """更新开机自启动复选框状态"""
        in_startup = self.is_in_startup()
        self.auto_run_var.set(in_startup)

    def toggle_auto_run(self):
        """切换开机自启动"""
        if self.auto_run_var.get():
            self.add_to_startup()
            self.status_var.set('已添加到开机启动项')
        else:
            self.remove_from_startup()
            self.status_var.set('已从开机启动项移除')

    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 加载监控路径
                if 'paths' in config:
                    self.watch_paths.clear()
                    self.path_listbox.delete(0, 'end')
                    for path in config['paths']:
                        if os.path.exists(path):
                            self.watch_paths.append(path)
                            self.path_listbox.insert('end', path)

                # 加载事件类型
                if 'event_types' in config:
                    self.check_created.set('created' in config['event_types'])
                    self.check_deleted.set('deleted' in config['event_types'])
                    self.check_modified.set('modified' in config['event_types'])

                # 加载临时文件过滤
                if 'filter_temp' in config:
                    self.filter_temp_var.set(config['filter_temp'])
                    self.filter_temp = config['filter_temp']

                # 加载自动启动
                if 'auto_start' in config:
                    self.auto_start_var.set(config['auto_start'])
                    self.auto_start = config['auto_start']

                self.update_event_types()

                # 如果有路径且启用了自动启动,则开始监控
                if self.watch_paths and self.auto_start:
                    self.root.after(500, self.start_monitoring)

        except Exception as e:
            print(f"加载配置失败: {e}")

    def save_config(self):
        """保存配置"""
        try:
            # 获取当前列表框中的所有路径
            current_paths = []
            for i in range(self.path_listbox.size()):
                current_paths.append(self.path_listbox.get(i))

            config = {
                'paths': current_paths,
                'event_types': list(self.event_types),
                'filter_temp': self.filter_temp,
                'auto_start': self.auto_start_var.get()
            }

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            self.status_var.set('配置已保存')
            messagebox.showinfo('提示', f'配置已保存！\n监控路径数量: {len(current_paths)}')

        except Exception as e:
            messagebox.showerror('错误', f'保存配置失败:\n{str(e)}')

    def browse_folder(self):
        """浏览文件夹"""
        folder = filedialog.askdirectory(title='选择监控文件夹')
        if folder:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder)

    def add_path(self):
        """添加监控路径"""
        path = self.path_entry.get().strip()

        if not path:
            messagebox.showwarning('警告', '请输入或选择文件夹路径！')
            return

        if not os.path.exists(path):
            messagebox.showwarning('警告', '路径不存在！')
            return

        if not os.path.isdir(path):
            messagebox.showwarning('警告', '请选择文件夹路径！')
            return

        # 获取当前列表中的所有路径进行检查
        current_paths = list(self.path_listbox.get(0, 'end'))
        if path in current_paths:
            messagebox.showwarning('警告', '该路径已在监控列表中！')
            return

        self.watch_paths.append(path)
        self.path_listbox.insert('end', path)
        self.path_entry.delete(0, 'end')
        self.status_var.set(f'已添加监控路径: {path}')

        # 如果正在监控,立即开始监控新路径
        if self.is_monitoring:
            self.stop_monitoring()
            self.start_monitoring()

    def remove_path(self):
        """移除监控路径"""
        selection = self.path_listbox.curselection()
        if not selection:
            messagebox.showwarning('警告', '请选择要移除的路径！')
            return

        index = selection[0]
        path = self.path_listbox.get(index)

        # 如果正在监控,先停止该路径的监控
        if path in self.observers:
            self.observers[path].stop()
            del self.observers[path]

        # 从列表中移除
        self.path_listbox.delete(index)
        if path in self.watch_paths:
            self.watch_paths.remove(path)
        self.status_var.set(f'已移除监控路径: {path}')

    def update_event_types(self):
        """更新监控的事件类型"""
        self.event_types = set()
        if self.check_created.get():
            self.event_types.add('created')
        if self.check_deleted.get():
            self.event_types.add('deleted')
        if self.check_modified.get():
            self.event_types.add('modified')

        # 如果没有选中任何类型,默认选择所有
        if not self.event_types:
            self.event_types = {'created', 'deleted', 'modified'}
            self.check_created.set(True)
            self.check_deleted.set(True)
            self.check_modified.set(True)
            messagebox.showwarning('警告', '至少需要选择一种事件类型！')

    def toggle_filter(self):
        """切换临时文件过滤"""
        self.filter_temp = self.filter_temp_var.get()

    def toggle_auto_start(self):
        """切换自动启动监控"""
        self.auto_start = self.auto_start_var.get()

    def is_temp_file(self, path):
        """检查是否为临时文件"""
        if not self.filter_temp:
            return False

        filename = os.path.basename(path)

        # 检查文件名是否以~开头或结尾
        if filename.startswith('~') or filename.endswith('~'):
            return True

        # 检查扩展名
        for ext in self.temp_extensions:
            if path.lower().endswith(ext):
                return True

        return False

    def on_file_change(self, event_type, file_path, timestamp):
        """文件变化回调 - 在主线程中执行"""
        # 过滤临时文件
        if self.is_temp_file(file_path):
            return

        # 获取标签名，映射中文事件类型
        tag_map = {'新增': '新增', '删除': '删除', '修改': '修改'}
        tag = tag_map.get(event_type, 'info')

        # 使用统一格式显示日志，确保所有事件都有颜色
        self.log_text.insert('end', f'[{timestamp}] ', 'info')
        self.log_text.insert('end', f'[{event_type}] ', tag)
        self.log_text.insert('end', f'{file_path}\n', tag)
        self.log_text.see('end')

    def start_monitoring(self):
        """开始监控"""
        if not self.watch_paths:
            self.status_var.set('请先添加要监控的路径！')
            return

        if self.is_monitoring:
            return

        self.log_text.delete('1.0', 'end')
        self.append_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始监控...")
        self.append_log(f"监控路径数量: {len(self.watch_paths)}")
        self.append_log(f"事件类型: {', '.join(self.event_types)}")
        self.append_log("-" * 60)

        for path in self.watch_paths:
            try:
                if not os.path.exists(path):
                    self.append_log(f"[跳过] 路径不存在: {path}")
                    continue

                event_handler = FileChangeHandler(self.on_file_change, self.event_types)

                observer = Observer()
                observer.schedule(event_handler, path, recursive=True)
                observer.start()
                self.observers[path] = observer

                self.append_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始监控: {path}")

            except Exception as e:
                self.append_log(f"[错误] 无法监控 {path}: {str(e)}")

        self.is_monitoring = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_var.set(f'正在监控 {len(self.watch_paths)} 个路径...')

    def stop_monitoring(self):
        """停止监控"""
        if not self.is_monitoring:
            return

        for path, observer in self.observers.items():
            try:
                observer.stop()
                observer.join(timeout=1)
            except:
                pass

        self.observers.clear()
        self.is_monitoring = False

        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.append_log(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 停止监控")
        self.status_var.set('监控已停止')

    def append_log(self, message):
        """添加日志消息"""
        self.log_text.insert('end', message + '\n', 'info')
        self.log_text.see('end')

    def clear_log(self):
        """清空日志"""
        self.log_text.delete('1.0', 'end')
        self.status_var.set('日志已清空')

    def on_closing(self):
        """窗口关闭事件 - 询问用户选择"""
        # 弹出确认对话框
        choice = messagebox.askyesnocancel('退出确认',
            '是否退出程序？\n\n'
            '是 - 退出程序\n'
            '否 - 最小化到托盘（继续后台监控）\n'
            '取消 - 取消关闭')

        if choice is True:
            # 用户选择退出
            self.force_close()
        elif choice is False:
            # 用户选择最小化到托盘
            self.root.withdraw()
            if self.tray_icon and not self.tray_running:
                self.tray_thread = threading.Thread(target=self.run_tray_icon, daemon=True)
                self.tray_thread.start()
            self.status_var.set('程序已最小化到托盘，点击托盘图标可恢复')
        # choice is None (取消) - 不做任何操作

    def run(self):
        """运行应用"""
        self.root.mainloop()


if __name__ == '__main__':
    app = FolderMonitorTool()
    app.run()
