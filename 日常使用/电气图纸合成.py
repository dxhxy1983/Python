import os
import fitz  # PyMuPDF

def get_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()
def get_filename_from_path(filepath):
    return os.path.basename(filepath)
def add_text_to_pdf(input_pdf, output_pdf, text):
    # 打开现有的PDF
    pdf_document = fitz.open(input_pdf)     
    # 遍历每一页
    for page_number in range(len(pdf_document)):
        # 选择要添加文本的页面
        page = pdf_document.load_page(page_number)
        # 定义文本位置
        x, y = 653, 809

    # 插入文本
        page.insert_text((x, y), text, fontsize=12, color=(0, 0, 0))
    filename=get_filename_from_path(input_pdf)
    if filename=="封面.pdf":
         page.insert_text((330, 330), text, fontsize=18, color=(0, 0, 0))

    # 保存更改后的PDF
    pdf_document.save(output_pdf)

if __name__ == "__main__":
    # 获取当前目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_directory, "output")

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 从型号.txt 文件读取要添加的文本
    text_to_add = get_text_from_file(os.path.join(current_directory, "型号.txt"))

    # 遍历当前文件夹下的所有 PDF 文件
    for filename in os.listdir(current_directory):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(current_directory, filename)
            output_pdf_path = os.path.join(output_folder, filename)
            add_text_to_pdf(input_pdf_path, output_pdf_path, text_to_add)
    print("Text added to all PDF files successfully.")





# import fitz  # PyMuPDF
# import os
# import sys
# import glob
# from PyPDF2 import PdfMerger
# def list_pdf_files(folder_path):
#     # 使用glob模块查找所有的PDF文件
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
#     # 获取每个文件的绝对路径
#     absolute_paths = [os.path.abspath(pdf) for pdf in pdf_files]
#     return absolute_paths,pdf_files

# def merge_pdfs(pdf_paths, output_path):
#     merger = PdfMerger()
    
#     for pdf in pdf_paths:
#         merger.append(pdf)
    
#     merger.write(output_path)
#     merger.close()

# def add_text_to_pdf(input_pdf, output_pdf, texts,fontsize, page_number):
#     # 打开现有的PDF
#     pdf_document = fitz.open(input_pdf)

#     # 选择要添加文本的页面
#     page = pdf_document.load_page(page_number)

#     # 获取页面尺寸
#     rect = page.rect
#     width, height = rect.width, rect.height

#     # 循环插入多个文本
#     for text, (x, y) in texts:
#         if 0 <= x <= width and 0 <= y <= height:
#             page.insert_text((x, y), text, fontsize=fontsize, color=(0, 0, 0))
#         else:
#             print(f"Text '{text}' is out of bounds and will not be inserted.")

#     # 保存更改后的PDF
#     pdf_document.save(output_pdf)

# if __name__ == "__main__":
#     current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
#     file_txt=current_path+"\\型号.txt"
#     textList=[]
#     with open(file_txt,'r',encoding="utf-8") as f:
#         i=0
#         for line in f:
#             textList.append(line)

#     filePathList,fileNameList=list_pdf_files(current_path)
#     for i in range(len(filePathList)):

#         input_pdf=filePathList[i]  # 输入PDF文件路径
#         output_pdf=current_path+("\\out\\")+fileNameList[i] # 输出PDF文件路径
#         texts = [(textList[0], (330, 330)),  # 要添加的文本和位置
#                     (textList[1], (653, 812))]  # 另一个文本和位置，确保在页面范围内
#         page_number = 0  # 页面索引（0表示第一页）  
#         add_text_to_pdf(input_pdf, output_pdf, texts,15,page_number)
#     # merge_pdfs(filePathList,current_path)
