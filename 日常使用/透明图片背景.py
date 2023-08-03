from PIL import Image
  
# img = Image.open(r'F:\myDoc\github\Python\日常使用\1.png')
# rgba = img.convert("RGBA")
# datas = rgba.getdata()
  
# newData = []
# for item in datas:
#     if item[0] == 255 and item[1] == 255 and item[2] == 255:  # finding  colour by its RGB value
#         # storing a transparent value when we find a black colour
#         newData.append((255, 255, 255, 0))
#     else:
#         newData.append(item)  # other colours remain unchanged
  
# rgba.putdata(newData)
# rgba.save("transparent_image.png", "PNG")
# 如果当前位深是32的话，可以不用写转RGBA模式的这一句，但是写上也没啥问题
# 从RGB（24位）模式转成RGBA（32位）模式
img = Image.open(r'F:\myDoc\github\Python\日常使用\1.png').convert('RGBA')
W, L = img.size
white_pixel = (255, 255, 255, 255)  # 白色
for h in range(W):
    for i in range(L):
        if img.getpixel((h, i)) == white_pixel:
            img.putpixel((h, i), (0, 0, 0, 0))   # 设置透明
img.save('transparent_image.png')  # 自己设置保存地址