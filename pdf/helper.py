import fitz  # PyMuPDF
from math import ceil

# 定义函数来处理PDF缩放和分割
def adjust_pdf_to_a4(input_path, output_path):
    """
    调整PDF文件到A4大小并分割过长的页面。

    :param input_path: 输入PDF文件的路径。
    :param output_path: 输出PDF文件的路径。
    """
    # 打开原始PDF
    doc = fitz.open(input_path)

    # A4纸张尺寸（点单位）
    a4_width, a4_height = 595, 842

    # 创建新的PDF以保存调整后的页面
    new_doc = fitz.open()
    for page in doc:
        # 获取原始页面尺寸
        orig_rect = page.rect
        orig_width, orig_height = orig_rect.width, orig_rect.height

        # 计算缩放比例
        scale = a4_width / orig_width
        mat = fitz.Matrix(scale, scale)

        # 计算缩放后的高度
        scaled_height = orig_height * scale

        # 分割页面
        num_pages = ceil(scaled_height / a4_height)
        for i in range(num_pages):
            portion = fitz.Rect(0, a4_height * i / scale, orig_width, min(a4_height * (i + 1) / scale, orig_height))
            new_page = new_doc.new_page(-1, width=a4_width, height=a4_height)
            new_page.show_pdf_page(new_page.rect, doc, page.number, clip=portion, matrix=mat)

    # 保存调整后的PDF
    new_doc.save(output_path)
    new_doc.close()
    doc.close()

# 函数定义完成
adjust_pdf_to_a4("data/DevOps.pdf", "data/DevOpsSplit.pdf")
