#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/3/23 19:03
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : pdfHelper.py
# @Descr   : pdf操作
# @Software: PyCharm
import fitz


# 将pdf转换为img
def convert_pdf_to_img(pdf_file):
    doc = fitz.open(pdf_file)
    (file_pre_path, temp_filename) = os.path.split(pdf_file)
    (shot_name, file_ext) = os.path.splitext(temp_filename)
    img_path_list = []
    for pg in range(doc.pageCount):
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为3，这将为我们生成分辨率提高6倍的图像。
        zoom_x, zoom_y = 3, 3
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        img_path = os.path.join(file_pre_path, shot_name + "_" + str(pg) + ".png")
        img_path_list.append(img_path)
        pm.writePNG(img_path)
    return "&&&".join(img_path_list)


import os
import comtypes.client


def get_path():
    path = "E:\\work-维璟\\2 项目实施\\2.1行业应用部\\54保险OCR识别\\原油附件压缩包" # 获取当前运行路径
    filename_list = os.listdir(path)
    wordname_list = [filename for filename in filename_list if filename.endswith((".doc", ".docx"))]
    for wordname in wordname_list:
        # 分离word文件名称和后缀，转化为pdf名称
        pdfname = os.path.splitext(wordname)[0] + '.vgis_pdf'
        # 如果当前word文件对应的pdf文件存在，则不转化
        if pdfname in filename_list:
            continue
        wordpath = os.path.join(path, wordname)  # word所在目录
        pdfpath = os.path.join(path, pdfname)  # 存放生成的pdf目录
        # 生成器
        yield wordpath, pdfpath


if __name__ == '__main__':
    word = comtypes.client.CreateObject("Word.Application")
    word.Visiable = 0  # 设置可见性，不可见

    for w, p in get_path():
        newpdf = word.Documents.Open(w)
        newpdf.SaveAS(p, FileFormat=17)  # 17表示PDF格式
        newpdf.Close()