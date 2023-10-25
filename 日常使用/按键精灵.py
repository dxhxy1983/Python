import pyautogui
import keyboard
pyautogui.FAILSAFE = True
# pyautogui.moveTo(1000,500,duration=5) #鼠标移动到坐标(1000,500)位置，duration参数是移动持续的时间

# pyautogui.scroll(clicks=-500)#当前页面靠鼠标滑轮向下拉500个像素单位；反之，如果想向上拉则将clicks参数改为正数即可

# pyautogui.click(1000,500,duration=2,button="left") # 移动到指定位置，单击左键
# pyautogui.click(1000,600,duration=2,button="right") # 移动到指定位置，单击右键
# pyautogui.click(1000,700,duration=2,button="middle") # 移动到指定位置，单击中键

# pyautogui.doubleClick(1000,500,duration=2) # 移动到指定位置，双击右键
# pyautogui.rightClick(1000,600,duration=2)  # 移动到指定位置，双击右键
# pyautogui.middleClick(1000,700,duration=2) # 移动到指定位置，双击中键

# pyautogui.dragTo(1000,500,duration=2)   
# pyautogui.dragRel(1000,500,duration=2)
# pyautogui.dragTo方法是把鼠标拖拉至目的地坐标；
# pyautogui.dragRel方法则是拖动对应的像素单位；

# pyautogui.hotkey('ctrl','v')#热键功能i
# pyautogui.press('i')
# pyautogui.typewrite('maishu', 0.1)
while True:
    if keyboard.is_pressed("F8"):                       
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.typewrite("Pr",0.1)
        
        pyautogui.press('shift')

